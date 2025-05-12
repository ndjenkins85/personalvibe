# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/1.2.8.py
#!/usr/bin/env python
"""
sprint_2_patch.py – Sprint #2  (nox *vibed* enhancements & flaky-test fix)

Run me **once** from anywhere inside the repo:

    poetry run python sprint_2_patch.py

What this script does
---------------------
1. Replace the broken `pytest.register_mark` call with a modern
   `pytest_configure` hook (tests/conftest.py).
2. Add a focused unit-test that guarantees our logging harness really
   writes the header + BEGIN-STAMP lines (tests/test_logger.py).
3. (Already done in previous code) `_log_to` operates in *append* mode,
   so no change is required – but we assert that behaviour inside the
   new test.
4. Prints a short “next steps” message so you remember to run:

       nox -s tests
       nox -s vibed -- 0.0.2

That’s it – under 20 000 characters, only files relevant to sprint #2.
"""
from __future__ import annotations

import textwrap
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()


def _write(rel_path: str, content: str) -> None:
    """Create/overwrite `rel_path` (UTF-8, trailing newline)."""
    abs_path = REPO / rel_path
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    abs_path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
    print(f"✔  wrote {abs_path.relative_to(REPO)}")


# --------------------------------------------------------------------- #
# 1. Fix the deprecated pytest API usage
# --------------------------------------------------------------------- #
conftest_py = """
import pytest

# Single authoritative place to declare project-wide markers.  Older
# code used the removed `pytest.register_mark`.  The hook below works
# on every modern Pytest (≥7).
def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "advanced: marks tests that hit heavier integration paths "
        "(deselect with '-m \"not advanced\"').",
    )
"""
_write("tests/conftest.py", conftest_py)

# --------------------------------------------------------------------- #
# 2. Minimal unit-test for the logging harness (_BEGIN-STAMP behaviour)
# --------------------------------------------------------------------- #
test_logger_py = r"""
from pathlib import Path
from personalvibe import logger

def test_logfile_created_and_stamp(tmp_path: Path):
    run_id = "0.0.1_base"
    log_dir = tmp_path / "logs"
    logger.reset_logging()                      # clean slate
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
"""
_write("tests/test_logger.py", test_logger_py)

# --------------------------------------------------------------------- #
# 3. Friendly reminder
# --------------------------------------------------------------------- #
print(
    "\n🎉  Sprint #2 patch applied.\n"
    "Run quality-gate locally:\n"
    "   nox -s tests                     # fast feedback\n"
    "   nox -s vibed -- 0.0.2            # end-to-end (writes logs/0.0.2_base.log)\n"
)
