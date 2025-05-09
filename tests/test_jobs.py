# Copyright © 2025 by Nick Jenkins. All rights reserved

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
