# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/storymaker/stages/03_bootstrap_chunk1.py
"""
Executable helper to **apply Chunk 1 – Domain & Config** to the Storymaker
code-base.  Run once from anywhere inside the repo:

    $ python chunk1_domain_config.py

The script will:

1. Locate the repository root with `vibe_utils.get_base_path()`.
2. Create / overwrite the files that belong to the “Domain & Config” layer:
       • src/storymaker/config.py
       • src/storymaker/models/{__init__,character,chapter,book,user}.py
3. Leave all other folders untouched.

It is idempotent—re-running will just re-write the same contents.
"""

from __future__ import annotations

import textwrap
from pathlib import Path
from uuid import uuid4

from personalvibe import vibe_utils

# ──────────────────────────────────────────────────────────────────────────
# 1.  Resolve repo root & convenience helpers
# ──────────────────────────────────────────────────────────────────────────
REPO = vibe_utils.get_base_path()  # e.g.  /home/me/projects/personalvibe
SRC = REPO / "src"
STORYMAKER = SRC / "storymaker"
MODELS = STORYMAKER / "models"

MODELS.mkdir(parents=True, exist_ok=True)


# Generic file-writer
def write(rel_path: str, code: str) -> None:
    abs_path = REPO / rel_path
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    abs_path.write_text(textwrap.dedent(code).lstrip())
    print(f"[chunk1] wrote {abs_path.relative_to(REPO)}")


# ──────────────────────────────────────────────────────────────────────────
# 2.  storymaker/config.py  (expanded Settings)
# ──────────────────────────────────────────────────────────────────────────
write(
    "src/storymaker/config.py",
    """
    # Copyright © 2025 by Nick Jenkins. All rights reserved
    \"\"\"Runtime configuration singleton for **Storymaker**.

    The class `Settings` is a thin Pydantic wrapper around environment
    variables and sensible fall-backs.  Import the *instance* named
    `settings` from anywhere in the code-base:

        >>> from storymaker.config import settings
        >>> settings.data_dir.mkdir(exist_ok=True)

    New fields can be added in later chunks—unit tests catch regressions.
    \"\"\"

    import os
    import secrets
    from pathlib import Path
    from typing import List

    from pydantic import BaseSettings, Field, HttpUrl, validator


    class Settings(BaseSettings):
        # -----------------------------------------------------------------
        # Core paths
        # -----------------------------------------------------------------
        repo_root: Path = Field(
            default_factory=lambda: Path(__file__).resolve().parents[2],
            description="Absolute path to the git repository root.",
        )
        data_dir: Path = Field(
            default=Path("data/storymaker"),
            description="Root folder for all user-generated artefacts.",
        )

        # -----------------------------------------------------------------
        # Flask / API
        # -----------------------------------------------------------------
        secret_key: str = Field(
            default_factory=lambda: secrets.token_urlsafe(32),
            description="Flask session & JWT signing key.",
        )
        debug: bool = Field(
            default=True,
            description="Enable verbose logging & hot-reload in local dev.",
        )
        api_base_url: HttpUrl = Field(
            default="http://localhost:8777",
            description="Public URL where the Flask API is reachable.",
        )
        spa_base_url: HttpUrl = Field(
            default="http://localhost:5173",
            description="Public URL where the Vite/React SPA is served.",
        )
        allowed_origins: List[str] = Field(
            default=["http://localhost:5173"],
            description="CORS allow-list consumed by Flask-CORS.",
        )

        # -----------------------------------------------------------------
        # 3rd-party APIs
        # -----------------------------------------------------------------
        openai_api_key: str | None = Field(
            default=None,
            description="Pulled from OPENAI_API_KEY env var automatically.",
        )

        # -----------------------------------------------------------------
        # Misc feature flags & limits
        # -----------------------------------------------------------------
        rate_limit_per_minute: int = Field(
            default=60,
            description="Simple in-memory rate-limit for unauthenticated users.",
        )

        # -----------------------------------------------------------------
        # Validators
        # -----------------------------------------------------------------
        @validator("openai_api_key", pre=True, always=True)
        def _load_openai_key(cls, v: str | None) -> str | None:
            return v or os.getenv("OPENAI_API_KEY")

        class Config:
            env_prefix = "STORYMAKER_"
            case_sensitive = False


    # Singleton—import anywhere
    settings = Settings()
    """,
)

# ──────────────────────────────────────────────────────────────────────────
# 3.  storymaker/models/character.py
# ──────────────────────────────────────────────────────────────────────────
write(
    "src/storymaker/models/character.py",
    """
    \"\"\"Domain model: **Character**.

    Represents any protagonist or side-character that can appear in a
    Storymaker book (adult, child, or plush toy).
    \"\"\"

    from __future__ import annotations

    import datetime as _dt
    import enum
    from pathlib import Path
    from uuid import uuid4

    from pydantic import BaseModel, Field, validator


    class CharacterType(str, enum.Enum):
        ADULT = "adult"
        CHILD = "child"
        TOY = "toy"


    class Character(BaseModel):
        id: str = Field(default_factory=lambda: str(uuid4()))
        name: str = Field(..., min_length=1, max_length=50)
        type: CharacterType = CharacterType.TOY
        description: str = Field("", max_length=1_000)
        avatar_path: Path | None = Field(
            default=None, description="Path on disk to the latest avatar image."
        )
        created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)

        # ---------------------------- Validators -------------------------
        @validator("avatar_path", pre=True, always=True)
        def _expand_home(cls, v):
            return Path(v).expanduser() if v else None
    """,
)

# ──────────────────────────────────────────────────────────────────────────
# 4.  storymaker/models/chapter.py
# ──────────────────────────────────────────────────────────────────────────
write(
    "src/storymaker/models/chapter.py",
    """
    \"\"\"Domain model: **Chapter** (one page/scene in the final book).\"\"\"

    from __future__ import annotations

    import re
    from pathlib import Path

    from pydantic import BaseModel, Field, validator


    class Chapter(BaseModel):
        chapter: int = Field(..., ge=1, le=10)
        title: str = Field(..., max_length=50)
        scene: str = Field(..., max_length=300)
        key_visual: str = Field(..., max_length=300)
        caption: str | None = Field(default=None, max_length=120)
        image_path: Path | None = Field(
            default=None, description="Location of the rendered chapter image."
        )

        # ---------------------------- Helpers ---------------------------
        @property
        def safe_filename(self) -> str:
            \"\"\"Sanitised filename used when storing rendered images.\"\"\"
            safe_title = re.sub(r"[^a-zA-Z0-9]+", "_", self.title).strip("_")
            return f"{self.chapter:02d}_{safe_title}.png"

        # ---------------------------- Validators ------------------------
        @validator("image_path", pre=True, always=True)
        def _to_path(cls, v):
            return Path(v) if v else None
    """,
)

# ──────────────────────────────────────────────────────────────────────────
# 5.  storymaker/models/user.py
# ──────────────────────────────────────────────────────────────────────────
write(
    "src/storymaker/models/user.py",
    """
    \"\"\"Domain model: **User** (registered account).\"\"\"

    from __future__ import annotations

    import datetime as _dt
    from pathlib import Path
    from uuid import uuid4

    from pydantic import BaseModel, EmailStr, Field


    class User(BaseModel):
        id: str = Field(default_factory=lambda: str(uuid4()))
        email: EmailStr
        display_name: str = Field(..., min_length=1, max_length=50)
        avatar_path: Path | None = None
        created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)
        is_active: bool = True

        # ---------------------------- Computed -------------------------
        @property
        def initials(self) -> str:
            \"\"\"Return *DJ* for *Dev Jenkins* etc.\"\"\"
            return "".join(p[0] for p in self.display_name.split()[:2]).upper()
    """,
)

# ──────────────────────────────────────────────────────────────────────────
# 6.  storymaker/models/book.py  (imports new components)
# ──────────────────────────────────────────────────────────────────────────
write(
    "src/storymaker/models/book.py",
    """
    \"\"\"Domain aggregate: **Book**.

    A book is the top-level artefact containing metadata, characters, and
    up to 10 chapters (scenes).  It is serialisable to JSON for storage
    and is the primary object exchanged between backend & frontend.
    \"\"\"

    from __future__ import annotations

    import datetime as _dt
    from pathlib import Path
    from typing import List

    from pydantic import BaseModel, Field, root_validator, validator

    from storymaker.models.chapter import Chapter
    from storymaker.models.character import Character


    class Book(BaseModel):
        id: str
        name: str = Field(..., min_length=1, max_length=80)
        description: str = Field(..., max_length=400)
        created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)

        # Characters
        main_character: Character
        side_characters: List[Character] = Field(default_factory=list)

        # Content
        chapters: List[Chapter] = Field(
            default_factory=list, description="Front page + 10 scenes + back page"
        )

        # ---------------------------- Validators ------------------------
        @root_validator
        def _validate_chapters(cls, values):  # noqa: D401
            \"\"\"Ensure chapter numbers are unique & sequential.\"\"\"
            chapters: list[Chapter] = values.get("chapters", [])
            chapter_nums = [c.chapter for c in chapters]
            if chapter_nums != sorted(set(chapter_nums)):
                raise ValueError("Chapter numbers must be unique and sorted ascending.")
            return values

        @validator("side_characters", each_item=True)
        def _limit_side_chars(cls, v):
            if v.type == v.type.TOY and v.name == values.get("main_character").name:  # type: ignore
                raise ValueError("Side characters cannot duplicate the main character.")
            return v

        # ---------------------------- Helpers --------------------------
        @property
        def cover_image(self) -> Path | None:
            \"\"\"Return path to chapter 1 image if present.\"\"\"
            if not self.chapters:
                return None
            return self.chapters[0].image_path

        @property
        def page_count(self) -> int:
            return len(self.chapters)

        def dict(self, **kwargs):
            \"\"\"Override to ensure Path serialises to string.\"\"\"
            out = super().dict(**kwargs)
            if (img := out.get("cover_image")) is not None:
                out["cover_image"] = str(img)
            return out
    """,
)

# ──────────────────────────────────────────────────────────────────────────
# 7.  storymaker/models/__init__.py  (re-export public API)
# ──────────────────────────────────────────────────────────────────────────
write(
    "src/storymaker/models/__init__.py",
    """
    \"\"\"Aggregate exports for Storymaker domain models.\"\"\"

    from storymaker.models.book import Book
    from storymaker.models.chapter import Chapter
    from storymaker.models.character import Character, CharacterType
    from storymaker.models.user import User

    __all__ = [
        "Book",
        "Chapter",
        "Character",
        "CharacterType",
        "User",
    ]
    """,
)

print("\n[chunk1] 🎉  Domain & Config layer applied successfully!")
print(f"[chunk1] Repo root: {REPO}")
print("[chunk1] You can now run unit tests or start the Flask API.")
