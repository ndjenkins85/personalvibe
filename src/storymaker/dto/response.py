# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Generic **API response** & pagination DTOs.

Motivation
----------
Storymaker’s Flask routes currently build ad-hoc JSON dictionaries
(`{"status": "ok", "data": …}`).  This module introduces *typed*
wrappers based on **Pydantic generics** so downstream consumers
– including the SPA’s type-generator – can rely on a single
contract.

Nothing in production imports these yet; future chunks will
migrate route handlers incrementally.

Usage
-----
    >>> from storymaker.dto import ApiResponse
    >>> payload = ApiResponse[int](data=42)
    >>> payload.model_dump()
    {'status': 'ok', 'data': 42, 'meta': None}

"""

from __future__ import annotations

import datetime as _dt
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field
from typing_extensions import Literal


# --------------------------------------------------------------------- #
# Shared helpers
# --------------------------------------------------------------------- #
class _BaseDTO(BaseModel):
    """Common Pydantic config – mirrors api.schemas.BaseSchema."""

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
    }


# --------------------------------------------------------------------- #
# Pagination
# --------------------------------------------------------------------- #
class PaginationMeta(_BaseDTO):
    """Offset-based pagination metadata (mirror of api.pagination)."""

    page: int = Field(1, ge=1, description="1-based page index")
    per_page: int = Field(20, ge=1, description="Requested page size")
    total: int = Field(..., ge=0, description="Total items across pages")
    pages: int = Field(..., ge=1, description="Total number of pages")


# --------------------------------------------------------------------- #
# Generic envelope
# --------------------------------------------------------------------- #
T = TypeVar("T")


class ApiResponse(_BaseDTO, Generic[T]):
    """Success envelope – default `status='ok'`.

    The `data` attribute is generic so the response can enforce
    shape, e.g. `ApiResponse[List[BookOut]]`.
    """

    status: Literal["ok"] = "ok"
    data: Optional[T] = Field(None, description="Payload for the caller")
    meta: Optional[Any] = Field(None, description="Optional metadata (e.g. pagination details)")
    ts: _dt.datetime = Field(
        default_factory=_dt.datetime.utcnow,
        description="Server timestamp – convenience for clients",
    )


# --------------------------------------------------------------------- #
# Error envelope (simple, non-generic)
# --------------------------------------------------------------------- #
class ErrorResponse(_BaseDTO):
    """Uniform error wrapper emitted by `storymaker.api.errors`."""

    status: Literal["error"] = "error"
    error: str = Field(..., description="Human readable error message")
    code: int = Field(..., description="HTTP status code")
    ts: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)
