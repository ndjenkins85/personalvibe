# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Flask **application factory**.

The outer `create_app()` keeps tests clean and allows multiple app
instances if needed (e.g. celery workers importing business logic).
"""

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
