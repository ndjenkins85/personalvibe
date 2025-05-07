# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Opinionated **structured logging** configuration.

Follows the _Observability by Default_ principle from the style guide.
The function `configure_logging()` is idempotent and safe to call
multiple times (first call wins).
"""

from __future__ import annotations

import logging
import logging.config

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
    """Wire `logging` with the pre-defined YAML-equivalent dict."""
    global _configured
    if _configured:
        return
    logging.config.dictConfig(_LOGGING_DICT)
    _configured = True
