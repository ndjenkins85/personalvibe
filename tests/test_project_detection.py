# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Tests for vibe_utils.detect_project_name (chunk 2)."""

from pathlib import Path

import pytest

from personalvibe.vibe_utils import detect_project_name


def _mk_repo(tmp_path: Path, names: list[str]) -> Path:
    """Create minimal prompts/<name> dirs and return repo root."""
    root = tmp_path / "myrepo"
    for n in names:
        (root / "prompts" / n / "stages").mkdir(parents=True)
    return root


def test_detect_from_nested_dir(tmp_path, monkeypatch):
    root = _mk_repo(tmp_path, ["alpha"])
    deep = root / "prompts" / "alpha" / "stages"
    monkeypatch.chdir(deep)
    assert detect_project_name() == "alpha"


def test_detect_single_project_from_root(tmp_path, monkeypatch):
    root = _mk_repo(tmp_path, ["solo"])
    monkeypatch.chdir(root)
    assert detect_project_name() == "solo"


def test_detect_ambiguous(tmp_path, monkeypatch):
    root = _mk_repo(tmp_path, ["one", "two"])
    monkeypatch.chdir(root)
    with pytest.raises(ValueError):
        detect_project_name()


def test_detect_not_found(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError):
        detect_project_name()
