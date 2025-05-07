# Copyright © 2025 by Nick Jenkins. All rights reserved

"""HTTP routes grouped by SPA pages.

We expose **JSON APIs** consumed by the React / Vue front-end rather
than serving full HTML (the latter lives in `web/templates` mostly
for SSR fallback).
"""

from __future__ import annotations

import logging
from uuid import uuid4

from flask import Flask, abort, jsonify, request

from storymaker.data.storage import LocalStorage
from storymaker.logging_config import configure_logging
from storymaker.models.book import Book

configure_logging()
log = logging.getLogger(__name__)
storage = LocalStorage()


def register_routes(app: Flask) -> None:
    # -----------------------------------------------------------------
    # Index / health
    # -----------------------------------------------------------------
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify(status="ok", time=request.environ.get("werkzeug.request").start_time)

    # -----------------------------------------------------------------
    # Books
    # -----------------------------------------------------------------
    @app.route("/api/books", methods=["POST"])
    def create_book():
        payload = request.get_json(force=True, silent=True)
        if not payload:
            abort(400, "JSON body required")

        # VERY simplified—assumes valid payload
        book_id = str(uuid4())
        payload["id"] = book_id
        book = Book(**payload)
        storage.save_book(book)
        return jsonify(status="ok", data={"book_id": book_id})

    @app.route("/api/books/<book_id>", methods=["GET"])
    def get_book(book_id: str):
        book = storage.load_book(book_id)
        return jsonify(status="ok", data=book.dict())
