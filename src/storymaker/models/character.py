# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Domain model: **Character**.

Represents any protagonist or side-character that can appear in a
Storymaker book (adult, child, or plush toy).
"""

from __future__ import annotations

import datetime as _dt
import enum
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Union
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, validator


def _parse_date(value: str) -> datetime:
    try:
        return parsedate_to_datetime(value)
    except Exception:
        return value  # fallback for regular pydantic parsing


class CharacterType(str, enum.Enum):
    ADULT = "adult"
    CHILD = "child"
    TOY = "toy"


class Character(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., min_length=1, max_length=50)
    type: CharacterType = CharacterType.TOY
    description: str = Field("", max_length=1_000)
    avatar_path: Union[Path, None] = Field(default=None, description="Path on disk to the latest avatar image.")
    created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)

    # ---------------------------- Validators -------------------------
    @validator("avatar_path", pre=True, always=True)
    def _expand_home(cls, v):
        return Path(v).expanduser() if v else None

    @field_validator("created_at", mode="before")
    def _flexible_date(cls, v):
        if isinstance(v, str) and "GMT" in v:
            return _parse_date(v)
        return v
