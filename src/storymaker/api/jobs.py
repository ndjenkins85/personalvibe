# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Blueprint exposing **/api/jobs** endpoints."""

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
@bp.route("/demo", methods=["POST"])
def demo_job():
    """Launch a **fake 5-second job**.

    Body can contain { "sleep": int } to tweak duration.
    """
    payload = _parse_json()
    sleep_s: int = int(payload.get("sleep", 5))

    def _slow_task(duration: int):
        time.sleep(duration)
        return {"slept": duration}

    job_id = job_queue.submit(_slow_task, sleep_s)
    log.info("Queued demo_job %s (sleep=%s)", job_id, sleep_s)
    return jsonify(status="accepted", job_id=job_id), HTTPStatus.ACCEPTED


@bp.route("/<job_id>", methods=["GET"])
def job_status(job_id: str):
    try:
        job = job_queue.get(job_id)
    except KeyError:
        raise APIError("Job not found", HTTPStatus.NOT_FOUND)  # noqa: TRY003
    return jsonify(status="ok", data=job.dict_for_api())
