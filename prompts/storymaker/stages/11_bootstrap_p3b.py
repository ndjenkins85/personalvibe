# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/storymaker/stages/11_bootstrap_p3b.py
# build_chunk_b_jobqueue.py
"""
Chunk B – Job Queue bootstrapper
────────────────────────────────
Run this file **once from anywhere inside the repo**:

    poetry run python build_chunk_b_jobqueue.py

What it does:
1. Locates the repo root (via personalvibe.vibe_utils.get_base_path()).
2. Creates NEW modules:
      • storymaker/jobs/…           – in-memory + disk-persisted job queue
      • storymaker/api/jobs.py       – Flask blueprint (/api/jobs/*)
3. Patches storymaker/api/app.py to register the new blueprint.
4. Adds pytest covering the happy path (submit job → poll → result).
5. Prints usage examples (curl + SPA hint).

Safe to re-run; files are overwritten idempotently.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path().resolve()


# --------------------------------------------------------------------------- #
# Helper utils
# --------------------------------------------------------------------------- #
def write(path: Path, content: str):
    """Make parent dirs, write `content` UTF-8."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    print(f"✓ wrote {path.relative_to(REPO)}")


# --------------------------------------------------------------------------- #
# 1. storymaker/jobs/…
# --------------------------------------------------------------------------- #
jobs_init = """
    \"\"\"Minimal async **Job Queue** (Chunk B).

    • LocalJobQueue – ThreadPoolExecutor wrapper
    • JobStatus / Job models (Pydantic)
    • module-level singleton `job_queue` for easy imports
    \"\"\"

    from __future__ import annotations

    import datetime as _dt
    import logging
    import threading
    import uuid
    from concurrent.futures import Future, ThreadPoolExecutor, as_completed
    from pathlib import Path
    from typing import Any, Callable, Dict, Final

    from pydantic import BaseModel, Field
    from storymaker.config import settings
    from storymaker.logging_config import configure_logging

    configure_logging()
    log = logging.getLogger(__name__)

    # ────────────────────────────────────────────────────────────────────────
    # Models
    # ────────────────────────────────────────────────────────────────────────
    class JobStatus(str):
        PENDING    = "pending"
        RUNNING    = "running"
        COMPLETED  = "completed"
        FAILED     = "failed"


    class Job(BaseModel):
        id: str = Field(default_factory=lambda: str(uuid.uuid4()))
        task_name: str
        status: JobStatus = JobStatus.PENDING
        created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)
        updated_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)
        result: Any | None = None
        error: str | None = None

        model_config = { "arbitrary_types_allowed": True }  # result can be any python obj

        def dict_for_api(self) -> dict[str, Any]:
            return {
                "id": self.id,
                "task_name": self.task_name,
                "status": self.status,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat(),
                "error": self.error,
            }


    # ────────────────────────────────────────────────────────────────────────
    # In-memory queue
    # ────────────────────────────────────────────────────────────────────────
    class LocalJobQueue:
        \"\"\"Thread-pooled job queue with **lightweight** persistence.

        Persistence strategy (keep it simple for MVP):
        • Metadata JSON for each job under data/storymaker/jobs/job_<id>.json
        • Large binary artefacts should be stored by the task itself elsewhere.
        \"\"\"

        _JOBS_DIR: Final[Path] = (settings.data_dir / "jobs").expanduser()

        def __init__(self, max_workers: int = 4):
            self._executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="job")
            self._jobs: dict[str, Job] = {}
            self._futures: dict[str, Future] = {}
            self._lock = threading.Lock()
            self._JOBS_DIR.mkdir(parents=True, exist_ok=True)
            log.info("🪄 LocalJobQueue ready (workers=%s)", max_workers)

        # -------------------------- public API --------------------------
        def submit(self, fn: Callable, *args, **kwargs) -> str:
            \"\"\"Enqueue *callable* – return job_id immediately.\"\"\"
            job = Job(task_name=fn.__name__)
            with self._lock:
                self._jobs[job.id] = job
                self._persist(job)

            # wrap callable so we can update status/result centrally
            def _runner():  # noqa: ANN001
                _update = self._update_status
                _update(job.id, JobStatus.RUNNING)
                try:
                    result = fn(*args, **kwargs)
                    _update(job.id, JobStatus.COMPLETED, result=result)
                except Exception as e:  # noqa: BLE001
                    log.exception("Job %s failed: %s", job.id, e)
                    _update(job.id, JobStatus.FAILED, error=str(e))
                    raise

            fut = self._executor.submit(_runner)
            with self._lock:
                self._futures[job.id] = fut
            return job.id

        def get(self, job_id: str) -> Job:
            with self._lock:
                if job_id in self._jobs:
                    return self._jobs[job_id]
            # Attempt disk load (after restart) – not fully bullet-proof but fine for dev
            path = self._JOBS_DIR / f"job_{job_id}.json"
            if path.exists():
                return Job.parse_file(path)
            raise KeyError(job_id)

        def await_job(self, job_id: str, timeout: float | None = None) -> Job:
            fut = self._futures.get(job_id)
            if not fut:
                raise KeyError(job_id)
            fut.result(timeout=timeout)  # will raise if failed
            return self.get(job_id)

        # -------------------------- internals --------------------------
        def _update_status(self, job_id: str, status: JobStatus, *, result: Any | None = None, error: str | None = None):
            with self._lock:
                job = self._jobs[job_id]
                job.status = status
                job.updated_at = _dt.datetime.utcnow()
                if result is not None:
                    job.result = result
                if error is not None:
                    job.error = error
                self._persist(job)

        def _persist(self, job: Job):
            path = self._JOBS_DIR / f"job_{job.id}.json"
            path.write_text(job.model_dump_json(indent=2, exclude_none=True), encoding="utf-8")
            log.debug("💾 persisted job %s (%s)", job.id, job.status)

    # module-level singleton
    job_queue: Final[LocalJobQueue] = LocalJobQueue()
    """

write(REPO / "src/storymaker/jobs/__init__.py", jobs_init)

# --------------------------------------------------------------------------- #
# 2. storymaker/api/jobs.py – Flask blueprint
# --------------------------------------------------------------------------- #
api_jobs_bp = """
    \"\"\"Blueprint exposing **/api/jobs** endpoints.\"\"\"

    from __future__ import annotations

    import logging
    import time
    from http import HTTPStatus

    from flask import Blueprint, jsonify, request
    from pydantic import ValidationError

    from storymaker.api.errors import APIError
    from storymaker.jobs import job_queue

    bp = Blueprint("jobs", __name__, url_prefix="/api/jobs")
    log = logging.getLogger(__name__)

    # --------------------------------------------------------------------- #
    # Helpers
    # --------------------------------------------------------------------- #
    def _parse_json():
        return request.get_json(force=True, silent=True) or {}


    # --------------------------------------------------------------------- #
    # Routes
    # --------------------------------------------------------------------- #
    @bp.route("/demo", methods=[ "POST" ])
    def demo_job():
        \"\"\"Launch a **fake 5-second job**.

        Body can contain { "sleep": int } to tweak duration.
        \"\"\"
        payload = _parse_json()
        sleep_s: int = int(payload.get("sleep", 5))

        def _slow_task(duration: int):
            time.sleep(duration)
            return { "slept": duration }

        job_id = job_queue.submit(_slow_task, sleep_s)
        log.info("Queued demo_job %s (sleep=%s)", job_id, sleep_s)
        return jsonify(status="accepted", job_id=job_id), HTTPStatus.ACCEPTED


    @bp.route("/<job_id>", methods=[ "GET" ])
    def job_status(job_id: str):
        try:
            job = job_queue.get(job_id)
        except KeyError:
            raise APIError("Job not found", HTTPStatus.NOT_FOUND)  # noqa: TRY003
        return jsonify(status="ok", data=job.dict_for_api())
    """

write(REPO / "src/storymaker/api/jobs.py", api_jobs_bp)

# --------------------------------------------------------------------------- #
# 3. Patch storymaker/api/app.py (register blueprint)
# --------------------------------------------------------------------------- #
app_path = REPO / "src/storymaker/api/app.py"
original = app_path.read_text(encoding="utf-8")
needle = "register_error_handlers(app)"
patch_line = "    from storymaker.api.jobs import bp as jobs_bp\n    app.register_blueprint(jobs_bp)"
if patch_line not in original:
    modified = original.replace(
        "register_error_handlers(app)",
        "register_error_handlers(app)\n\n" + patch_line,
    )
    write(app_path, modified)
else:
    print("✓ app.py already patched")


# --------------------------------------------------------------------------- #
# 4. tests/test_jobs.py
# --------------------------------------------------------------------------- #
tests_jobs = """
    import time

    from storymaker.jobs import job_queue

    def _echo(x):  # quick task
        return x * 2

    def test_job_queue_basic():
        job_id = job_queue.submit(_echo, 21)
        # wait max 2 seconds (should be instant)
        job = job_queue.await_job(job_id, timeout=2)
        assert job.status == "completed"
        assert job.result == 42
    """

write(REPO / "tests/test_jobs.py", tests_jobs)

# --------------------------------------------------------------------------- #
# 5. Developer directions
# --------------------------------------------------------------------------- #
print(
    """
────────────────────────────────────────────────────────────────────────────
Chunk B – Job Queue installed!  Quick manual test:

1.  Start the Flask API (if not running yet):

        python -m storymaker.api.app

2.  In another shell hit the **demo** endpoint:

        curl -X POST http://localhost:8777/api/jobs/demo \\
             -H "Content-Type: application/json" \\
             -d '{"sleep":3}'

    → HTTP/1.1 202 Accepted
      {"status":"accepted","job_id":"<uuid>"}

3.  Poll until done:

        curl http://localhost:8777/api/jobs/<job_id>

    Status field transitions: pending → running → completed.

Front-end integration hint
──────────────────────────
A React component can POST the job, stash `job_id` in state, then poll
`/api/jobs/<id>` every second until `status === "completed"`.  Replace
the dummy `/demo` job with a real *image generation* task in later
chunks.

Pytest
──────
Automated test added:  `poetry run pytest -k job_queue`

Happy hacking!  🪄
"""
)
