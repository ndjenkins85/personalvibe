# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Opinionated Structured Logging Configuration.

Follows the _Observability by Default_ principle.
Use `configure_logging()` once during app startup.
"""

import logging
import logging.config
import sys

_configured = False


class ColorFormatter(logging.Formatter):
    """Optional colorized formatter for console output."""

    COLORS = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[95m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


def configure_logging(verbosity: str = "none", color: bool = True) -> None:
    """Configure centralized logging. Call once at startup.

    Args:
        verbosity (str): 'verbose', 'none', or 'errors'
        color (bool): Enable colorized output for console logs
    """
    global _configured
    if _configured:
        return

    levels = {"verbose": logging.DEBUG, "none": logging.INFO, "errors": logging.ERROR}
    level = levels.get(verbosity, logging.INFO)

    formatter = (
        ColorFormatter(fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        if color
        else logging.Formatter(fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logging.root.setLevel(level)
    logging.root.handlers = []  # Clear existing handlers
    logging.root.addHandler(console_handler)

    _configured = True
