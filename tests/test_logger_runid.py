# Copyright © 2025 by Nick Jenkins. All rights reserved

import logging
from pathlib import Path

from personalvibe import logger as pv_logger


def test_configure_logging_run_id(tmp_path):
    pv_logger.reset_logging()
    run_id = "testrun_1234abcd"
    pv_logger.configure_logging("none", color=False, run_id=run_id, log_dir=tmp_path)
    log = logging.getLogger(__name__)
    log.info("hello world")
    log_path = Path(tmp_path) / f"{run_id}.log"
    assert log_path.exists(), "Run-ID log file not created"
    first_line = log_path.read_text(encoding="utf-8").splitlines()[0]
    assert first_line.strip() == f"RUN_ID={run_id}"
