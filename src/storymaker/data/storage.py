# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Filesystem storage backend.

Abstracts CRUD operations so future migrations (e.g. S3, Firestore)
require only swapping this module—business logic remains untouched.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from storymaker.config import settings
from storymaker.logging_config import configure_logging
from storymaker.models.book import Book

configure_logging()
log = logging.getLogger(__name__)


class LocalStorage:
    """Disk-based storage under `settings.data_dir`."""

    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or settings.data_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        log.info("LocalStorage initialised at %s", self.base_dir.resolve())

    # -----------------------------------------------------------------
    # Book persistence
    # -----------------------------------------------------------------
    def save_book(self, book: Book) -> Path:
        """Serialise `Book` → JSON on disk and return the file path."""
        path = self.base_dir / f"{book.id}.json"
        path.write_text(book.json(indent=2, ensure_ascii=False))
        log.info("Saved book %s (%s bytes)", book.id, path.stat().st_size)
        return path

    def load_book(self, book_id: str) -> Book:
        path = self.base_dir / f"{book_id}.json"
        data: dict[str, Any] = json.loads(path.read_text())
        return Book(**data)
