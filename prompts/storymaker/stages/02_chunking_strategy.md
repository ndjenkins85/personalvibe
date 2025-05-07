Storymaker already contains a slim, working “skeleton”.  What remains is to flesh-out the full MVP (more models, richer API, SPA, tests, docs, etc.).  If we attempted to emit the entire code-base in a single pass, the result would greatly exceed the ~20 000-character hard limit per LLM response, and we would lose both clarity and the ability to iterate.  Therefore the only practical path is to decompose the deliverables along clear boundaries of responsibility (config ↔ models ↔ I/O ↔ API ↔ frontend ↔ tests/docs) and emit them in small, self-contained increments that each compile and run independently.  Successive chunks can then import or call the artefacts produced earlier, allowing tight feedback loops and easy re-runs if the model or reviewer detects an error.

Applied to Storymaker, we will start with the absolute foundations (project metadata, settings, and domain models), because every later layer—persistence, routes, prompts, React pages—relies on these contracts.  Once the foundations are locked, we can layer on the I/O adapters, then the Flask routes, and finally the SPA and tests.  This “bottom-up, contract-first” strategy minimises rewrites and ensures each 20 k-character burst is logically coherent, individually runnable, and small enough to keep the LLM within its token budget.

────────────────────────────────────────────────────────────────────────────
1.  APPROXIMATE TOTAL PROJECT SIZE
────────────────────────────────────────────────────────────────────────────
• Existing code in repo excerpt ≈ 9 k characters
• New artefacts required for MVP (rough estimate)
  – Expanded Pydantic models & validators .............  6 k
  – Storage adapters (local + placeholder cloud) ......  3 k
  – Auth (cookie + JWT refresh) .......................  4 k
  – Flask routes for 5 pages + utils .................. 10 k
  – CLI / background tasks (image gen jobs) ...........  5 k
  – Front-end React/Vite project (5 pages + router) ... 25 k
  – Unit/integration tests ............................ 10 k
  – Prompt templates & docs ...........................  4 k
  ————————————————————————————————————————————————
  ≈ 77 000 characters in total

Given the 20 000-character ceiling per call, we need 4-5 well-planned chunks.

────────────────────────────────────────────────────────────────────────────
2.  CHUNKING STRATEGY
────────────────────────────────────────────────────────────────────────────
Chunk 0 (optional bootstrap ≤ 3 k)
  • pyproject.toml (Poetry), .env.example, README stubs
  • Ensures later code can `poetry install` & run tests

Chunk 1 – “Domain & Config” (~15 k)
  • storymaker/config.py (finished)
  • logging_config.py (finished)
  • Expanded models: Book, Chapter, Character, User, AuthToken
  • validators & helpers (e.g. Book.cover_image property)
  • __all__ exports + docstrings

Chunk 2 – “Persistence & Auth” (~16 k)
  • data/storage.py (local + S3 placeholder)
  • auth/auth.py (cookie+JWT helpers, login_required decorator)
  • tests for models + storage + auth (pytest)

Chunk 3 – “API Layer” (~18 k)
  • api/app.py (app factory + CORS)
  • api/routes.py (health, books, characters, account, image-job queue)
  • error handlers, DTO schemas, pagination utils
  • tests: flask_client fixture + happy-path CRUD

Chunk 4 – “Frontend SPA Skeleton” (~18 k)
  • vite.config.ts, index.html
  • src/App.tsx with React-Router
  • Pages: Index, MyBooks, Characters, Studio, Account
  • Shared components: NavBar, CardGrid, AvatarUploader
  • Simple fetch wrappers hitting Chunk 3 endpoints

Chunk 5 – “CI, Docs & Prompts” (~7 k)
  • GitHub Actions workflow (lint+test)
  • docs/architecture.md & CONTRIBUTING.md
  • prompts/storymaker/{generate_story.md,generate_chapter.md} final versions
  • README updates and code-sample snippets

────────────────────────────────────────────────────────────────────────────
3.  RECOMMENDED EXECUTION ORDER
────────────────────────────────────────────────────────────────────────────
1. Chunk 0 – Bootstrap (if repo does not already have Poetry scaffolding)
2. Chunk 1 – Domain & Config
3. Chunk 2 – Persistence & Auth
4. Chunk 3 – API Layer
5. Chunk 4 – Frontend SPA Skeleton
6. Chunk 5 – CI, Docs & Prompts

Rationale for order:
• Chunks 1-2 define the “contracts” (models + storage) that everything else imports.
• API layer (Chunk 3) can then be coded and tested using real storage/auth.
• Front-end (Chunk 4) consumes stable JSON endpoints already proven by tests.
• Auxiliary assets and automation (Chunk 5) are least likely to break earlier code.

────────────────────────────────────────────────────────────────────────────
4.  SUMMARY
────────────────────────────────────────────────────────────────────────────
By splitting the remaining 77 k characters into five logical, dependency-ordered deliveries—each ≤ 20 k—we stay within LLM limits while ensuring every slice compiles and runs independently.  Starting with “Domain & Config” first gives later chunks a rock-solid, typed foundation and prevents cascade failures down the line.
