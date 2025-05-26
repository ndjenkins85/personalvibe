# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Test bugfix mode functionality."""

from pathlib import Path

import pytest

from personalvibe import vibe_utils
from personalvibe.run_pipeline import ConfigModel, load_config


def test_bugfix_mode_config(tmp_path):
    """Test that bugfix mode is accepted in config."""
    cfg_yaml = tmp_path / "1.0.1.yaml"
    cfg_yaml.write_text(
        """
        project_name: testproject
        mode: bugfix
        execution_details: "Fix the import error"
        code_context_paths: []
    """,
        encoding="utf-8",
    )

    config = load_config(str(cfg_yaml))
    assert config.mode == "bugfix"
    assert config.execution_details == "Fix the import error"


def test_bugfix_file_extension(monkeypatch, tmp_path):
    """Test that bugfix versions use .md extension."""
    from personalvibe.parse_stage import determine_next_version

    root = tmp_path / "repo"
    stages = root / "prompts" / "demo" / "stages"
    stages.mkdir(parents=True)

    # Create an existing sprint file
    (stages / "1.1.0.py").write_text("# sprint code")

    monkeypatch.patch.object(vibe_utils, "get_base_path", lambda: root)

    # Next version should be a bugfix
    next_ver = determine_next_version("demo", "bugfix")
    assert next_ver == "1.1.1"  # bugfix version
