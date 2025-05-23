# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Tests for the YAML sanitiser introduced in Chunk-4."""

from pathlib import Path

import pytest

from personalvibe.run_pipeline import load_config


def _mk_cfg(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "cfg.yaml"
    p.write_text(body, encoding="utf-8")
    return p


def test_control_chars_stripped(tmp_path: Path):
    txt = "project_name: demo\n" "mode: milestone\n" 'execution_details: "bad\x07value"\n' "code_context_paths: []\n"
    cfg = load_config(str(_mk_cfg(tmp_path, txt)))
    assert cfg.execution_details == "bad value"


def test_invalid_surrogate_raises(tmp_path: Path):
    bad = "project_name: demo\n" "mode: milestone\n" 'execution_details: "oops\ud800oops"\n' "code_context_paths: []\n"
    with pytest.raises(ValueError):
        load_config(str(_mk_cfg(tmp_path, bad)))
