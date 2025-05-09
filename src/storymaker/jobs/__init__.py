# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Minimal async **Job Queue** (Chunk B).

• LocalJobQueue – ThreadPoolExecutor wrapper
• JobStatus / Job models (Pydantic)
• module-level singleton `job_queue` for easy imports
"""

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
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Job(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    task_name: str
    status: JobStatus = JobStatus.PENDING
    created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)
    updated_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)
    result: Any | None = None
    error: str | None = None

    model_config = {"arbitrary_types_allowed": True}  # result can be any python obj

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
    """Thread-pooled job queue with **lightweight** persistence.

    Persistence strategy (keep it simple for MVP):
    • Metadata JSON for each job under data/storymaker/jobs/job_<id>.json
    • Large binary artefacts should be stored by the task itself elsewhere.
    """

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
        """Enqueue *callable* – return job_id immediately."""
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
