# Copyright © 2025 by Nick Jenkins. All rights reserved
"""HTTP JSON routes grouped by SPA sections (Chunk 3)."""

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
    """Helper → raises APIError on validation problems."""
    try:
        return model_cls.parse_obj(data)
    except ValidationError as e:
        raise APIError(str(e), HTTPStatus.UNPROCESSABLE_ENTITY) from e


# ─────────────────────────── Route registration ─────────────────────
def register_routes(app: Flask) -> None:
    # -----------------------------------------------------------------
    # Index / health
    # -----------------------------------------------------------------
    @app.route("/api/health", methods=["GET"])
    def health():
        return {"status": "ok"}

    # -----------------------------------------------------------------
    # Auth
    # -----------------------------------------------------------------
    @app.route("/api/login", methods=["POST"])
    def login():
        payload = _parse_pydantic(LoginRequest, request.get_json(force=True, silent=True))
        # MVP: only dev user works without password
        if payload.email != DEV_USER.email:
            raise APIError("Only dev@local supported in MVP", HTTPStatus.UNAUTHORIZED)

        token = create_access_token(user_id=DEV_USER.id)
        return jsonify(status="ok", data=LoginResponse(access_token=token).dict())

    @app.route("/api/me", methods=["GET"])
    @login_required
    def me():
        user = getattr(g, "user", DEV_USER)
        return jsonify(
            status="ok", data=MeResponse(id=user.id, email=user.email, display_name=user.display_name).dict()
        )

    # -----------------------------------------------------------------
    # Books
    # -----------------------------------------------------------------
    @app.route("/api/books", methods=["POST"])
    @login_required
    def create_book():
        book_in = _parse_pydantic(BookIn, request.get_json(force=True, silent=True) or {})
        book_id = str(uuid4())
        book = Book(id=book_id, **book_in.dict())
        storage.save_book(book)
        return jsonify(status="ok", data={"book_id": book_id}), 201

    @app.route("/api/books/<book_id>", methods=["GET"])
    @login_required
    def get_book(book_id: str):
        book = storage.load_book(book_id)
        return jsonify(status="ok", data=book.dict())

    @app.route("/api/books", methods=["GET"])
    @login_required
    def list_books():
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
        books = []
        for p in storage.base_dir.glob("book_*.json"):
            try:
                books.append(BookOut.from_model(storage.load_book(p.stem.removeprefix("book_"))))
            except Exception:  # noqa: BLE001
                log.warning("Failed to parse %s", p)
        slice_, meta = paginate(sorted(books, key=lambda b: b.created_at, reverse=True), page, per_page)
        return jsonify(status="ok", data=[b.dict() for b in slice_], meta=meta)

    # -----------------------------------------------------------------
    # Characters
    # -----------------------------------------------------------------
    @app.route("/api/characters", methods=["POST"])
    @login_required
    def create_character():
        char_in = _parse_pydantic(CharacterIn, request.get_json(force=True, silent=True) or {})
        char = Character(**char_in.dict())
        storage.save_json(char.dict(), storage.base_dir / f"character_{char.id}")
        return jsonify(status="ok", data={"character_id": char.id}), 201

    @app.route("/api/characters/<char_id>", methods=["GET"])
    @login_required
    def get_character(char_id: str):
        try:
            data = storage.load_json(storage.base_dir / f"character_{char_id}.json")
            return jsonify(status="ok", data=CharacterOut(**data).dict())
        except FileNotFoundError:
            abort(404)

    @app.route("/api/characters", methods=["GET"])
    @login_required
    def list_characters():
        chars = []
        for p in storage.base_dir.glob("character_*.json"):
            try:
                chars.append(CharacterOut(**storage.load_json(p)))
            except Exception:  # noqa: BLE001
                log.warning("Failed to load character %s", p)
        slice_, meta = paginate(chars, int(request.args.get("page", 1)), int(request.args.get("per_page", 50)))
        return jsonify(status="ok", data=[c.dict() for c in slice_], meta=meta)
