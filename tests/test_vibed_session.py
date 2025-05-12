# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Integration test for `nox -s vibed` (advanced).

It spawns a **sub-process** that executes:

    nox -s vibed -- 0.0.2 tests/dummy_patch.py

The session should:
  • create logs/0.0.2_base.log (append mode)
  • contain the three m
"""

import subprocess
from pathlib import Path

import pytest


@pytest.mark.advanced
def test_vibed_creates_base_log(tmp_path):
    log_path = Path("logs") / "0.0.2_base.log"
    # Start clean
    if log_path.exists():
        log_path.unlink()

    # Record current branch to restore later
    current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()

    try:
        subprocess.run(
            ["nox", "-s", "vibed", "--", "0.0.2", "tests/dummy_patch.py"],
            check=True,
            text=True,
        )
    finally:
        # Switch back & drop test branch to keep workspace tidy
        subprocess.run(["git", "checkout", current_branch], check=True, text=True)
        subprocess.run(["git", "branch", "-D", "vibed/0.0.2"], check=False, text=True)

    assert log_path.exists(), "vibed should create logs/0.0.2_base.log"
    content = log_path.read_text()

    expected = [
        "Creating branch vibed/0.0.2",
        "Running patch script: tests/dummy_patch.py",
        "Executing quality-gate (tests/personalvibe.sh)",
    ]
    for phrase in expected:
        assert phrase in content, f"Missing banner line: {phrase}"
