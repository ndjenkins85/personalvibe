# Copyright © 2025 by Nick Jenkins. All rights reserved


"""Persistence back-ends for Storymaker.

Chunk 2 expands the earlier *disk-only* helper into a **pluggable**
architecture ready for future S3 / Firestore migration.  Business
logic and API routes should import **Storage** (alias for the default
backend) rather than hard-coding `LocalStorage`.
"""

from __future__ import annotations

import json
import logging
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Final, TypeVar

from storymaker.config import settings
from storymaker.logging_config import configure_logging
from storymaker.models.book import Book
from storymaker.models.user import User

configure_logging()
log = logging.getLogger(__name__)

T = TypeVar("T")  # generic for save/load


# ──────────────────────────────────────────────────────────────────────────────
# Abstract interface
# ──────────────────────────────────────────────────────────────────────────────
class StorageBackend(ABC):
    """Interface every storage backend must satisfy."""

    # ---------------- Generic helpers -----------------
    @abstractmethod
    def save_json(self, obj: T, path: Path) -> Path: ...

    @abstractmethod
    def load_json(self, path: Path) -> T: ...

    # ---------------- Domain helpers -----------------
    # Book
    @abstractmethod
    def save_book(self, book: Book) -> Path: ...

    @abstractmethod
    def load_book(self, book_id: str) -> Book: ...

    # User
    @abstractmethod
    def save_user(self, user: User) -> Path: ...

    @abstractmethod
    def load_user(self, user_id: str) -> User: ...


# ──────────────────────────────────────────────────────────────────────────────
# Concrete local-filesystem implementation
# ──────────────────────────────────────────────────────────────────────────────
class LocalStorage(StorageBackend):
    """Disk-based JSON storage under `settings.data_dir`."""

    SUFFIX: Final[str] = ".json"

    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = (base_dir or settings.data_dir).expanduser()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        log.info("📂 LocalStorage ready at %s", self.base_dir.resolve())

    # ---------------- Generic helpers -----------------
    def save_json(self, obj: Any, path: Path) -> Path:
        path = path.with_suffix(self.SUFFIX)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False))
        tmp.replace(path)  # atomic-ish on POSIX
        log.debug("Saved %s (%s bytes)", path.name, path.stat().st_size)
        return path

    def load_json(self, path: Path) -> Any:
        return json.loads(path.read_text())

    # ---------------- Domain helpers -----------------
    # Book
    def save_book(self, book: Book) -> Path:
        return self.save_json(book.dict(), self.base_dir / f"book_{book.id}")

    def load_book(self, book_id: str) -> Book:
        data = self.load_json(self.base_dir / f"book_{book_id}{self.SUFFIX}")
        return Book(**data)

    # User
    def save_user(self, user: User) -> Path:
        return self.save_json(user.dict(), self.base_dir / f"user_{user.id}")

    def load_user(self, user_id: str) -> User:
        data = self.load_json(self.base_dir / f"user_{user_id}{self.SUFFIX}")
        return User(**data)

    # ---------------- Utility -----------------
    def wipe_all(self) -> None:
        """Dangerous helper for tests → removes *everything* under base_dir."""
        shutil.rmtree(self.base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        log.warning("🧹 LocalStorage wiped %s", self.base_dir)


# ──────────────────────────────────────────────────────────────────────────────
# S3 placeholder – to be implemented in a later chunk
# ──────────────────────────────────────────────────────────────────────────────
class S3Storage(StorageBackend):  # pragma: no cover
    """*Not implemented* – stub for future migration."""

    def __init__(self, bucket: str) -> None:
        raise NotImplementedError("S3 backend will arrive in a future chunk.")

    # All abstract methods intentionally raise for now
    def save_json(self, obj, path: Path):  # type: ignore[override]
        raise NotImplementedError()

    def load_json(self, path: Path):  # type: ignore[override]
        raise NotImplementedError()

    def save_book(self, book: Book):  # type: ignore[override]
        raise NotImplementedError()

    def load_book(self, book_id: str):  # type: ignore[override]
        raise NotImplementedError()

    def save_user(self, user: User):  # type: ignore[override]
        raise NotImplementedError()

    def load_user(self, user_id: str):  # type: ignore[override]
        raise NotImplementedError()


# Default alias used by business logic – *swap here* to migrate backend
Storage: type[StorageBackend] = LocalStorage
