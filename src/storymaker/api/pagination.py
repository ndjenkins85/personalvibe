# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Minimal **offset-based** pagination helper."""

from __future__ import annotations

from math import ceil
from typing import Any, List, Tuple


def paginate(items: List[Any], page: int = 1, per_page: int = 20) -> Tuple[list, dict]:
    """Return `(slice, meta)`.

    Args:
        items: Full data set (already materialised).
        page: 1-based page index.
        per_page: Items per page.

    Returns:
        slice_: Items for the requested page.
        meta: Dict with pagination meta suitable for API response.
    """
    total = len(items)
    page = max(page, 1)
    per_page = max(1, per_page)
    start = (page - 1) * per_page
    end = start + per_page
    return (
        items[start:end],
        {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": ceil(total / per_page) if per_page else 1,
        },
    )
