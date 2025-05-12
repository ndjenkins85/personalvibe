# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Unit tests for the enhanced logging harness."""

from pathlib import Path

from personalvibe import logger


def test_logfile_created(tmp_path: Path) -> None:
    """configure_logging() must create <run_id>.log & stamp it."""
    run_id = "0.0.1_base"
    logger.reset_logging()
    logger.configure_logging("none", run_id=run_id, log_dir=tmp_path)

    log_file = tmp_path / f"{run_id}.log"
    assert log_file.exists(), "Log file should be created"

    lines = log_file.read_text().splitlines()
    assert lines[0] == f"RUN_ID={run_id}"
    assert lines[1].startswith("BEGIN-STAMP"), "Missing session stamp"
    logger.reset_logging()
