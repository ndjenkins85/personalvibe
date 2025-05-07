#!/usr/bin/env python3
# Copyright © 2025 by Nick Jenkins. All rights reserved

"""
bootstrap_storymaker.py

One-shot bootstrapper that lays down the **entire** Storymaker skeleton—
folders, README stubs, and Python modules with descriptive docstrings.

Running it once is idempotent: existing files are left untouched
(to avoid clobbering manual edits), while missing pieces are created.

Usage
-----
$ python bootstrap_storymaker.py

Why a Python bootstrapper instead of a plain bash script?
--------------------------------------------------------
1. Cross-platform (Windows devs can run it, too).
2. Allows richer logic—e.g., “create only if absent”, write multi-line
   docstrings, etc.
3. Easier future extension (templating, interactive questions, …).

The generated layout intentionally mirrors the Code Style Guide
principles supplied in the PRD—small, composable modules with
README breadcrumbs for both humans and AI copilots.
"""
from __future__ import annotations

import datetime
import json
import sys
import textwrap
from pathlib import Path

################################################################################
# Helper utilities
################################################################################


def mkdir(path: Path) -> None:
    """Create a directory (recursively) if it doesn’t already exist."""
    path.mkdir(parents=True, exist_ok=True)


def touch(path: Path, content: str = "") -> None:
    """Create `path` and write `content` **only if the file is absent**."""
    if path.exists():
        return
    path.write_text(textwrap.dedent(content).lstrip())


def timestamp() -> str:
    """Return ISO 8601 timestamp (UTC)."""
    return datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"


################################################################################
# 1. Folders to create
################################################################################

FOLDERS: dict[str, str] = {
    # fmt: off
    "src/storymaker":               "Top-level Storymaker Python package.  Business logic lives here.",
    "src/storymaker/api":           "Flask API layer—exposes HTTP routes consumed by the SPA frontend.",
    "src/storymaker/auth":          "Tiny auth/login helpers (placeholder; to be swapped for real OAuth later).",
    "src/storymaker/data":          "Thin I/O wrappers around the local filesystem → eventual plug-and-play cloud backends.",
    "src/storymaker/models":        "Pydantic domain models (Book, Chapter, User, Character…).",
    "src/storymaker/web":           "Server-rendered pages & SPA bootstrapping glue.",
    "src/storymaker/web/templates": "Jinja2 templates (fallback / SSR paths).",
    "src/storymaker/web/static":    "Bundled frontend assets—output of Vite/React build goes here.",
    "src/personalvibe":             "Shared utilities reused by multiple hobby projects (importable as `personalvibe`).",
    "prompts/storymaker":           "Prompt engineering templates that instruct the LLM for story & image generation.",
    "data/storymaker":              "On-disk storage for generated books, images, and user uploads (dev-only).",
    "tests":                        "Pytest suites mirroring `src/` layout.",
    # fmt: on
}

################################################################################
# 2. Files to create  (path -> contents)
################################################################################

FILES: dict[str, str] = {
    # ======================================================================
    # ── Package initialisers ───────────────────────────────────────────────
    # ======================================================================
    "src/storymaker/__init__.py": """
        \"\"\"Storymaker package bootstrap.

        Exposes:
            __version__: Semantic version string.
            get_version(): Helper returning the same string (import safety).

        Note
        ----
        The real version source of truth will be managed by *poetry* and
        surfaced here at build-time via `poetry-dynamic-versioning` or a
        similar plugin.  For now, we hard-code *0.1.0*.
        \"\"\"

        __version__ = "0.1.0"

        def get_version() -> str:
            \"\"\"Return package version (semantic).\"\"\"
            return __version__
        """,
    # ----------------------------------------------------------------------
    "src/storymaker/config.py": """
        \"\"\"Centralised runtime configuration powered by **Pydantic**.

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
        \"\"\"
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
        """,
    # ----------------------------------------------------------------------
    "src/storymaker/logging_config.py": """
        \"\"\"Opinionated **structured logging** configuration.

        Follows the _Observability by Default_ principle from the style guide.
        The function `configure_logging()` is idempotent and safe to call
        multiple times (first call wins).
        \"\"\"

        import logging
        import logging.config
        from __future__ import annotations

        _LOGGING_DICT = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "concise": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "concise",
                }
            },
            "root": {"level": "INFO", "handlers": ["console"]},
        }


        _configured = False


        def configure_logging() -> None:
            \"\"\"Wire `logging` with the pre-defined YAML-equivalent dict.\"\"\"
            global _configured
            if _configured:
                return
            logging.config.dictConfig(_LOGGING_DICT)
            _configured = True
        """,
    # ----------------------------------------------------------------------
    "src/storymaker/models/book.py": """
        \"\"\"Domain models: **Book**, **Chapter**, **Character**, **User**.

        These pure-data Pydantic models form the contract between:
        * API layer ⇄ SPA
        * Storage layer ⇄ business logic
        * LLM prompt builder ⇄ generation pipelines
        \"\"\"
        from __future__ import annotations
        from pathlib import Path
        from typing import List
        from pydantic import BaseModel, Field, HttpUrl
        import datetime as _dt

        class Character(BaseModel):
            name: str
            type: str = Field(regex="^(adult|child|toy)$")
            description: str
            avatar_path: Path | None = None


        class Chapter(BaseModel):
            chapter: int
            title: str
            scene: str
            key_visual: str
            caption: str | None = None
            image_path: Path | None = None


        class Book(BaseModel):
            id: str
            created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)
            name: str
            description: str
            main_character: Character
            side_characters: List[Character]
            chapters: List[Chapter]

            @property
            def cover_image(self) -> Path | None:  # noqa: D401
                \"\"\"Return path to chapter 1 image if present.\"\"\"
                return self.chapters[0].image_path if self.chapters else None
        """,
    # ----------------------------------------------------------------------
    "src/storymaker/data/storage.py": """
        \"\"\"Filesystem storage backend.

        Abstracts CRUD operations so future migrations (e.g. S3, Firestore)
        require only swapping this module—business logic remains untouched.
        \"\"\"
        from __future__ import annotations
        import json
        from pathlib import Path
        from typing import Any
        from storymaker.config import settings
        from storymaker.models.book import Book
        from storymaker.logging_config import configure_logging
        import logging

        configure_logging()
        log = logging.getLogger(__name__)


        class LocalStorage:
            \"\"\"Disk-based storage under `settings.data_dir`.\"\"\"

            def __init__(self, base_dir: Path | None = None) -> None:
                self.base_dir = base_dir or settings.data_dir
                self.base_dir.mkdir(parents=True, exist_ok=True)
                log.info("LocalStorage initialised at %s", self.base_dir.resolve())

            # -----------------------------------------------------------------
            # Book persistence
            # -----------------------------------------------------------------
            def save_book(self, book: Book) -> Path:
                \"\"\"Serialise `Book` → JSON on disk and return the file path.\"\"\"
                path = self.base_dir / f\"{book.id}.json\"
                path.write_text(book.json(indent=2, ensure_ascii=False))
                log.info("Saved book %s (%s bytes)", book.id, path.stat().st_size)
                return path

            def load_book(self, book_id: str) -> Book:
                path = self.base_dir / f\"{book_id}.json\"
                data: dict[str, Any] = json.loads(path.read_text())
                return Book(**data)
        """,
    # ----------------------------------------------------------------------
    "src/storymaker/api/app.py": """
        \"\"\"Flask **application factory**.

        The outer `create_app()` keeps tests clean and allows multiple app
        instances if needed (e.g. celery workers importing business logic).
        \"\"\"
        from __future__ import annotations
        from flask import Flask
        from storymaker.api.routes import register_routes
        from storymaker.config import settings
        from storymaker.logging_config import configure_logging

        def create_app() -> Flask:
            configure_logging()
            app = Flask(__name__)
            app.config["SECRET_KEY"] = settings.secret_key

            # Blueprints / route registration
            register_routes(app)

            return app


        # ── CLI entry-point (python -m storymaker.api.app) ──────────────────
        if __name__ == "__main__":  # pragma: no cover
            app = create_app()
            app.run(debug=settings.debug, port=8777)
        """,
    # ----------------------------------------------------------------------
    "src/storymaker/api/routes.py": """
        \"\"\"HTTP routes grouped by SPA pages.

        We expose **JSON APIs** consumed by the React / Vue front-end rather
        than serving full HTML (the latter lives in `web/templates` mostly
        for SSR fallback).
        \"\"\"
        from __future__ import annotations
        from flask import Flask, jsonify, request, abort
        from uuid import uuid4
        from storymaker.data.storage import LocalStorage
        from storymaker.models.book import Book
        from storymaker.logging_config import configure_logging
        import logging

        configure_logging()
        log = logging.getLogger(__name__)
        storage = LocalStorage()


        def register_routes(app: Flask) -> None:
            # -----------------------------------------------------------------
            # Index / health
            # -----------------------------------------------------------------
            @app.route("/api/health", methods=["GET"])
            def health():
                return jsonify(status="ok", time=request.environ.get("werkzeug.request").start_time)

            # -----------------------------------------------------------------
            # Books
            # -----------------------------------------------------------------
            @app.route("/api/books", methods=["POST"])
            def create_book():
                payload = request.get_json(force=True, silent=True)
                if not payload:
                    abort(400, "JSON body required")

                # VERY simplified—assumes valid payload
                book_id = str(uuid4())
                payload["id"] = book_id
                book = Book(**payload)
                storage.save_book(book)
                return jsonify(status="ok", data={"book_id": book_id})

            @app.route("/api/books/<book_id>", methods=["GET"])
            def get_book(book_id: str):
                book = storage.load_book(book_id)
                return jsonify(status="ok", data=book.dict())
        """,
    # ----------------------------------------------------------------------
    "src/storymaker/auth/auth.py": """
        \"\"\"Placeholder auth system.

        For the MVP we rely on signed cookies and a single hard-coded user.
        Swap with proper OAuth or Firebase once the rest of the platform
        stabilises.
        \"\"\"
        from dataclasses import dataclass

        @dataclass
        class User:
            id: str
            email: str
            display_name: str

        # Global dev user
        DEV_USER = User(id="0000", email="dev@local", display_name="Dev User")
        """,
    # ----------------------------------------------------------------------
    "src/storymaker/web/__init__.py": "# Empty namespace package for web helpers\n",
    # ----------------------------------------------------------------------
    "src/personalvibe/__init__.py": """
        \"\"\"Personalvibe mega-project namespace.

        This sub-package is intentionally left minimal—actual shared
        utilities will be added organically as Storymaker evolves.
        \"\"\"
        """,
    # ======================================================================
    # ── Prompt templates ───────────────────────────────────────────────────
    # ======================================================================
    "prompts/storymaker/generate_story.md": """
        <!--
        Storymaker prompt template: Generate a full 10-chapter CSV story.

        Filled-in dynamically by backend with:
          * {specific_story_prompt}
          * {story_character_information}
        -->
        """,
    # ----------------------------------------------------------------------
    "prompts/storymaker/generate_chapter.md": """
        <!--
        Storymaker prompt template: Generate a *single* chapter image.

        Placeholders:
          * {generate_chapter}
          * {whole_story}
          * {story_character_information}
        -->
        """,
    # ----------------------------------------------------------------------
    "prompts/storymaker/chiki.md": """
        <!-- Centralised character sheet for *Chiki* (sample) -->
        """,
    # ======================================================================
    # ── Misc project config ────────────────────────────────────────────────
    # ======================================================================
    "pyproject.toml": f"""
        [tool.poetry]
        name = "storymaker"
        version = "0.1.0"
        description = "Automated children’s book generator (LLM + image synthesis)."
        authors = ["You <you@example.com>"]
        readme = "README.md"
        packages = [{{ include = "src" }}]

        [tool.poetry.dependencies]
        python = "^3.10"
        flask = "^2.3"
        pydantic = "^2.0"
        requests = "^2.31"
        tenacity = "^8.2"
        python-dotenv = "^1.0"
        tqdm = "^4.66"

        [tool.poetry.group.dev.dependencies]
        black = "^24.3"
        isort = "^5.12"
        ruff = "^0.2"
        pytest = "^8.0"

        [build-system]
        requires = ["poetry-core"]
        build-backend = "poetry.core.masonry.api"
        """,
    # ======================================================================
    # ── Doc roots ──────────────────────────────────────────────────────────
    # ======================================================================
    "README.md": """
        # Storymaker

        Hobby project that spins up a *complete* children’s book pipeline:
        prompt engineering → ChatGPT narrative → DALL·E / GPT-Vision images →
        SPA bookshelf.

        This repository was initialised programmatically on {ts}.
        """.format(
        ts=timestamp()
    ),
    # ----------------------------------------------------------------------
    "tests/__init__.py": "# Root pytest namespace\n",
}

################################################################################
# 3. Create everything
################################################################################


def main() -> None:
    print(f"🛠  Bootstrapping Storymaker at {timestamp()}")
    # 1. Folders
    for folder, readme_text in FOLDERS.items():
        path = Path(folder)
        mkdir(path)
        touch(path / "_README.md", f"# {path.name}\n\n{readme_text}\n")
        print(f"  📁 {path}/")

    # 2. Files
    for file_path, content in FILES.items():
        path = Path(file_path)
        mkdir(path.parent)
        touch(path, content)
        print(f"  📄 {path}")

    print("\n✅  Done.  Activate your venv & run `poetry install` to get started!")


if __name__ == "__main__":
    main()
