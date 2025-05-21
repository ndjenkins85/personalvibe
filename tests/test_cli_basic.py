# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Smoke-test for the new ``pv`` entry-point."""

import shutil
import subprocess
from pathlib import Path


def test_pv_help():
    exe = shutil.which("pv")
    assert exe, "'pv' console script not found – poetry install failed?"
    res = subprocess.run([exe, "--help"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert res.returncode == 0
    assert "Personalvibe CLI" in res.stdout
