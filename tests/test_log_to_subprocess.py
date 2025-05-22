# Copyright © 2025 by Nick Jenkins. All rights reserved
"""Ensure `_log_to` captures *sub-process* stdout & stderr."""
import importlib
import subprocess
import sys
from pathlib import Path

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
