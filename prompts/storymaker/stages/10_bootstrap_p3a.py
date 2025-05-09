# python prompts/storymaker/stages/10_bootstrap_p3a.py
#!/usr/bin/env python
# Copyright © 2025 by Nick Jenkins. All rights reserved
"""
Chunk A – Storymaker **Backend-API foundations**

Running this file will:

1. Locate the git-repo root (via personalvibe.vibe_utils.get_base_path()).
2. Create a *tiny* formal OpenAPI-lite spec (+ route `/api/openapi.json`).
3. Patch `storymaker/api/app.py` to register the new blueprint.
4. Add unit-tests proving the new route & existing health route.
5. Print concise next-step instructions (incl. SPA setup for beginners).

Nothing in the existing repo is deleted – we only append new artefacts
or skip creation if they already exist so the script is **idempotent**.
"""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

from personalvibe import vibe_utils

# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
REPO: Path = vibe_utils.get_base_path()  # project root (~/…/personalvibe)
SRC = REPO / "src"
TESTS = REPO / "tests"


def write(fp: Path, content: str) -> None:
    """Write *content* to file path `fp` (create parents)."""
    fp.parent.mkdir(parents=True, exist_ok=True)
    if fp.exists() and fp.read_text() == content:
        print(f"✓ {fp.relative_to(REPO)} unchanged")
        return
    fp.write_text(content)
    print(f"• Wrote {fp.relative_to(REPO)}")


# --------------------------------------------------------------------------- #
# 1.  New spec blueprint                                                      #
# --------------------------------------------------------------------------- #
bp_code = textwrap.dedent(
    """
    \"\"\"Light-weight OpenAPI-lite blueprint.

    Only captures *paths* and basic schema names.  Good enough for the SPA
    to auto-discover routes until a full swagger.json is generated later.
    \"\"\"

    from __future__ import annotations

    from flask import Blueprint, jsonify, current_app

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
    """
)

write(SRC / "storymaker" / "api" / "spec_blueprint.py", bp_code)

# --------------------------------------------------------------------------- #
# 2.  Patch create_app() to register the blueprint (if not already)           #
# --------------------------------------------------------------------------- #
app_py = SRC / "storymaker" / "api" / "app.py"
app_txt = app_py.read_text()

needle = "register_routes(app)"
patch_code = "    from storymaker.api.spec_blueprint import spec_bp  # auto-added by Chunk A\n    app.register_blueprint(spec_bp)\n"
if "spec_blueprint" not in app_txt:
    # insert right AFTER register_routes(app) call
    app_txt = re.sub(re.escape(needle) + r"(.*\n)+?", needle + "\n" + patch_code, app_txt, count=1)
    write(app_py, app_txt)
else:
    print("✓ storymaker/api/app.py already imports spec_blueprint – skip patch")

# --------------------------------------------------------------------------- #
# 3.  Tests                                                                   #
# --------------------------------------------------------------------------- #
test_api_content = textwrap.dedent(
    '''
    """Smoke-tests for the API foundations (health + openapi)."""

    from storymaker.api.app import create_app


    def _client():
        app = create_app()
        app.testing = True
        return app.test_client()


    def test_health_route():
        rv = _client().get("/api/health")
        assert rv.status_code == 200
        assert rv.get_json() == {"status": "ok"}


    def test_openapi_route():
        rv = _client().get("/api/openapi.json")
        assert rv.status_code == 200
        data = rv.get_json()
        assert data["openapi"].startswith("3.")
        assert "/api/health" in data["paths"]
    '''
)

write(TESTS / "test_api_spec.py", test_api_content)

# --------------------------------------------------------------------------- #
# 4.  Optional .env.example (help newcomers)                                  #
# --------------------------------------------------------------------------- #
env_example = textwrap.dedent(
    """
    # Storymaker – example environment variables
    OPENAI_API_KEY="sk-..."
    STORYMAKER_SECRET_KEY="replace_in_prod"
    """
).lstrip()

write(REPO / ".env.example", env_example)

# --------------------------------------------------------------------------- #
# 5.  Summary to user                                                         #
# --------------------------------------------------------------------------- #
print(
    textwrap.dedent(
        f"""
        ────────────────────────────────
        Chunk A bootstrap completed 🎉
        ────────────────────────────────
        • Run unit tests:      poetry run pytest -q
        • Start API server:    python -m storymaker.api.app  (or `flask run`)
        • Inspect spec:        http://localhost:8777/api/openapi.json

        Front-end quick-start (if you’ve never used React/Vite):

        1. Install Node ≥20 (recommended via https://github.com/nvm-sh/nvm).
        2. cd {REPO.relative_to(Path.cwd()) / 'storymaker_spa'}   # front-end folder
        3. npm install        # pulls dependencies
        4. npm run dev        # launches dev-server on http://localhost:5173

           The dev React app already uses the special header
           “Authorization: DEV” so it can call the Flask API without
           a login step.

        When both servers are running you can open the SPA and browse:
        • Home, My Books, Characters   (data coming from the backend)

        Happy hacking! 🚀
        """
    )
)
