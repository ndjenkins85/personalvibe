# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Smoke test for prompt_only mode with sprint template."""

import os
from pathlib import Path

from personalvibe import run_pipeline, vibe_utils


def test_prompt_only_sprint_template(monkeypatch, tmp_path):
    """Verify prompt_only mode works with sprint_template.yaml."""
    # Create minimal config using sprint template format
    cfg_yaml = tmp_path / "1.1.0.yaml"
    cfg_yaml.write_text(
        """
        project_name: smoketest
        mode: sprint
        execution_details: "Test smoketest sprint execution"
        code_context_paths: []
        """,
        encoding="utf-8",
    )

    # Create required directory structure
    prompts_dir = tmp_path / "prompts" / "smoketest"
    stages_dir = prompts_dir / "stages"
    stages_dir.mkdir(parents=True)

    # Create PRD template
    prd_path = prompts_dir / "prd.md"
    prd_path.write_text(
        """# {{ project_name }} PRD

Task: {{ execution_task }}

{{ instructions }}

Details: {{ execution_details }}

Code context:
{{ code_context }}
""",
        encoding="utf-8",
    )

    # Create a minimal milestone file
    milestone_path = stages_dir / "1.0.0.md"
    milestone_path.write_text(
        """# Milestone 1: Initial Setup

        This milestone focuses on basic setup.

        Sprint 1: Create basic structure
        """,
        encoding="utf-8",
    )

    # Mock get_base_path to return our temp directory
    monkeypatch.setattr(vibe_utils, "get_base_path", lambda: tmp_path)

    # Mock the template loader to return our test templates
    def mock_load_template(fname):
        if fname == "sprint.md":
            return "Sprint instructions: Execute the requested sprint."
        elif fname == "milestone.md":
            return "Milestone instructions: Plan the next milestone."
        elif fname == "validate.md":
            return "Validate instructions: Check the sprint results."
        return ""

    monkeypatch.setattr(vibe_utils, "_load_template", mock_load_template)

    # IMPORTANT: Set PV_DATA_DIR to use our temp directory for data files
    monkeypatch.setenv("PV_DATA_DIR", str(tmp_path))

    # Run with prompt_only
    import sys

    monkeypatch.setattr(sys, "argv", ["pv", "--config", str(cfg_yaml), "--prompt_only"])

    try:
        run_pipeline.main()
    except SystemExit:
        pass

    # Verify prompt was saved in the workspace-aware location
    data_dir = tmp_path / "data" / "smoketest" / "prompt_inputs"
    assert data_dir.exists(), f"Expected {data_dir} to exist"

    # Check that at least one prompt file was created
    prompt_files = list(data_dir.glob("*.md"))
    assert len(prompt_files) > 0, "No prompt files were created"

    # Verify the prompt contains expected content
    prompt_content = prompt_files[0].read_text(encoding="utf-8")
    assert "smoketest" in prompt_content
    assert "sprint number marked 1" in prompt_content
    assert "Sprint instructions" in prompt_content


def test_prompt_only_with_max_tokens(monkeypatch, tmp_path):
    """Verify max_tokens parameter works with prompt_only."""
    cfg_yaml = tmp_path / "1.0.0.yaml"
    cfg_yaml.write_text(
        """
        project_name: tokentest
        mode: milestone
        execution_details: ""
        code_context_paths: []
        """,
        encoding="utf-8",
    )

    # Create minimal structure
    prompts_dir = tmp_path / "prompts" / "tokentest"
    prompts_dir.mkdir(parents=True)

    prd_path = prompts_dir / "prd.md"
    prd_path.write_text("# Test PRD\n{{ execution_task }}", encoding="utf-8")

    monkeypatch.setattr(vibe_utils, "get_base_path", lambda: tmp_path)
    monkeypatch.setattr(vibe_utils, "_load_template", lambda x: "Test template")

    # IMPORTANT: Set PV_DATA_DIR to use our temp directory
    monkeypatch.setenv("PV_DATA_DIR", str(tmp_path))

    # Run with custom max_tokens
    import sys

    monkeypatch.setattr(sys, "argv", ["pv", "--config", str(cfg_yaml), "--prompt_only", "--max_tokens", "50000"])

    try:
        run_pipeline.main()
    except SystemExit:
        pass

    # Just verify it ran without error
    data_dir = tmp_path / "data" / "tokentest" / "prompt_inputs"
    assert data_dir.exists(), f"Expected {data_dir} to exist"
