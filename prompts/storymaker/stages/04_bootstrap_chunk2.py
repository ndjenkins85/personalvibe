# Copyright © 2025 by Nick Jenkins. All rights reserved

"""
chunk_2_persistence_and_auth.py  ⚙️

Executable helper that **writes / updates** all code artefacts for
“3. Chunk 2 – Persistence & Auth” of the Storymaker project.

Run it once from anywhere inside the repo:

    $ python chunk_2_persistence_and_auth.py

After execution the following files will have been *created / overwritten*:

• src/storymaker/data/storage.py        (abstract backend, Local+S3)
• src/storymaker/auth/auth.py           (password hash + JWT + decorator)
• tests/test_storage.py
• tests/test_auth.py
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

from personalvibe import vibe_utils

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────
REPO = vibe_utils.get_base_path()
SRC = REPO / "src"
TESTS = REPO / "tests"
TESTS.mkdir(exist_ok=True, parents=True)


def write(rel_path: str, code: str) -> None:
    """Utility to write `code` to `REPO/rel_path`, creating folders as needed."""
    path = REPO / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(code).lstrip())
    print(f"✓ wrote {path.relative_to(REPO)}")


# ──────────────────────────────────────────────────────────────────────────────
# 1.  data/storage.py  – persistence layer (Abstract → Local + S3 stub)
# ──────────────────────────────────────────────────────────────────────────────
storage_py = r"""
# Copyright © 2025 by Nick Jenkins. All rights reserved
"""
# provide code string with dedent; craft content:

storage_py += r"""
"""
storage_py += """
\"\"\"Persistence back-ends for Storymaker.

Chunk 2 expands the earlier *disk-only* helper into a **pluggable**
architecture ready for future S3 / Firestore migration.  Business
logic and API routes should import **Storage** (alias for the default
backend) rather than hard-coding `LocalStorage`.
\"\"\"

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
    \"\"\"Interface every storage backend must satisfy.\"\"\"

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
    \"\"\"Disk-based JSON storage under `settings.data_dir`.\"\"\"

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
        \"\"\"Dangerous helper for tests → removes *everything* under base_dir.\"\"\"
        shutil.rmtree(self.base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        log.warning("🧹 LocalStorage wiped %s", self.base_dir)


# ──────────────────────────────────────────────────────────────────────────────
# S3 placeholder – to be implemented in a later chunk
# ──────────────────────────────────────────────────────────────────────────────
class S3Storage(StorageBackend):  # pragma: no cover
    \"\"\"*Not implemented* – stub for future migration.\"\"\"

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
"""
write("src/storymaker/data/storage.py", storage_py)


# ──────────────────────────────────────────────────────────────────────────────
# 2.  auth/auth.py  – basic password hashing + JWT & decorator
# ──────────────────────────────────────────────────────────────────────────────
auth_py = r"""
# Copyright © 2025 by Nick Jenkins. All rights reserved
"""
auth_py += """
\"\"\"Authentication utilities (MVP).

Features added in *Chunk 2*:

1. **Password hashing** – deterministic SHA-256 + salt.
2. **JWT access tokens** – `create_access_token()` / `decode_access_token()`.
3. **`login_required` decorator** for Flask routes.

These helpers stay intentionally *minimal* until we wire proper OAuth.
\"\"\"

from __future__ import annotations

import datetime as _dt
import hashlib
import hmac
import logging
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Final

import jwt
from flask import abort, g, request

from storymaker.config import settings
from storymaker.data.storage import LocalStorage
from storymaker.logging_config import configure_logging

configure_logging()
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# MVP in-memory user (kept for dev convenience)
# ---------------------------------------------------------------------------
@dataclass
class DevUser:
    id: str
    email: str
    display_name: str
    password_hash: str = "<dev>"


DEV_USER = DevUser(id="0000", email="dev@local", display_name="Dev User")

# ---------------------------------------------------------------------------
# Password hashing (deterministic SHA-256 + pepper)
# ---------------------------------------------------------------------------
_PEPPER: Final[bytes] = b"storymaker_pepper_v1"


def _hash_password(password: str, salt: str) -> str:
    \"\"\"Return PBKDF2-like hash → hex digest.

    Not for production use – *good enough* for MVP until Firebase/Auth0.
    \"\"\"
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), (salt + _PEPPER.decode()).encode(), 100_000)
    return dk.hex()


def verify_password(password: str, salt: str, hashed: str) -> bool:
    return hmac.compare_digest(_hash_password(password, salt), hashed)


# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------
JWT_ALGO: Final[str] = "HS256"


def create_access_token(user_id: str, expires: _dt.timedelta | None = None) -> str:
    expires = expires or _dt.timedelta(hours=2)
    payload = {
        "sub": user_id,
        "exp": _dt.datetime.utcnow() + expires,
        "iat": _dt.datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=JWT_ALGO)
    log.debug("Issued JWT for %s (exp %s)", user_id, payload["exp"])
    return token


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[JWT_ALGO])
        return payload
    except jwt.ExpiredSignatureError:  # noqa: PERF203
        abort(401, description="Token expired")
    except jwt.InvalidTokenError as e:  # noqa: BLE001
        log.warning("Invalid JWT: %s", e)
        abort(401, description="Invalid token")


# ---------------------------------------------------------------------------
# Flask decorator
# ---------------------------------------------------------------------------
_storage = LocalStorage()


def login_required(fn: Callable) -> Callable:
    \"\"\"Guard Flask route – expects **Bearer <JWT>** header.\"\"\"

    @wraps(fn)
    def wrapper(*args, **kwargs):  # type: ignore[override]
        auth_header = request.headers.get("Authorization", "")
        token = ""
        if auth_header.startswith("Bearer "):
            token = auth_header.removeprefix("Bearer ").strip()
        elif auth_header == "DEV":  # fallback – local dev, no auth
            g.user = DEV_USER
            return fn(*args, **kwargs)

        if not token:
            abort(401, description="Missing bearer token")

        payload = decode_access_token(token)
        user_id = payload["sub"]
        try:
            user = _storage.load_user(user_id)
        except FileNotFoundError:
            abort(401, description="User not found")

        g.user = user  # type: ignore
        return fn(*args, **kwargs)

    return wrapper
"""
write("src/storymaker/auth/auth.py", auth_py)


# ──────────────────────────────────────────────────────────────────────────────
# 3.  tests – quick regression checks
# ──────────────────────────────────────────────────────────────────────────────
test_storage = """
import tempfile
from pathlib import Path

from storymaker.data.storage import LocalStorage
from storymaker.models.book import Book
from storymaker.models.character import Character
from storymaker.models.chapter import Chapter


def _dummy_book() -> Book:
    return Book(
        id="b1",
        name="Test Book",
        description="desc",
        main_character=Character(name="Plushie"),
        chapters=[Chapter(chapter=1, title="T", scene="S", key_visual="K")],
    )


def test_save_load_book_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        store = LocalStorage(base_dir=Path(tmp))
        b = _dummy_book()
        store.save_book(b)
        loaded = store.load_book(b.id)
        assert loaded.id == b.id
        assert loaded.main_character.name == "Plushie"
"""
write("tests/test_storage.py", test_storage)

test_auth = """
from storymaker.auth.auth import create_access_token, decode_access_token


def test_jwt_roundtrip():
    token = create_access_token("user123")
    payload = decode_access_token(token)
    assert payload["sub"] == "user123"
"""
write("tests/test_auth.py", test_auth)


# ──────────────────────────────────────────────────────────────────────────────
print("\\nAll Chunk 2 assets generated successfully ✅")
