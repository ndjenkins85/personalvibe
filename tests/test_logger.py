# Copyright © 2025 by Nick Jenkins. All rights reserved

from pathlib import Path

from personalvibe import logger


def test_logfile_created_and_stamp(tmp_path: Path):
    run_id = "0.0.1_base"
    log_dir = tmp_path / "logs"
    logger.reset_logging()  # clean slate
    logger.configure_logging("none", run_id=run_id, log_dir=log_dir)

    log_path = log_dir / f"{run_id}.log"
    assert log_path.exists(), "logger should create the file on first call"

    content = log_path.read_text(encoding="utf-8").splitlines()
    assert content[0] == f"RUN_ID={run_id}"
    assert content[1].startswith("BEGIN-STAMP "), "BEGIN-STAMP must be written for *_base runs"

    # Re-configure again → file should get APPENDED another BEGIN-STAMP
    logger.reset_logging()
    logger.configure_logging("none", run_id=run_id, log_dir=log_dir)
    new_lines = log_path.read_text(encoding="utf-8").splitlines()
    assert len(new_lines) == 3  # original 2 + fresh stamp
    assert new_lines[-1].startswith("BEGIN-STAMP ")
