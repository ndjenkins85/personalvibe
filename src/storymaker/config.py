# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Centralised runtime configuration powered by **Pydantic**.

Environment variable precedence
-------------------------------
1. Explicit kwargs (rare; mainly unit tests)
2. `.env` file in project root
3. Hard-coded defaults below

The object is imported by every entry-point (Flask, CLI, notebooks)
to ensure **one single source of truth** for params such as:

* `data_dir`:       Where generated books & images live.
* `openai_api_key`: Pulled from env var; never committed.
* `debug`:          Toggles verbose logs & Flask reload.

Usage
-----
>>> from storymaker.config import settings
>>> print(settings.data_dir)
"""

import os
from pathlib import Path

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    # -----------------------------------------------------------------
    # Core paths
    # -----------------------------------------------------------------
    data_dir: Path = Field(
        default=Path("data/storymaker"),
        description="Root folder for all user-generated artefacts.",
    )

    # -----------------------------------------------------------------
    # API & auth
    # -----------------------------------------------------------------
    secret_key: str = Field(
        default="change-me-in-prod",
        description="Flask session & JWT signing key.",
    )
    openai_api_key: str | None = Field(
        default=None,
        description="Pulled from OPENAI_API_KEY env var automatically.",
    )

    # -----------------------------------------------------------------
    # Misc flags
    # -----------------------------------------------------------------
    debug: bool = Field(default=True, description="Enable verbose logging & hot reload.")

    # -----------------------------------------------------------------
    # Validators
    # -----------------------------------------------------------------
    @validator("openai_api_key", pre=True, always=True)
    def _load_openai_key(cls, v: str | None) -> str | None:
        return v or os.getenv("OPENAI_API_KEY")


# Singleton instance (import from anywhere)
settings = Settings()
