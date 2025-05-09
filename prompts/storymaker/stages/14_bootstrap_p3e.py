# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/storymaker/stages/14_bootstrap_p3e.py
#!/usr/bin/env python3
"""
Chunk E – *Tests & Polish*

This bootstrap script **adds an API integration-test suite** and a small
polish tweak (root “/” redirect → “/api/spec”) then guides the user on the
next steps.

Run it from *any* sub-folder; it will discover the repo root automatically.

After execution you can simply run:

    poetry run pytest

to verify that all endpoints work end-to-end.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from textwrap import dedent

from personalvibe import vibe_utils

# ────────────────────────── helpers ────────────────────────────
REPO = vibe_utils.get_base_path()
print(f"🛠  Detected repo root at {REPO}")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def touch(path: Path) -> None:
    path.touch(exist_ok=True)


def patch_file(path: Path, needle: str, patch: str) -> None:
    """Append *patch* below *needle* only if not already present."""
    txt = path.read_text()
    if patch.strip() in txt:
        print(f"ℹ️  {path.relative_to(REPO)} already contains patch – skipping")
        return
    idx = txt.find(needle)
    if idx == -1:
        raise RuntimeError(f"Could not find insertion point in {path}")
    new_txt = txt[: idx + len(needle)] + patch + txt[idx + len(needle) :]
    path.write_text(new_txt)
    print(f"✅ Patched {path.relative_to(REPO)}")


# ────────────────────────── 1. Root redirect polish ────────────
app_py = REPO / "src" / "storymaker" / "api" / "app.py"
redirect_patch = dedent(
    """
    # -----------------------------------------------------------------
    # Optional root redirect (nice DX instead of 404 on "/")
    # -----------------------------------------------------------------
    @app.route("/")
    def _root():
        \"\"\"Redirect bare root → poor-man’s API spec.\"\"\"
        from flask import redirect

        return redirect("/api/spec", code=302)
    """
)

patch_file(app_py, "def _openapi():", redirect_patch)

# ────────────────────────── 2. Integration test suite ───────────
tests_dir = REPO / "tests"
ensure_dir(tests_dir)

api_test_file = tests_dir / "test_api_endpoints.py"
if not api_test_file.exists():
    api_test_file.write_text(
        dedent(
            """
            # Copyright © 2025 by Nick Jenkins. All rights reserved
            \"\"\"Happy-path integration tests for Flask API.

            These tests spin up a real Flask test_client, exercise the
            JSON routes, and verify that the LocalStorage layer performs
            the expected round-trips.  They *wipe* the LocalStorage
            folder before/after to stay hermetic.
            \"\"\"

            import json
            from http import HTTPStatus
            from pathlib import Path

            import pytest
            from storymaker.api import create_app
            from storymaker.api.routes import storage  # re-exported LocalStorage

            # ───────────────────────── Fixtures ──────────────────────────
            @pytest.fixture(scope=\"module\")
            def client():
                app = create_app()
                app.config[\"TESTING\"] = True
                with app.test_client() as c:
                    yield c

            @pytest.fixture(autouse=True)
            def _isolated_storage():
                \"\"\"Clean LocalStorage before & after each test.\"\"\"
                storage.wipe_all()
                yield
                storage.wipe_all()

            DEV = {\"Authorization\": \"DEV\"}

            # ───────────────────────── Tests – health & misc ─────────────
            def test_health_ok(client):
                r = client.get(\"/api/health\")
                assert r.status_code == HTTPStatus.OK
                assert r.get_json()[\"status\"] == \"ok\"

            def test_root_redirects(client):
                r = client.get(\"/\", follow_redirects=False)
                assert r.status_code in (301, 302, 308)
                assert r.headers[\"Location\"].endswith(\"/api/spec\")

            # ───────────────────────── Characters CRUD ───────────────────
            def _create_character(client, name=\"Plushie Duck\"):
                payload = {\"name\": name, \"type\": \"toy\", \"description\": \"Soft yellow\"}
                res = client.post(\"/api/characters\", json=payload, headers=DEV)
                assert res.status_code == HTTPStatus.CREATED
                cid = res.get_json()[\"data\"][\"character_id\"]
                # Fetch full object
                full = client.get(f\"/api/characters/{cid}\", headers=DEV).get_json()[\"data\"]
                return full  # dict

            def test_characters_roundtrip(client):
                char = _create_character(client)
                # List returns our character
                listed = client.get(\"/api/characters\", headers=DEV).get_json()[\"data\"]
                assert any(c[\"id\"] == char[\"id\"] for c in listed)

            # ───────────────────────── Books CRUD ────────────────────────
            def _create_book(client, main_character):
                payload = {
                    \"name\": \"My Test Book\",
                    \"description\": \"A lovely description\",
                    \"main_character\": main_character,
                    \"side_characters\": [],
                    \"chapters\": [],
                }
                r = client.post(\"/api/books\", json=payload, headers=DEV)
                assert r.status_code == HTTPStatus.CREATED
                return r.get_json()[\"data\"][\"book_id\"]

            def test_books_roundtrip(client):
                char = _create_character(client)
                book_id = _create_book(client, char)
                # GET
                g = client.get(f\"/api/books/{book_id}\", headers=DEV)
                assert g.status_code == HTTPStatus.OK
                assert g.get_json()[\"data\"][\"name\"] == \"My Test Book\"
                # LIST
                books = client.get(\"/api/books\", headers=DEV).get_json()[\"data\"]
                assert any(b[\"id\"] == book_id for b in books)

            # ───────────────────────── Auth edge cases ───────────────────
            def test_login_must_be_dev_local(client):
                bad = {\"email\": \"foo@example.com\", \"password\": \"x\"}
                r = client.post(\"/api/login\", json=bad)
                assert r.status_code == HTTPStatus.UNAUTHORIZED
            """
        )
    )
    print(f"✅ Created {api_test_file.relative_to(REPO)}")
else:
    print(f"ℹ️  {api_test_file.relative_to(REPO)} already exists – left untouched")

# ────────────────────────── 3. Guidance for user ─────────────────
print(
    dedent(
        f"""
        ───────────────────────────────────────────────────────────────
        SUCCESS – Chunk E assets written/updated.

        Next steps
        ──────────
        1.  Install dev deps (once per machine):
              $ poetry install --with tests

        2.  Run the test suite:
              $ poetry run pytest

            All  🟢  tests (auth, storage, NEW api endpoints) should pass.

        3.  (Optional) start the Flask API locally to verify the new
            '/' redirect:
              $ python -m storymaker.api.app
              Visit http://127.0.0.1:8777/  → should bounce to /api/spec

        4.  Front-end developers can now rely on these tested endpoints.

        Happy hacking! 🚀
        ───────────────────────────────────────────────────────────────
        """
    )
)
