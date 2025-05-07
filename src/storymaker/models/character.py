# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Domain model: **Character**.

Represents any protagonist or side-character that can appear in a
Storymaker book (adult, child, or plush toy).
"""

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
    avatar_path: Path | None = Field(default=None, description="Path on disk to the latest avatar image.")
    created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)

    # ---------------------------- Validators -------------------------
    @validator("avatar_path", pre=True, always=True)
    def _expand_home(cls, v):
        return Path(v).expanduser() if v else None
