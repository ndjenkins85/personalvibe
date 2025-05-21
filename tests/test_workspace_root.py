# Copyright © 2025 by Nick Jenkins. All rights reserved

import os
from pathlib import Path

from personalvibe import vibe_utils


def test_workspace_env_override(tmp_path, monkeypatch):
    monkeypatch.setenv("PV_DATA_DIR", str(tmp_path))
    assert vibe_utils.get_workspace_root() == tmp_path.resolve()


def test_save_prompt_install_mode(tmp_path, monkeypatch):
    monkeypatch.setenv("PV_DATA_DIR", str(tmp_path))
    data_dir = vibe_utils.get_data_dir("demo")
    assert data_dir == tmp_path / "data" / "demo"

    p = vibe_utils.save_prompt("hello world", data_dir)
    # file is inside the overridden workspace
    assert str(p).startswith(str(data_dir))
