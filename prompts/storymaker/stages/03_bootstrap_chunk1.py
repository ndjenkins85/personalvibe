# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/storymaker/stages/03_bootstrap_chunk1.py
#!/usr/bin/env python
"""Bootstrap “Chunk 1 – Domain & Config”.

Run **once** from repository root::

    python bootstrap_chunk1.py

The script will:

• (Over)write Storymaker *domain* models
• Extend centralised `config.py` (dotenv + JWT defaults)
• Create an aggregate `models/__init__.py` for ergonomic imports

Sub-folders are created automatically; existing files are **replaced**
with the new, backwards-compatible versions.

Nothing outside *Domain & Config* is touched.
"""
from __future__ import annotations

import os
import textwrap
from pathlib import Path

from personalvibe import vibe_utils


def write(path: Path, content: str) -> None:
    """Idempotent helper that mkdirs & writes *dedented* text."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content))
    print(f"✓ wrote {path.relative_to(REPO)}")


# -----------------------------------------------------------------------------#
#  Locate repo root (assumes script lives anywhere under repo)
# -----------------------------------------------------------------------------#
REPO = os.chdir(vibe_utils.get_base_path())
# REPO = Path(__file__).resolve().parent
# while REPO.name not in {"storymaker", "personalvibe"} and REPO.parent != REPO:
#     REPO = REPO.parent
SRC = REPO / "src"

# -----------------------------------------------------------------------------#
#  1.  Expanded CONFIG
# -----------------------------------------------------------------------------#
config_py = SRC / "storymaker" / "config.py"
write(
    config_py,
    r"""
    # Copyright © 2025 by Nick Jenkins. All rights reserved
    """
    """
    Centralised runtime configuration powered by **Pydantic**.

    Priority order
    --------------
    1. Explicit keyword arguments (mainly unit tests)
    2. .env in project root  ← NEW
    3. Hard-coded defaults below

    Import the **singleton** `settings` from anywhere:

        from storymaker.config import settings
    """
    '''
    import os
    from pathlib import Path
    from typing import Any

    from dotenv import load_dotenv
    from pydantic import BaseSettings, Field, validator

    # Auto-load .env if present (silent =True avoids error if missing)
    load_dotenv(override=False)

    class Settings(BaseSettings):
        # ── Core paths ────────────────────────────────────────────────────
        data_dir: Path = Field(
            default=Path("data/storymaker"),
            description="Root folder for all user-generated artefacts.",
        )

        # ── API & auth ───────────────────────────────────────────────────
        secret_key: str = Field(
            default="change-me-in-prod",
            description="Flask session & JWT signing key.",
        )
        openai_api_key: str | None = Field(
            default=None,
            description="Pulled from OPENAI_API_KEY env var automatically.",
        )
        jwt_expiry_hours: int = Field(
            default=6,
            description="Default access-token lifetime (hours).",
        )

        # ── Misc flags ───────────────────────────────────────────────────
        debug: bool = Field(
            default=True,
            description="Enable verbose logging & hot reload in dev.",
        )

        # ── Validators ───────────────────────────────────────────────────
        @validator("openai_api_key", pre=True, always=True)
        def _load_openai_key(cls, v: str | None) -> str | None:  # noqa: N805
            return v or os.getenv("OPENAI_API_KEY")

        # ── Inner Config (pydantic) ──────────────────────────────────────
        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"

        # ── Convenience helpers ──────────────────────────────────────────
        def asdict(self) -> dict[str, Any]:
            """Return **serialisable** dict (Path → str)."""
            d = self.dict()
            d["data_dir"] = str(d["data_dir"])
            return d

    # Singleton – import from anywhere
    settings = Settings()
    ''',
)

# -----------------------------------------------------------------------------#
#  2.  DOMAIN MODELS
# -----------------------------------------------------------------------------#
models_package = SRC / "storymaker" / "models"

# ── 2.1  Character, Chapter, Book  (rewrite)───────────────────────────────
write(
    models_package / "book.py",
    r'''
    # Copyright © 2025 by Nick Jenkins. All rights reserved
    """Domain models – Book stack.

    These **pure-data** Pydantic models are the *contract* between:

        • API layer  ⇄  SPA frontend
        • Storage    ⇄  business logic
        • Prompt     ⇄  image / story generation pipelines
    """

    from __future__ import annotations

    import datetime as _dt
    from pathlib import Path
    from typing import List

    from pydantic import BaseModel, Field, HttpUrl, root_validator, validator

    # ------------------------------------------------------------------#
    # Character
    # ------------------------------------------------------------------#
    class Character(BaseModel):
        """A person / toy present in the story universe."""

        name: str
        type: str = Field(regex="^(adult|child|toy)$")
        description: str = Field(
            ...,
            description="Long-form, plain-English description used by LLM prompt.",
        )
        avatar_path: Path | None = None
        age: int | None = Field(
            default=None, ge=0, le=120, description="Optional helper for age-appropriate scenes."
        )
        avatar_url: HttpUrl | None = None  # Populated by API for SPA convenience

        @validator("name")
        def _strip(cls, v: str) -> str:  # noqa: N805
            return v.strip()

    # ------------------------------------------------------------------#
    # Chapter
    # ------------------------------------------------------------------#
    class Chapter(BaseModel):
        chapter: int = Field(ge=1, description="1-indexed position inside book.")
        title: str
        scene: str
        key_visual: str
        caption: str | None = None
        image_path: Path | None = None

        @property
        def is_cover(self) -> bool:  # noqa: D401
            """True for first chapter – used by gallery UI."""
            return self.chapter == 1

    # ------------------------------------------------------------------#
    # Book
    # ------------------------------------------------------------------#
    class Book(BaseModel):
        id: str
        created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)
        name: str
        description: str
        main_character: Character
        side_characters: List[Character] = Field(default_factory=list, max_items=5)
        chapters: List[Chapter] = Field(min_items=1, max_items=12)

        # ── Validators ────────────────────────────────────────────────
        @root_validator
        def _unique_chapter_numbers(cls, values):  # noqa: N805
            chapter_numbers = [c.chapter for c in values.get("chapters", [])]
            if len(chapter_numbers) != len(set(chapter_numbers)):
                raise ValueError("Duplicate chapter numbers are not allowed")
            return values

        # ── Computed helpers ──────────────────────────────────────────
        @property
        def cover_image(self) -> Path | None:  # noqa: D401
            """Return path of first chapter image (or *None*)."""
            return self.chapters[0].image_path if self.chapters else None

        def dict_for_api(self) -> dict:
            """Convert to dict with Path → str for JSON serialisation."""
            d = self.dict()
            for ch in d["chapters"]:
                if ch["image_path"]:
                    ch["image_path"] = str(ch["image_path"])
            if d["main_character"]["avatar_path"]:
                d["main_character"]["avatar_path"] = str(d["main_character"]["avatar_path"])
            return d
    ''',
)

# ── 2.2  User model ───────────────────────────────────────────────────────
write(
    models_package / "user.py",
    r'''
    """User account model (MVP – no OAuth yet)."""

    from __future__ import annotations

    import datetime as _dt
    from pathlib import Path

    from pydantic import BaseModel, EmailStr, Field


    class User(BaseModel):
        id: str
        email: EmailStr
        display_name: str
        hashed_password: str | None = None  # For future login upgrade
        created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)
        avatar_path: Path | None = None
        is_active: bool = True

        # Convenience
        @property
        def avatar_url(self) -> str | None:
            if self.avatar_path:
                return f"/static/avatars/{self.avatar_path.name}"
            return None
    ''',
)

# ── 2.3  AuthToken model ─────────────────────────────────────────────────
write(
    models_package / "token.py",
    r'''
    """Auth token (simple signed JWT wrapper, no refresh tokens yet)."""

    from __future__ import annotations

    import datetime as _dt

    from pydantic import BaseModel, Field


    class AuthToken(BaseModel):
        access_token: str
        token_type: str = Field(default="bearer", const=True)
        expires_at: _dt.datetime

        # Helpers
        def expired(self) -> bool:  # noqa: D401
            """Whether the token has *already* expired."""
            return _dt.datetime.utcnow() >= self.expires_at
    ''',
)

# ── 2.4  Aggregate `models/__init__.py` for ergonomic imports ────────────
write(
    models_package / "__init__.py",
    r'''
    """Convenience re-exports – import models like::

        from storymaker.models import Book, User
    """

    from .book import Book, Chapter, Character
    from .token import AuthToken
    from .user import User

    __all__ = ["Book", "Chapter", "Character", "User", "AuthToken"]
    ''',
)

print("\nDomain & Config bootstrap complete 🎉 – run `pytest` or start Flask!  ")
