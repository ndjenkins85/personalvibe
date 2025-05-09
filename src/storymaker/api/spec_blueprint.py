# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Light-weight OpenAPI-lite blueprint.

Only captures *paths* and basic schema names.  Good enough for the SPA
to auto-discover routes until a full swagger.json is generated later.
"""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify

spec_bp = Blueprint("spec_bp", __name__)

_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "Storymaker API",
        "version": "0.1.0",
        "description": "Poor-man’s spec – will be replaced by real OpenAPI in a later chunk",
    },
    "paths": {
        "/api/health": {"get": {"summary": "Health check"}},
        "/api/login": {"post": {"summary": "Login (DEV shortcut)"}},
        "/api/me": {"get": {"summary": "Current user info"}},
        "/api/books": {
            "get": {"summary": "List books"},
            "post": {"summary": "Create book"},
        },
        "/api/books/{book_id}": {"get": {"summary": "Get book"}},
        "/api/characters": {
            "get": {"summary": "List characters"},
            "post": {"summary": "Create character"},
        },
        "/api/characters/{char_id}": {"get": {"summary": "Get character"}},
    },
}


@_SPEC.setdefault("__meta__", {})  # noqa: SLF001
def _():  # noqa: D401
    pass


@spec_bp.route("/api/openapi.json")
def openapi_json():
    current_app.logger.debug("Serving /api/openapi.json")
    return jsonify(_SPEC)
