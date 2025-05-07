# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Authentication utilities (MVP).

Features added in *Chunk 2*:

1. **Password hashing** – deterministic SHA-256 + salt.
2. **JWT access tokens** – `create_access_token()` / `decode_access_token()`.
3. **`login_required` decorator** for Flask routes.

These helpers stay intentionally *minimal* until we wire proper OAuth.
"""

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
    """Return PBKDF2-like hash → hex digest.

    Not for production use – *good enough* for MVP until Firebase/Auth0.
    """
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
    """Guard Flask route – expects **Bearer <JWT>** header."""

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
