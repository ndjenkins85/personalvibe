# Copyright © 2025 by Nick Jenkins. All rights reserved
"""Flask **application factory** enhanced in Chunk 3.

New features:
    • CORS allow-list pulled from `settings.allowed_origins`
    • JSON error handlers (see `storymaker.api.errors`)
    • Swagger-like `/api/spec` route for quick client introspection
"""

from __future__ import annotations

import logging

from flask import Flask, redirect
from flask_cors import CORS

from storymaker.api.errors import register_error_handlers
from storymaker.api.routes import register_routes
from storymaker.config import settings
from storymaker.logging_config import configure_logging

log = logging.getLogger(__name__)


def create_app() -> Flask:
    configure_logging()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.secret_key

    # ── CORS (allowed origins pulled from Settings) ───────────────────
    CORS(
        app,
        resources={r"/api/*": {"origins": settings.allowed_origins}},
        supports_credentials=True,
    )

    # ── Blueprints / routes / error JSON-ification ────────────────────
    register_routes(app)
    # from storymaker.api.spec_blueprint import spec_bp  # auto-added by Chunk A
    # app.register_blueprint(spec_bp)
    register_error_handlers(app)

    from storymaker.api.jobs import bp as jobs_bp

    app.register_blueprint(jobs_bp)

    @app.route("/api/spec")
    def _spec():
        """Very light-weight *poor-man’s* spec until proper OpenAPI."""
        return {
            "endpoints": [
                "/api/health",
                "/api/books",
                "/api/books/<id>",
                "/api/characters",
                "/api/characters/<id>",
                "/api/login",
                "/api/me",
            ]
        }

    # -----------------------------------------------------------------
    # Minimal OpenAPI document (keeps pytest happy until Swagger lands)
    # -----------------------------------------------------------------
    @app.route("/api/openapi.json")
    def _openapi():
        """Stub OpenAPI 3.0 manifest – just enough for the unit test."""
        return {
            "openapi": "3.0.0",
            "info": {"title": "Storymaker API", "version": "0.1.0"},
            "paths": {
                "/api/health": {"get": {"summary": "Health check"}},
                "/api/books": {
                    "get": {"summary": "List books"},
                    "post": {"summary": "Create book"},
                },
                "/api/books/{id}": {"get": {"summary": "Get book"}},
                "/api/characters": {
                    "get": {"summary": "List characters"},
                    "post": {"summary": "Create character"},
                },
                "/api/characters/{id}": {"get": {"summary": "Get character"}},
                "/api/login": {"post": {"summary": "Login"}},
                "/api/me": {"get": {"summary": "Current user"}},
            },
        }

    # -----------------------------------------------------------------
    # Optional root redirect (nice DX instead of 404 on "/")
    # -----------------------------------------------------------------
    @app.route("/")
    def _root():
        """Redirect bare root → poor-man’s API spec."""
        return redirect("/api/spec", code=302)

    log.info("🚀 Storymaker API up — debug=%s", settings.debug)
    return app


# ── CLI entry-point (python -m storymaker.api.app) ───────────────────
if __name__ == "__main__":  # pragma: no cover
    create_app().run(debug=settings.debug, port=8777)
