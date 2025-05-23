# Copyright © 2025 by Nick Jenkins. All rights reserved

import os
from pathlib import Path

from personalvibe import cli, vibe_utils


def _mk_repo(tmp_path: Path):
    root = tmp_path / "repo"
    stages = root / "prompts" / "demo" / "stages"
    stages.mkdir(parents=True)
    # baseline milestone 1.0.0
    (stages / "1.0.0.md").write_text("Milestone 1")
    return root


def test_prepare_sprint(monkeypatch, tmp_path):
    root = _mk_repo(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setenv("EDITOR", "true")  # no-op cmd
    cli.cli_main(["prepare-sprint", "--project_name", "demo", "--no-open"])
    assert Path(root, "1.1.0.yaml").exists()


def test_new_milestone(monkeypatch, tmp_path):
    root = _mk_repo(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setenv("EDITOR", "true")
    cli.cli_main(["new-milestone", "--project_name", "demo", "--no-open"])
    assert Path(root, "2.0.0.yaml").exists()
