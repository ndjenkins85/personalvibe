# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Domain model: **User** (registered account)."""

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
        """Return *DJ* for *Dev Jenkins* etc."""
        return "".join(p[0] for p in self.display_name.split()[:2]).upper()
