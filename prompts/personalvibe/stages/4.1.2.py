# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/4.2.0.py

"""
patch_fix_log_to.py

Sprint 1  –  Dependency-diet milestone
=====================================

This one-off helper **patches the faulty `_log_to` context-manager** inside
`noxfile.py`.  The previous implementation accidentally contained **two**
code blocks in the same generator which broke the contextlib contract and
caused:

    RuntimeError: generator didn't stop

in `tests/test_log_to_cm.py` and `tests/test_log_to_subprocess.py`.

The replacement below is:

* single generator (yield exactly once)
* pre-creates the target file and opens **append** mode
* duplicates file-descriptors 1 & 2 so *sub-processes* inherit them
* mirrors Python‐level `sys.stdout/stderr` so regular `print()` works
* guarantees clean restoration, even on error

Run this script from anywhere inside the repository root:

    python patch_fix_log_to.py

Afterwards re-run the quality-gate:

    bash tests/personalvibe.sh
"""

from __future__ import annotations

import io
import os
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path


# ---------------------------------------------------------------------------#
def _generate_fixed_log_to() -> str:
    """Return the Python source text for the new `_log_to` implementation."""
    return '''
from contextlib import contextmanager
import io
import os
import subprocess
import sys
from pathlib import Path


@contextmanager
def _log_to(path: Path):  # type: ignore[override]
    """
    Duplicate *all* stdout / stderr – including child-process output – to
    ``path`` **in append mode**.

    The algorithm:

    1. Ensure parent directories exist, then ``touch`` the file so `tee -a`
       never truncates.
    2. Spawn *one* persistent ``tee -a`` process and obtain its stdin FD.
    3. `os.dup2` that FD onto FD 1 and FD 2 so every sub-process inherits it.
    4. Replace `sys.stdout` / `sys.stderr` with fresh `TextIOWrapper`s that
       write to the *same* FD, preserving high-level Python printing.
    5. On context exit:
         • flush wrappers
         • restore original FDs and `sys.std*` objects
         • close tee stdin and wait for the process
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

    # ------------------------------------------------------------------ tee
    tee_proc = subprocess.Popen(
        ["tee", "-a", str(path)],
        stdin=subprocess.PIPE,
        text=False,      # binary mode for FD duplication
    )
    if tee_proc.stdin is None:  # pragma: no cover
        raise RuntimeError("Failed to obtain tee stdin")

    tee_fd = tee_proc.stdin.fileno()

    # ------------------------------------------------------------------ FDs
    saved_out_fd = os.dup(1)
    saved_err_fd = os.dup(2)
    os.dup2(tee_fd, 1)
    os.dup2(tee_fd, 2)

    # ---------------------------------------------------------------- PyIO
    saved_stdout_obj, saved_stderr_obj = sys.stdout, sys.stderr
    sys.stdout = io.TextIOWrapper(os.fdopen(os.dup(1), "wb"), encoding="utf-8", line_buffering=True)
    sys.stderr = io.TextIOWrapper(os.fdopen(os.dup(2), "wb"), encoding="utf-8", line_buffering=True)

    try:
        yield
    finally:
        try:
            sys.stdout.flush()
            sys.stderr.flush()
        except Exception:  # noqa: BLE001
            pass

        # restore low-level FDs first
        os.dup2(saved_out_fd, 1)
        os.dup2(saved_err_fd, 2)
        os.close(saved_out_fd)
        os.close(saved_err_fd)

        # close tee & wait
        tee_proc.stdin.close()
        tee_proc.wait()

        # restore Python objects
        sys.stdout, sys.stderr = saved_stdout_obj, saved_stderr_obj
    '''.lstrip()


def main() -> None:  # noqa: D401
    repo_root = Path(__file__).resolve()
    # climb until we find noxfile.py
    while not (repo_root / "noxfile.py").exists():
        if repo_root.parent == repo_root:
            raise SystemExit("noxfile.py not found – run from within repository.")
        repo_root = repo_root.parent

    noxfile_path = repo_root / "noxfile.py"
    content = noxfile_path.read_text(encoding="utf-8")

    # ------------------------------------------------------------------ patch
    marker = "# --- FIXED _log_to IMPLEMENTATION ---\n"
    if marker in content:
        print("✓  noxfile.py already patched – nothing to do.")
        return

    patched = content + "\n\n" + marker + _generate_fixed_log_to() + "\n# --- END FIXED _log_to IMPLEMENTATION ---\n"
    noxfile_path.write_text(patched, encoding="utf-8")
    print(f"✓  Patched _log_to in {noxfile_path.relative_to(repo_root)}")


if __name__ == "__main__":
    main()
