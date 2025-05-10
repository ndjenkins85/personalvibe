Storymaker already has a rock-solid “hello-world” stack: a Flask API with auth, Pydantic models, local JSON storage, a minimal React/Vite SPA, and an async job queue.  All smoke-tests are green (Chunk 6/8), but the product still stops at “create empty book”.  The next leap of value is letting users press “Generate story” in Studio and actually receive a full 10-chapter script + (stub) images they can edit.  That entails new background jobs, DTOs, CRUD routes, and front-end flows—large enough that we must slice the work so each slice fits comfortably under an LLM’s ~20 k character reply limit and under a human’s review bandwidth.

Below is a concrete plan that (1) defines the next milestone, (2) estimates its code size, (3) splits it into ≤ 5 coherent chunks, and (4) orders them so each chunk scaffolds the next.

────────────────────────────────────────────────────────────────────────
1. Current state
────────────────────────────────────────────────────────────────────────
• Backend serves health, books, characters, auth; LocalStorage + JobQueue exist.
• SPA can list/create characters & book stubs, but Studio step 2 is a placeholder.
• Unit tests & lint pass; CORS, JWT DEV mode, logging, etc. are in place.

────────────────────────────────────────────────────────────────────────
2. Next major milestone  –  “Script & Image Generation MVP”
────────────────────────────────────────────────────────────────────────
Goal: A user clicks “Next” in Studio → the backend launches a job that
  a) calls OpenAI with the generate_story_prompt,
  b) stores the resulting CSV as chapters inside the book JSON,
  c) (optionally) kicks off chapter-image sub-jobs (stubbed),
  d) lets the SPA poll and then display an editable table of chapters.
Acceptance: end-to-end happy-path works and is covered by tests.

────────────────────────────────────────────────────────────────────────
3. Size estimate
────────────────────────────────────────────────────────────────────────
Code & docs to add (roughly):
  • New schemas + routes + tests …………………… ~6 k chars
  • Job helpers / OpenAI wrapper / storage glue … ~5 k
  • SPA components (ChapterTable, polling hook) … ~7 k
  • Docs + migration notes …………………………… ~2 k
Total ≈ 20 k chars   → just above one-shot limit, hence chunking.

────────────────────────────────────────────────────────────────────────
4. Chunking (≤ 5 pieces, each ≤ 10 k, average 6–8 k)
────────────────────────────────────────────────────────────────────────
Rank | Chunk (logical focus)                                           | Est. chars | Reason this must come first
---- | --------------------------------------------------------------- | ---------- | ---------------------------------------------
1    | Data & DTO foundation                                            | 4 k        | Adds ChapterCSV, BookWithChaptersOut, JobDTO; enables the rest.
2    | Backend routes & story-generation job                            | 7 k        | /api/books/<id>/generate, job handler calling OpenAI, persistence, tests.
3    | Chapter PATCH/PUT routes + validation                            | 4 k        | Needed before the UI can edit scenes; small but unlocks FE work.
4    | Front-end: polling hook, ChapterTable component, Studio step 2   | 8 k        | Consumes new endpoints, displays chapters, allows edits.
5    | Image-generation stub + regenerate-chapter flow + docs           | 5 k        | Optional polish that exercises JobQueue; sits nicely after script flow works.

Each chunk comfortably fits in one LLM reply, lets a human run tests, and leaves the repo in a green state before moving on.

────────────────────────────────────────────────────────────────────────
5. Recommended execution order (same as rank above)
────────────────────────────────────────────────────────────────────────
1. Data/DTO foundation
2. Backend “generate story” job & route
3. Chapter edit / PATCH support
4. Front-end Studio step 2 (poll & table)
5. Image-generation stub & regenerate flow

By tackling schema and backend scaffolding first we ensure later chunks (especially the React work) compile against actual, testable endpoints, preventing wasted cycles on mock contracts.
