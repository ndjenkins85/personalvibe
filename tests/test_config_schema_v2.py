# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Schema v2 tests – conversation_history + legacy compatibility."""

from pathlib import Path

from pydantic import ValidationError

from personalvibe.run_pipeline import ConfigModel, load_config


def _tmp_cfg(tmp_path: Path, yaml_txt: str) -> Path:
    p = tmp_path / "cfg.yaml"
    p.write_text(yaml_txt, encoding="utf-8")
    return p


def test_valid_history(tmp_path: Path):
    yaml_txt = """
    project_name: personalvibe
    task: milestone
    user_instructions: ""
    project_context_paths: []
    conversation_history:
      - role: user
        content: hi
      - role: assistant
        content: hello
    """
    cfg = load_config(str(_tmp_cfg(tmp_path, yaml_txt)))
    assert isinstance(cfg, ConfigModel)
    assert cfg.conversation_history[0]["role"] == "user"


def test_history_optional(tmp_path: Path):
    yaml_txt = """
    project_name: personalvibe
    task: prd
    user_instructions: ""
    project_context_paths: []
    """
    cfg = load_config(str(_tmp_cfg(tmp_path, yaml_txt)))
    assert cfg.conversation_history is None


def test_legacy_milestone_file_name_ignored(tmp_path: Path):
    yaml_txt = """
    project_name: personalvibe
    task: sprint
    user_instructions: ""
    project_context_paths: []
    milestone_file_name: legacy.txt  # obsolete
    """
    cfg = load_config(str(_tmp_cfg(tmp_path, yaml_txt)))
    assert not hasattr(cfg, "milestone_file_name")
