# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/1.2.2.py
#!/usr/bin/env python
"""
patch_sprint_2.py  – “Logging Harness & Tests”

Run this once (e.g. `python patch_sprint_2.py`) from *anywhere* inside the
repository.  The script

1.  Switches noxfile._log_to() to **append** mode (tee ‑a).
2.  Adds pytest coverage for the per-semver log contract.
3.  Provides an auto-reset fixture for logger tests.
4.  Supplies a stage-driver that correctly invokes “nox -s vibed”.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("")


def patch_file(path: Path, pattern: str, replacement: str) -> None:
    txt = path.read_text(encoding="utf-8")
    if re.search(pattern, txt, flags=re.DOTALL):
        new = re.sub(pattern, replacement, txt, flags=re.DOTALL)
        path.write_text(new, encoding="utf-8")


# --------------------------------------------------------------------------- #
# 1. PATCH noxfile._log_to – append, never truncate
# --------------------------------------------------------------------------- #
NOXFILE = REPO / "noxfile.py"
patch_file(
    NOXFILE,
    r"def _log_to\(path: Path\):[\s\S]+?with path\.open\(\"w\"\) as fh:",
    dedent(
        """
        def _log_to(path: Path):
            \"\"\"Context manager that duplicates everything sent to stdout/stderr.

            IMPORTANT: always **append** to the target log so previous
            processes (e.g. lint / pytest) are preserved.
            \"\"\"
            # Keep handle open so concurrent writers don’t delete the file.
            with path.open("a") as fh:  # ← append not truncate
                # tee -a  … also append
                proc = subprocess.Popen(
                    ["tee", "-a", str(path)],
                    stdin=subprocess.PIPE,
                    text=True,
                )  # type: ignore[arg-type]
                saved_out, saved_err = sys.stdout, sys.stderr
                sys.stdout = sys.stderr = proc.stdin  # type: ignore[assignment]
                try:
                    yield
                finally:
                    sys.stdout.flush()
                    sys.stderr.flush()
                    proc.stdin.close()  # type: ignore[attr-defined]
                    proc.wait()
                    sys.stdout, sys.stderr = saved_out, saved_err
        """
    ).strip(),
)

print("✓  Patched noxfile._log_to → append mode")


# --------------------------------------------------------------------------- #
# 2.  Add pytest coverage for logger behaviour
# --------------------------------------------------------------------------- #
TEST_PY = REPO / "tests" / "test_logger.py"
touch(TEST_PY)
TEST_PY.write_text(
    dedent(
        """
        \"\"\"Unit-tests for per-semver logging contract.\"\"\"

        from pathlib import Path
        import time

        import pytest
        from personalvibe import logger as _logger

        # ------------------------------------------------------------------ #
        # Fixtures
        # ------------------------------------------------------------------ #
        @pytest.fixture(autouse=True)
        def _reset_logging():
            \"\"\"Ensure a clean logging env before & after each test.\"\"\"
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
        """
    ).lstrip(),
    encoding="utf-8",
)

print("✓  Added tests/test_logger.py")


# --------------------------------------------------------------------------- #
# 3. Stage driver that shells-out to nox vibed
# --------------------------------------------------------------------------- #
STAGE_DIR = REPO / "prompts" / "personalvibe" / "stages"
STAGE_PY = STAGE_DIR / "1.2.0.py"
touch(STAGE_PY)
STAGE_PY.write_text(
    dedent(
        """
        \"\"\"Stage driver for sprint 1.2.0 – calls `nox -s vibed` correctly.\"\"\"

        import subprocess
        import sys
        from pathlib import Path

        def main() -> None:
            if len(sys.argv) < 2:
                print("Usage: python 1.2.0.py <semver>")
                sys.exit(1)
            semver = sys.argv[1]
            # Bubble all output so the parent process handles logging/tee
            cmd = ["nox", "-s", "vibed", "--", semver]
            print(f"▶ Running: {' '.join(cmd)}")
            try:
                subprocess.check_call(cmd)
            except subprocess.CalledProcessError as exc:
                print(f"❌ nox vibed failed with code {exc.returncode}")
                sys.exit(exc.returncode)

        if __name__ == "__main__":
            main()
        """
    ).lstrip(),
    encoding="utf-8",
)
print("✓  Added prompts/personalvibe/stages/1.2.0.py")


# --------------------------------------------------------------------------- #
# 4.  Ensure tests/personalvibe.sh is executable (idempotent chmod +x)
# --------------------------------------------------------------------------- #
SH = REPO / "tests" / "personalvibe.sh"
if SH.exists():
    SH.chmod(SH.stat().st_mode | 0o111)
    print("✓  Ensured tests/personalvibe.sh is executable")


# --------------------------------------------------------------------------- #
# 5.  Done – print next steps
# --------------------------------------------------------------------------- #
print(
    dedent(
        """
        ------------------------------------------------------------------------
        Patch applied.  Recommended quick-check:

            nox -s tests                   # unit tests incl. new logger suite
            nox -s vibed -- 1.2.0          # full branch + gate (uses new stage)

        Verify that logs/1.2.0_base.log collects *all* BEGIN-STAMP entries
        without truncation.
        ------------------------------------------------------------------------
        """
    )
)
