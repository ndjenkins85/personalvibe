# Copyright © 2025 by Nick Jenkins. All rights reserved

"""
Extra CLI smoke-tests for new sub-commands.
"""

import shutil
import subprocess
import sys
from pathlib import Path

_PV = shutil.which("pv") or sys.executable + " -m personalvibe.cli"


def _run(*args):
    if isinstance(_PV, str) and _PV.endswith("cli"):
        cmd = _PV.split() + list(args)
    else:
        cmd = [_PV, *args]  # type: ignore[list-item]
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def test_help_ok():
    res = _run("--help")
    assert res.returncode == 0
    assert "Personalvibe CLI – Command-Line Interface" in res.stdout


def test_subcommand_help():
    for sub in ("run", "milestone", "sprint", "validate", "parse-stage"):
        res = _run(sub, "--help")
        assert res.returncode == 0, f"{sub} --help failed"
