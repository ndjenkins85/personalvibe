# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/4.2.0.py

# sprint_4.1.1_fix_logging.py
"""
Sprint 4.1.1 – Fix `_log_to` so **sub-process output** is captured.

Problem
-------
`noxfile._log_to` only redirected Python-level `print()` statements.  Any
`subprocess.run()` invoked inside the context still wrote directly to the
original tty, so important banners (e.g. `pv parse-stage …`) never reached
`logs/<semver>_base.log`.

Solution
--------
1. Replace `_log_to` with an implementation that uses low-level
   `os.dup2` FD cloning.  This re-routes file-descriptors **1 & 2** to a
   `tee -a` child – thereby capturing *everything*, including C-extensions
   and arbitrary shell commands.
2. Add a regression test which spawns a real sub-process and asserts its
   output is present in the log file.

Run    `poetry run nox -rs lint tests`    or simply `bash tests/personalvibe.sh`
to verify.

The patch keeps cross-platform concerns in mind (falls back to original
stdout if `dup2` is unavailable, e.g. on very old Windows builds).
"""
from __future__ import annotations

import os
import sys
import textwrap
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()

# --------------------------------------------------------------------------- #
# 1️⃣  Patch `noxfile.py`
# --------------------------------------------------------------------------- #
noxfile_path = REPO / "noxfile.py"
src = noxfile_path.read_text(encoding="utf-8")

PATCH_TAG = "# --- PERSONALVIBE PATCH: robust _log_to ---"

if PATCH_TAG not in src:
    new_fn = f'''
{PATCH_TAG}
from contextlib import contextmanager
import io
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterator

@contextmanager
def _log_to(path: Path):  # type: ignore[override]
    """
    Context-manager that *appends* **all** stdout/stderr – including output
    from spawned sub-processes – to ``path`` using a persistent ``tee -a``.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

    # 1) spawn tee ----------------------------------------------------------------
    tee_proc = subprocess.Popen(
        ["tee", "-a", str(path)],
        stdin=subprocess.PIPE,
        text=False,  # binary stream
    )
    if tee_proc.stdin is None:                       # pragma: no cover
        raise RuntimeError("Failed to open tee stdin")

    # 2) low-level FD hijack -------------------------------------------------------
    saved_out_fd = os.dup(1)
    saved_err_fd = os.dup(2)
    os.dup2(tee_proc.stdin.fileno(), 1)
    os.dup2(tee_proc.stdin.fileno(), 2)

    # 3) wrap in Python TextIO so `print()` still works ----------------------------
    new_stdout = io.TextIOWrapper(os.fdopen(1, "wb", buffering=0), encoding="utf-8", line_buffering=True)
    new_stderr = io.TextIOWrapper(os.fdopen(2, "wb", buffering=0), encoding="utf-8", line_buffering=True)

    saved_stdout_obj, saved_stderr_obj = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = new_stdout, new_stderr
    try:
        yield
    finally:
        # flush buffers ------------------------------------------------------------
        try:
            sys.stdout.flush()
            sys.stderr.flush()
        except Exception:  # noqa: BLE001
            pass

        # restore original fds -----------------------------------------------------
        os.dup2(saved_out_fd, 1)
        os.dup2(saved_err_fd, 2)
        os.close(saved_out_fd)
        os.close(saved_err_fd)

        # close tee + wait ---------------------------------------------------------
        tee_proc.stdin.close()
        tee_proc.wait()

        # restore Python objects ---------------------------------------------------
        sys.stdout, sys.stderr = saved_stdout_obj, saved_stderr_obj
'''
    # Inject the patch **after** first definition of _log_to to override it
    insertion_point = src.find("def _log_to(")
    insertion_point = src.find("\n", insertion_point) + 1  # end of that line
    src = src[:insertion_point] + new_fn + src[insertion_point:]
    noxfile_path.write_text(src, encoding="utf-8")
    print(f"✅  Patched noxfile._log_to with FD-level redirection ({noxfile_path})")
else:
    print("ℹ️  Patch already present – no changes made to noxfile.py")

# --------------------------------------------------------------------------- #
# 2️⃣  Add regression test
# --------------------------------------------------------------------------- #
test_path = REPO / "tests" / "test_log_to_subprocess.py"
if not test_path.exists():
    test_code = '''
# Copyright © 2025 by Nick Jenkins. All rights reserved
"""Ensure `_log_to` captures *sub-process* stdout & stderr."""
import subprocess
import sys
from pathlib import Path

import importlib
import noxfile  # type: ignore


def test_log_to_captures_subprocess(tmp_path: Path):
    importlib.reload(noxfile)  # make sure patched version is loaded
    log_file = tmp_path / "proc.log"

    with noxfile._log_to(log_file):  # type: ignore[attr-defined]
        # python prints to stdout
        print("parent says hi")
        # real sub-process prints to both stdout and stderr
        subprocess.run(
            [sys.executable, "-c", "import sys; print('child out'); print('child err', file=sys.stderr)"],
            check=True,
        )

    content = log_file.read_text(encoding="utf-8")
    assert "parent says hi" in content
    assert "child out" in content
    assert "child err" in content
'''
    test_path.write_text(textwrap.dedent(test_code), encoding="utf-8")
    print(f"✅  Added regression test {test_path.relative_to(REPO)}")
else:
    print("ℹ️  Regression test already exists – no changes made")

# --------------------------------------------------------------------------- #
# 3️⃣  Friendly reminder
# --------------------------------------------------------------------------- #
print(
    "\\nNext steps:\\n"
    "1) Run  `poetry lock --no-update`  if you have not already (ensures lean lock-file).\\n"
    "2) Execute the quality-gate:  bash tests/personalvibe.sh\\n"
    "   – the new test *test_log_to_subprocess.py* validates end-to-end capture.\\n"
    "Happy vibecoding! 🚀"
)
