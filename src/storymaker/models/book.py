# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Domain aggregate: **Book**.

A book is the top-level artefact containing metadata, characters, and
up to 10 chapters (scenes).  It is serialisable to JSON for storage
and is the primary object exchanged between backend & frontend.
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field, field_validator, model_validator

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
    chapters: List[Chapter] = Field(default_factory=list, description="Front page + 10 scenes + back page")

    # ---------------------------- Validators ------------------------
    @model_validator(mode="after")
    def _validate_chapters(self):
        """Ensure chapter numbers are unique & sequential."""
        chapter_nums = [c.chapter for c in self.chapters]
        if chapter_nums != sorted(set(chapter_nums)):
            raise ValueError("Chapter numbers must be unique and sorted ascending.")
        return self

    @field_validator("side_characters")
    def _limit_side_chars(cls, v, info):
        main: Character | None = info.data.get("main_character")
        if main and any(c.type == c.type.TOY and c.name == main.name for c in v):
            raise ValueError("Side characters cannot duplicate the main character.")
        return v

    # ---------------------------- Helpers --------------------------
    @property
    def cover_image(self) -> Path | None:
        """Return path to chapter 1 image if present."""
        if not self.chapters:
            return None
        return self.chapters[0].image_path

    @property
    def page_count(self) -> int:
        return len(self.chapters)

    def dict(self, **kwargs):
        """Override to ensure Path serialises to string."""
        out = super().dict(**kwargs)
        if (img := out.get("cover_image")) is not None:
            out["cover_image"] = str(img)
        return out
