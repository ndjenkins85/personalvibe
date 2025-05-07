# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Pydantic **DTO** layer – clean boundary between HTTP & domain models."""

from __future__ import annotations

import datetime as _dt
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from storymaker.models.book import Book
from storymaker.models.character import Character


class BaseSchema(BaseModel):
    model_config = {
        "from_attributes": True,  # formerly orm_mode
        "populate_by_name": True,  # formerly allow_population_by_field_name
    }


# ─────────────────────────── Pagination ──────────────────────────────
class Pagination(BaseSchema):
    page: int
    per_page: int
    total: int


# ───────────────────────────── Books ─────────────────────────────────
class BookIn(BaseSchema):
    name: str = Field(..., min_length=1, max_length=80)
    description: str
    main_character: Character
    side_characters: List[Character] = []
    chapters: List = []  # Lightweight—client can PATCH later


class BookOut(BaseSchema):
    id: str
    name: str
    description: str
    created_at: _dt.datetime

    # Extra computed fields to make the SPA happy
    cover_image: Optional[str]
    page_count: int

    @classmethod
    def from_model(cls, book: Book) -> "BookOut":
        return cls(
            id=book.id,
            name=book.name,
            description=book.description,
            created_at=book.created_at,
            cover_image=str(book.cover_image) if book.cover_image else None,
            page_count=book.page_count,
        )


# ─────────────────────────── Characters ──────────────────────────────
class CharacterIn(Character):
    pass


class CharacterOut(Character):
    pass


# ──────────────────────────── Auth / Me ──────────────────────────────
class LoginRequest(BaseSchema):
    email: EmailStr
    password: str


class LoginResponse(BaseSchema):
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseSchema):
    id: str
    email: EmailStr
    display_name: str
