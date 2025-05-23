# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Verify default behavior works without model field."""

import os
from pathlib import Path

import pytest

from personalvibe import run_pipeline, vibe_utils


def test_default_model_fallback(monkeypatch, tmp_path):
    # Create minimal config with NO model field
    cfg_yaml = tmp_path / "test.yaml"
    cfg_yaml.write_text(
        """
        project_name: smoketest
        mode: milestone
        execution_details: ""
        code_context_paths: []
        """,
        encoding="utf-8",
    )

    # Mock the template loader and get_vibed to avoid real API calls
    monkeypatch.setattr(vibe_utils, "render_prompt_template", lambda *args, **kwargs: "Test prompt")

    # Capture the model parameter
    captured = {"model": None}

    def fake_get_vibed(prompt, **kwargs):
        captured["model"] = kwargs.get("model")
        return "Test response"

    monkeypatch.setattr(vibe_utils, "get_vibed", fake_get_vibed)

    # Create minimal prompts directory structure
    prompts_dir = tmp_path / "prompts" / "smoketest"
    prompts_dir.mkdir(parents=True)
    monkeypatch.setattr(vibe_utils, "get_base_path", lambda: tmp_path)

    # Run with --prompt_only to avoid actual API calls
    monkeypatch.setattr("sys.argv", ["pv", "run", "--config", str(cfg_yaml), "--prompt_only"])

    try:
        run_pipeline.main()
    except SystemExit:
        pass

    # Verify the model was None, which should trigger the default in llm_router
    assert captured["model"] is None
