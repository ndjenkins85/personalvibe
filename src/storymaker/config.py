# Copyright © 2025 by Nick Jenkins. All rights reserved
"""Runtime configuration singleton for **Storymaker**.

The class `Settings` is a thin Pydantic wrapper around environment
variables and sensible fall-backs.  Import the *instance* named
`settings` from anywhere in the code-base:

    >>> from storymaker.config import settings
    >>> settings.data_dir.mkdir(exist_ok=True)

New fields can be added in later chunks—unit tests catch regressions.
"""

import os
import secrets
from pathlib import Path
from typing import List, Union

from pydantic import Field, HttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # -----------------------------------------------------------------
    # Core paths
    # -----------------------------------------------------------------
    repo_root: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parents[2],
        description="Absolute path to the git repository root.",
    )
    data_dir: Path = Field(
        default=Path("data/storymaker"),
        description="Root folder for all user-generated artefacts.",
    )

    # -----------------------------------------------------------------
    # Flask / API
    # -----------------------------------------------------------------
    secret_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Flask session & JWT signing key.",
    )
    debug: bool = Field(
        default=True,
        description="Enable verbose logging & hot-reload in local dev.",
    )
    api_base_url: HttpUrl = Field(
        default="http://localhost:8777",
        description="Public URL where the Flask API is reachable.",
    )
    spa_base_url: HttpUrl = Field(
        default="http://localhost:5173",
        description="Public URL where the Vite/React SPA is served.",
    )
    allowed_origins: List[str] = Field(
        default=["http://localhost:5173"],
        description="CORS allow-list consumed by Flask-CORS.",
    )

    # -----------------------------------------------------------------
    # 3rd-party APIs
    # -----------------------------------------------------------------
    openai_api_key: Union[str, None] = Field(
        default=None,
        description="Pulled from OPENAI_API_KEY env var automatically.",
    )

    # -----------------------------------------------------------------
    # Misc feature flags & limits
    # -----------------------------------------------------------------
    rate_limit_per_minute: int = Field(
        default=60,
        description="Simple in-memory rate-limit for unauthenticated users.",
    )

    # -----------------------------------------------------------------
    # Validators
    # -----------------------------------------------------------------
    @validator("openai_api_key", pre=True, always=True)
    def _load_openai_key(cls, v: Union[str, None]) -> Union[str, None]:
        return v or os.getenv("OPENAI_API_KEY")

    class Config:
        env_prefix = "STORYMAKER_"
        case_sensitive = False


# Singleton—import anywhere
settings = Settings()
