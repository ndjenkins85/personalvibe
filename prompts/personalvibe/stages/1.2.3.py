# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/1.2.3.py
#!/usr/bin/env python
"""
Sprint-2 patch:  “nox vibed enhancements”

This file is meant to be executed via

    poetry run python data/storymaker/prompt_outputs/mypatch.py
or simply copied into that location and re-run
    nox -s vibed -- 1.2.2

What it does
------------
1. Patches noxfile._log_to:
      * removes the stray **second** tee section
      * guarantees true append behaviour
2. Adds tests/test_log_to.py to exercise the context-manager
      – ensures first & second invocations both land in the same file.
3. Touch-creates __init__.py under tests/ (pytest discovers correctly
   without it but it’s nice for import tooling).

After running this patch you should:

    nox -s tests                   # 15 tests incl. new suite
    nox -s vibed -- 1.2.2          # branch + gate, now appending logs

"""
from __future__ import annotations

import inspect
import re
import sys
import textwrap
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()


# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #
def _overwrite(path: Path, new_text: str) -> None:
    path.write_text(new_text, encoding="utf-8")
    print(f"✓  Patched {path.relative_to(REPO)}")


def _ensure_parent(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------- #
# 1️⃣  Patch `noxfile._log_to`                                                #
# --------------------------------------------------------------------------- #
noxfile_path = REPO / "noxfile.py"
source = noxfile_path.read_text(encoding="utf-8")

pattern = re.compile(
    r"@contextmanager\n"
    r"def _log_to\(.*?\):\n"  # def header
    r"(?:.|\n)*?"  # non-greedy, up to…
    r"@session",  # …next decorator marks end of func.
    re.MULTILINE,
)

old_block = pattern.search(source)
if not old_block:
    print("ERROR: could not locate _log_to definition in noxfile.py")
    sys.exit(1)

# --------------------------------------------------------------------------- #
# New implementation – single tee, true append                                #
# --------------------------------------------------------------------------- #
new_func = textwrap.dedent(
    """
    @contextmanager
    def _log_to(path: Path):
        \"\"\"Duplicate *all* stdout/stderr to **append** mode log file.

        The implementation purposefully:
        • opens the target file beforehand so it is never truncated
        • spawns one long-lived ``tee -a`` process
        • restores sys.std* even if exceptions occur
        \"\"\"
        path.parent.mkdir(parents=True, exist_ok=True)
        # Ensure file exists so tee -a never complains
        path.touch(exist_ok=True)

        proc = subprocess.Popen(
            [\"tee\", \"-a\", str(path)],
            stdin=subprocess.PIPE,
            text=True,
        )  # type: ignore[arg-type]
        saved_out, saved_err = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = proc.stdin  # type: ignore[assignment]
        try:
            yield
        finally:
            # Flush and close the tee input; restore
            try:
                sys.stdout.flush()
                sys.stderr.flush()
            finally:
                proc.stdin.close()  # type: ignore[attr-defined]
                proc.wait()
                sys.stdout, sys.stderr = saved_out, saved_err
    """
).strip("\n")

# Splice the new block in
start, end = old_block.span()
patched_source = source[:start] + new_func + "\n\n" + source[end:]

_overwrite(noxfile_path, patched_source)

# --------------------------------------------------------------------------- #
# 2️⃣  Add pytest for _log_to                                                 #
# --------------------------------------------------------------------------- #
test_path = REPO / "tests" / "test_log_to_cm.py"
_ensure_parent(test_path)

test_code = textwrap.dedent(
    """
    \"\"\"Tests for the revised noxfile._log_to context-manager.\"\"\"
    import tempfile
    from pathlib import Path
    import importlib

    import noxfile  # type: ignore

    def _read(p: Path) -> str:
        return p.read_text(encoding=\"utf-8\")

    def test_log_to_appends_twice(tmp_path: Path):
        log_file = tmp_path / \"sample.log\"

        # First write
        with noxfile._log_to(log_file):  # type: ignore[attr-defined]
            print(\"hello world\")

        first = _read(log_file)
        assert \"hello world\" in first
        size_after_first = log_file.stat().st_size

        # Second write
        with noxfile._log_to(log_file):  # type: ignore[attr-defined]
            print(\"second time!\")

        second = _read(log_file)
        assert \"second time!\" in second
        # File grew, not overwritten
        assert log_file.stat().st_size > size_after_first
    """
).lstrip()

_overwrite(test_path, test_code)

# --------------------------------------------------------------------------- #
# 3️⃣  Ensure tests/ is importable (aids editors, harmless otherwise)        #
# --------------------------------------------------------------------------- #
init_path = REPO / "tests" / "__init__.py"
if not init_path.exists():
    _overwrite(init_path, "# pytest namespace helper\n")


# --------------------------------------------------------------------------- #
# 4️⃣  Epilogue                                                               #
# --------------------------------------------------------------------------- #
print(
    """
------------------------------------------------------------------------
Patch applied.  Recommended quick-check:

    nox -s tests                   # unit tests incl. new log_to suite
    nox -s vibed -- 1.2.2          # full branch + gate (uses new stage)

Verify that logs/1.2.2_base.log collects *all* BEGIN-STAMP entries
without truncation.
------------------------------------------------------------------------
"""
)
