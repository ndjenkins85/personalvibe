# Copyright © 2025 by Nick Jenkins. All rights reserved

"""
chunk3_api_codegen.py

Run this file **once** (or on every `poetry run python chunk3_api_codegen.py`)
to create / overwrite all code artefacts that belong to *Chunk 3 – API Layer*.

It is fully idempotent—existing files are clobbered with the latest
version, new ones are created as needed.

The script relies on `personalvibe.vibe_utils.get_base_path()` to locate the
git-repo root no matter where you launch it from.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from personalvibe import vibe_utils

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
REPO = vibe_utils.get_base_path()


def _write(rel_path: str, raw: str) -> None:
    """Create parent dirs and dump *dedented* text to disk."""
    file_path = REPO / rel_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(textwrap.dedent(raw).lstrip())
    print(f"✓ wrote {file_path.relative_to(REPO)}")


# ─────────────────────────────────────────────────────────────────────────────
# File contents
# ─────────────────────────────────────────────────────────────────────────────
_init_py = """
\"\"\"Storymaker API namespace.

Exposes:
    • create_app ─ Flask application factory
    • All Pydantic DTOs under `schemas`
\"\"\"
from __future__ import annotations

from storymaker.api.app import create_app  # noqa: F401
"""

app_py = """
# Copyright © 2025 by Nick Jenkins. All rights reserved
\"\"\"Flask **application factory** enhanced in Chunk 3.

New features:
    • CORS allow-list pulled from `settings.allowed_origins`
    • JSON error handlers (see `storymaker.api.errors`)
    • Swagger-like `/api/spec` route for quick client introspection
\"\"\"

from __future__ import annotations

import logging

from flask import Flask
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
    register_error_handlers(app)

    @app.route("/api/spec")
    def _spec():
        \"\"\"Very light-weight *poor-man’s* spec until proper OpenAPI.\"\"\"
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

    log.info("🚀 Storymaker API up — debug=%s", settings.debug)
    return app


# ── CLI entry-point (python -m storymaker.api.app) ───────────────────
if __name__ == "__main__":  # pragma: no cover
    create_app().run(debug=settings.debug, port=8777)
"""

schemas_py = """
\"\"\"Pydantic **DTO** layer – clean boundary between HTTP & domain models.\"\"\"
from __future__ import annotations

import datetime as _dt
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from storymaker.models.book import Book
from storymaker.models.character import Character


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# ─────────────────────────── Pagination ──────────────────────────────
class Pagination(BaseSchema):
    page: int
    per_page: int
    total: int


# ───────────────────────────── Books ─────────────────────────────────
class BookIn(BaseSchema):
    name: str = Field(..., min_length=1, max_length=80)
    description: str
    main_character: Character
    side_characters: List[Character] = []
    chapters: List = []  # Lightweight—client can PATCH later


class BookOut(BaseSchema):
    id: str
    name: str
    description: str
    created_at: _dt.datetime

    # Extra computed fields to make the SPA happy
    cover_image: Optional[str]
    page_count: int

    @classmethod
    def from_model(cls, book: Book) -> "BookOut":
        return cls(
            id=book.id,
            name=book.name,
            description=book.description,
            created_at=book.created_at,
            cover_image=str(book.cover_image) if book.cover_image else None,
            page_count=book.page_count,
        )


# ─────────────────────────── Characters ──────────────────────────────
class CharacterIn(Character):
    pass


class CharacterOut(Character):
    pass


# ──────────────────────────── Auth / Me ──────────────────────────────
class LoginRequest(BaseSchema):
    email: EmailStr
    password: str


class LoginResponse(BaseSchema):
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseSchema):
    id: str
    email: EmailStr
    display_name: str
"""

pagination_py = """
\"\"\"Minimal **offset-based** pagination helper.\"\"\"
from __future__ import annotations

from math import ceil
from typing import Any, List, Tuple


def paginate(items: List[Any], page: int = 1, per_page: int = 20) -> Tuple[list, dict]:
    \"\"\"Return `(slice, meta)`.

    Args:
        items: Full data set (already materialised).
        page: 1-based page index.
        per_page: Items per page.

    Returns:
        slice_: Items for the requested page.
        meta: Dict with pagination meta suitable for API response.
    \"\"\"
    total = len(items)
    page = max(page, 1)
    per_page = max(1, per_page)
    start = (page - 1) * per_page
    end = start + per_page
    return (
        items[start:end],
        {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": ceil(total / per_page) if per_page else 1,
        },
    )
"""

errors_py = """
\"\"\"JSON API-friendly error helpers.

Every unhandled exception should bubble into a *structured* JSON blob
so the SPA never has to parse HTML tracebacks.
\"\"\"
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
"""

routes_py = """
# Copyright © 2025 by Nick Jenkins. All rights reserved
\"\"\"HTTP JSON routes grouped by SPA sections (Chunk 3).\"\"\"

from __future__ import annotations

import logging
from http import HTTPStatus
from uuid import uuid4

from flask import Flask, abort, g, jsonify, request
from pydantic import ValidationError

from storymaker.api.errors import APIError
from storymaker.api.pagination import paginate
from storymaker.api.schemas import (
    BookIn,
    BookOut,
    CharacterIn,
    CharacterOut,
    LoginRequest,
    LoginResponse,
    MeResponse,
)
from storymaker.auth.auth import DEV_USER, create_access_token, login_required
from storymaker.data.storage import LocalStorage
from storymaker.logging_config import configure_logging
from storymaker.models.book import Book
from storymaker.models.character import Character

configure_logging()
log = logging.getLogger(__name__)
storage = LocalStorage()


# ─────────────────────────────────────────────────────────────────────
def _parse_pydantic(model_cls, data):  # noqa: ANN001
    \"\"\"Helper → raises APIError on validation problems.\"\"\"
    try:
        return model_cls.parse_obj(data)
    except ValidationError as e:
        raise APIError(str(e), HTTPStatus.UNPROCESSABLE_ENTITY) from e


# ─────────────────────────── Route registration ─────────────────────
def register_routes(app: Flask) -> None:
    # -----------------------------------------------------------------
    # Index / health
    # -----------------------------------------------------------------
    @app.route("/api/health", methods=[\"GET\"])
    def health():
        return {\"status\": \"ok\"}

    # -----------------------------------------------------------------
    # Auth
    # -----------------------------------------------------------------
    @app.route(\"/api/login\", methods=[\"POST\"])
    def login():
        payload = _parse_pydantic(LoginRequest, request.get_json(force=True, silent=True))
        # MVP: only dev user works without password
        if payload.email != DEV_USER.email:
            raise APIError(\"Only dev@local supported in MVP\", HTTPStatus.UNAUTHORIZED)

        token = create_access_token(user_id=DEV_USER.id)
        return jsonify(status=\"ok\", data=LoginResponse(access_token=token).dict())

    @app.route(\"/api/me\", methods=[\"GET\"])
    @login_required
    def me():
        user = getattr(g, \"user\", DEV_USER)
        return jsonify(status=\"ok\", data=MeResponse(id=user.id, email=user.email, display_name=user.display_name).dict())

    # -----------------------------------------------------------------
    # Books
    # -----------------------------------------------------------------
    @app.route(\"/api/books\", methods=[\"POST\"])
    @login_required
    def create_book():
        book_in = _parse_pydantic(BookIn, request.get_json(force=True, silent=True) or {})
        book_id = str(uuid4())
        book = Book(id=book_id, **book_in.dict())
        storage.save_book(book)
        return jsonify(status=\"ok\", data={\"book_id\": book_id}), 201

    @app.route(\"/api/books/<book_id>\", methods=[\"GET\"])
    @login_required
    def get_book(book_id: str):
        book = storage.load_book(book_id)
        return jsonify(status=\"ok\", data=book.dict())

    @app.route(\"/api/books\", methods=[\"GET\"])
    @login_required
    def list_books():
        page = int(request.args.get(\"page\", 1))
        per_page = int(request.args.get(\"per_page\", 20))
        books = []
        for p in storage.base_dir.glob(\"book_*.json\"):
            try:
                books.append(BookOut.from_model(storage.load_book(p.stem.removeprefix(\"book_\"))))
            except Exception:  # noqa: BLE001
                log.warning(\"Failed to parse %s\", p)
        slice_, meta = paginate(sorted(books, key=lambda b: b.created_at, reverse=True), page, per_page)
        return jsonify(status=\"ok\", data=[b.dict() for b in slice_], meta=meta)

    # -----------------------------------------------------------------
    # Characters
    # -----------------------------------------------------------------
    @app.route(\"/api/characters\", methods=[\"POST\"])
    @login_required
    def create_character():
        char_in = _parse_pydantic(CharacterIn, request.get_json(force=True, silent=True) or {})
        char = Character(**char_in.dict())
        storage.save_json(char.dict(), storage.base_dir / f\"character_{char.id}\")
        return jsonify(status=\"ok\", data={\"character_id\": char.id}), 201

    @app.route(\"/api/characters/<char_id>\", methods=[\"GET\"])
    @login_required
    def get_character(char_id: str):
        try:
            data = storage.load_json(storage.base_dir / f\"character_{char_id}.json\")
            return jsonify(status=\"ok\", data=CharacterOut(**data).dict())
        except FileNotFoundError:
            abort(404)

    @app.route(\"/api/characters\", methods=[\"GET\"])
    @login_required
    def list_characters():
        chars = []
        for p in storage.base_dir.glob(\"character_*.json\"):
            try:
                chars.append(CharacterOut(**storage.load_json(p)))
            except Exception:  # noqa: BLE001
                log.warning(\"Failed to load character %s\", p)
        slice_, meta = paginate(chars, int(request.args.get(\"page\", 1)), int(request.args.get(\"per_page\", 50)))
        return jsonify(status=\"ok\", data=[c.dict() for c in slice_], meta=meta)
"""

# ─────────────────────────────────────────────────────────────────────
# Write to disk
# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    _write("src/storymaker/api/__init__.py", _init_py)
    _write("src/storymaker/api/app.py", app_py)
    _write("src/storymaker/api/schemas.py", schemas_py)
    _write("src/storymaker/api/pagination.py", pagination_py)
    _write("src/storymaker/api/errors.py", errors_py)
    _write("src/storymaker/api/routes.py", routes_py)

    print(
        "🎉  Chunk 3 – API Layer code generated successfully.\n"
        "   You can now `poetry run python -m storymaker.api.app` "
        "and visit http://localhost:8777/api/health"
    )
