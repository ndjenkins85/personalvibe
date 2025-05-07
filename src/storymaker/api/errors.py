# Copyright © 2025 by Nick Jenkins. All rights reserved

"""JSON API-friendly error helpers.

Every unhandled exception should bubble into a *structured* JSON blob
so the SPA never has to parse HTML tracebacks.
"""

from __future__ import annotations

import logging
from http import HTTPStatus

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

log = logging.getLogger(__name__)


class APIError(HTTPException):
    def __init__(self, message: str, status_code: int = HTTPStatus.BAD_REQUEST):
        super().__init__(description=message)
        self.code = status_code


def _to_json(err: HTTPException):
    payload = {
        "status": "error",
        "error": err.description or HTTPStatus(err.code).phrase,
        "code": err.code,
    }
    return jsonify(payload), err.code


def register_error_handlers(app: Flask) -> None:
    # Built-in HTTPException (404, 400, etc.)
    app.register_error_handler(HTTPException, _to_json)

    # Fallback for *any* uncaught error – always 500
    def _internal(err):  # noqa: ANN001
        log.exception("Unhandled exception: %s", err)
        return jsonify({"status": "error", "error": "Internal Server Error", "code": 500}), 500

    app.register_error_handler(Exception, _internal)
