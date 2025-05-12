# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Unit-tests for per-semver logging contract."""

import time
from pathlib import Path

import pytest

from personalvibe import logger as _logger


# ------------------------------------------------------------------ #
# Fixtures
# ------------------------------------------------------------------ #
@pytest.fixture(autouse=True)
def _reset_logging():
    """Ensure a clean logging env before & after each test."""
    _logger.reset_logging()
    yield
    _logger.reset_logging()


# ------------------------------------------------------------------ #
# Tests
# ------------------------------------------------------------------ #
def test_logfile_created(tmp_path: Path):
    run_id = "0.0.1_base"
    log_dir = tmp_path / "logs"
    _logger.configure_logging("none", run_id=run_id, log_dir=log_dir)

    lf = log_dir / f"{run_id}.log"
    assert lf.exists(), "log file not created"

    lines = lf.read_text().splitlines()
    assert lines[0] == f"RUN_ID={run_id}"
    assert lines[1].startswith("BEGIN-STAMP ")

    # Second init should only append *one* more BEGIN-STAMP
    _logger.reset_logging()
    _logger.configure_logging("none", run_id=run_id, log_dir=log_dir)

    lines2 = lf.read_text().splitlines()
    begin_count = [ln for ln in lines2 if ln.startswith("BEGIN-STAMP")]
    assert len(begin_count) == 2, "expected two BEGIN-STAMP entries"
    # RUN_ID header must remain singular / first line
    assert lines2[0] == f"RUN_ID={run_id}"
