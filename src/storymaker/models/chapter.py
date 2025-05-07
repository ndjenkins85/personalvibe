# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Domain model: **Chapter** (one page/scene in the final book)."""

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
    image_path: Path | None = Field(default=None, description="Location of the rendered chapter image.")

    # ---------------------------- Helpers ---------------------------
    @property
    def safe_filename(self) -> str:
        """Sanitised filename used when storing rendered images."""
        safe_title = re.sub(r"[^a-zA-Z0-9]+", "_", self.title).strip("_")
        return f"{self.chapter:02d}_{safe_title}.png"

    # ---------------------------- Validators ------------------------
    @validator("image_path", pre=True, always=True)
    def _to_path(cls, v):
        return Path(v) if v else None
