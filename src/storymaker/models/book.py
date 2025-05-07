# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Domain models: **Book**, **Chapter**, **Character**, **User**.

These pure-data Pydantic models form the contract between:
* API layer ⇄ SPA
* Storage layer ⇄ business logic
* LLM prompt builder ⇄ generation pipelines
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field, HttpUrl


class Character(BaseModel):
    name: str
    type: str = Field(regex="^(adult|child|toy)$")
    description: str
    avatar_path: Path | None = None


class Chapter(BaseModel):
    chapter: int
    title: str
    scene: str
    key_visual: str
    caption: str | None = None
    image_path: Path | None = None


class Book(BaseModel):
    id: str
    created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)
    name: str
    description: str
    main_character: Character
    side_characters: List[Character]
    chapters: List[Chapter]

    @property
    def cover_image(self) -> Path | None:  # noqa: D401
        """Return path to chapter 1 image if present."""
        return self.chapters[0].image_path if self.chapters else None
