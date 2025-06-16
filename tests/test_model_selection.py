# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Integration smoke test for model selection."""

import os
import sys
from unittest import mock

import pytest

from personalvibe import run_pipeline, vibe_utils


def test_model_field_passed_to_router(monkeypatch, tmp_path):
    # Create minimal config with model field
    cfg_yaml = tmp_path / "0.0.0.yaml"
    cfg_yaml.write_text(
        """
        project_name: smoketest
        task: milestone
        model: sharp_boe/sharp_gemma3_12k_128b
        user_instructions: ""
        project_context_paths: []
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

    monkeypatch.setattr(
        "personalvibe.llm_router.chat_completion",
        lambda **kwargs: {"choices": [{"message": {"content": "test complete"}}]},
    )

    # Run with --prompt_only to avoid actual API calls
    # monkeypatch.setattr(sys, "argv", ["pv", "--config", str(cfg_yaml), "--prompt_only"])
    monkeypatch.setattr(sys, "argv", ["pv", "--config", str(cfg_yaml)])

    try:
        run_pipeline.main()
    except SystemExit:
        pass

    # Verify the model was passed through correctly
    assert captured["model"] == "sharp_boe/sharp_gemma3_12k_128b"
