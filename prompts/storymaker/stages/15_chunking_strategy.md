Large systems become tractable when each incremental slice is **both self-consistent and independently verifiable**. Because a language model can emit only \~20 000 characters at a time, the safest path is to carve the roadmap along *natural architectural seams*—pure-Python services first, then API glue, then front-end consumption—so that every slice compiles, passes tests, and delivers a visible sliver of value before the next layer depends on it.  With Storymaker the main gap is turning an empty “book” record into a fully illustrated, reviewable story.  We therefore anchor the plan around an *End-to-End Story Creation* milestone and ensure that no chunk exceeds the token budget while still leaving space for docs and tests.

Applied to the brief, this means: (1) auditing what already exists (CRUD API, SPA skeleton, prompts), (2) defining the smallest feature that lets a user generate and review a book, and (3) splitting the work into ≤ 5 logical chunks, each < 20 k characters, that march steadily toward that feature.  The ordering starts with the most foundational code (prompt rendering + workers) and finishes with purely cosmetic UI, keeping risks low and feedback loops tight.

---

## 1 · Current state (high-level)

| Area               | Implemented assets                                                                     | Missing / weak spots                                                                        |
| ------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Backend**        | Flask app with CRUD for books & characters; local file storage; auth; basic test suite | No OpenAI integration; no background job orchestration; no chapter/image persistence routes |
| **Frontend SPA**   | Vite + React skeleton; five nav pages; fetch wrapper                                   | Studio step-2 editor, avatar upload, book viewer, polling logic                             |
| **Prompts / data** | `generate_story.md`, `generate_chapter.md`; example notebook                           | Not wired into API; no image pipeline                                                       |
| **Ops / tests**    | Poetry, logging, CI green                                                              | Tests for new flows absent                                                                  |

---

## 2 · Next major milestone

**Milestone 7 – End-to-End Story Creation & Review**

A logged-in user can:

1. Create/choose characters.
2. In **Studio > Generate**, submit title + characters.
3. Backend queues a *story-gen* job → returns 10-scene CSV.
4. Worker fan-outs *chapter-gen* jobs → stores PNGs under `data/storymaker/book_<id>/`.
5. Studio polls job; when done, shows editable chapter rows with thumbnails + “Regenerate” per row.
6. Book appears in **My Books** with real cover; clicking opens a chapter carousel.

---

## 3 · Approximate size of milestone

| Component                                           | ≈ Characters |
| --------------------------------------------------- | ------------ |
| Prompt engine (Jinja render, OpenAI wrapper)        | 3 k          |
| Story & chapter worker modules                      | 4 k          |
| New API routes (`/generate`, `/chapters`, job poll) | 4 k          |
| Storage utils + static image serving                | 3 k          |
| SPA additions (Studio editor, polling hooks)        | 6 k          |
| Tests & fixtures                                    | 4 k          |
| Docs / README tweaks                                | 1 k          |
| **Total**                                           | **≈ 25 k**   |

Since 25 k > 20 k, we divide into four slices (\~6–7 k each).

---

## 4 · Work split into ≤ 5 manageable chunks

| Chunk                                 | Scope (all code + tests)                                                                                                 | Est. chars | Compile/test gate                    |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ---------- | ------------------------------------ |
| **A – Prompt Engine & Workers**       | `prompt_engine.py`, `workers/story_gen.py`, `workers/chapter_gen.py`; monkey-patched OpenAI stubs                        | \~6 k      | `pytest -k workers`                  |
| **B – Generation API & Job Wiring**   | Endpoints: `POST /api/books/<id>/generate`, `GET /api/books/<id>/chapters`, job queue integration, storage of CSV & PNGs | \~7 k      | API unit + integration tests         |
| **C – Studio Step-2 UI**              | React context for job polling, chapter-editor table, regenerate buttons, API hooks                                       | \~6 k      | React Testing Library suites         |
| **D – Book Viewer & Static Assets**   | Flask blueprint to serve images, SPA `/books/:id` carousel viewer, minor CSS                                             | \~5 k      | Static-route tests + component tests |
| *(Optional E – Avatar polish / docs)* | Only if budget permits                                                                                                   | <3 k       | N/A                                  |

---

## 5 · Recommended execution order

1. **Chunk A** – Foundation: guarantees deterministic CSV/PNG outputs.
2. **Chunk B** – Exposes foundation via HTTP; enables backend E2E.
3. **Chunk C** – Consumes stable API; unlocks user-visible progress.
4. **Chunk D** – Pure UI polish; zero downstream blockers.

---

## 6 · Why this ordering works

*Building bottom-up* isolates risk: the prompt engine can be unit-tested without UI, the API can be hit with `curl` before React exists, and the SPA can rely on frozen contracts.  Each deliverable fits well under 20 000 characters, includes its own tests, and produces an artifact that the next chunk can mock or build upon.  Human review effort stays reasonable (≤ 5 PRs), and by delivering a visible Story Creation flow by Milestone 7 we maximise motivation and feedback while leaving room for later niceties such as advanced avatar tooling or cloud storage migration.
