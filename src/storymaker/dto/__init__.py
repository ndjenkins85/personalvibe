# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Storymaker DTO foundation.

Centralises shared envelopes & pagination helpers.  Import like:

    from storymaker.dto import ApiResponse, ErrorResponse, PaginationMeta
"""

from .response import ApiResponse, ErrorResponse, PaginationMeta

__all__ = [
    "ApiResponse",
    "ErrorResponse",
    "PaginationMeta",
]
