# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Storymaker API namespace.

Exposes:
    • create_app ─ Flask application factory
    • All Pydantic DTOs under `schemas`
"""

from __future__ import annotations

from storymaker.api.app import create_app  # noqa: F401
