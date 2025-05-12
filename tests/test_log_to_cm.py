# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Tests for the revised noxfile._log_to context-manager."""

import importlib
import tempfile
from pathlib import Path

import noxfile  # type: ignore


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def test_log_to_appends_twice(tmp_path: Path):
    log_file = tmp_path / "sample.log"

    # First write
    with noxfile._log_to(log_file):  # type: ignore[attr-defined]
        print("hello world")

    first = _read(log_file)
    assert "hello world" in first
    size_after_first = log_file.stat().st_size

    # Second write
    with noxfile._log_to(log_file):  # type: ignore[attr-defined]
        print("second time!")

    second = _read(log_file)
    assert "second time!" in second
    # File grew, not overwritten
    assert log_file.stat().st_size > size_after_first
