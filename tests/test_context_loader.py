# Copyright © 2025 by Nick Jenkins. All rights reserved

# tests/test_context_loader.py
# run with:  pytest -q
import importlib
from pathlib import Path
from types import SimpleNamespace

import pytest

MODULE = "personalvibe.vibe_utils"  # adjust if you move the library


@pytest.fixture()
def dummy_project(tmp_path, monkeypatch):
    """
    Create an in-memory mini project:
        tmp/
        ├─ a.py
        ├─ config.json
        ├─ src/personalvibe/core.py
        ├─ tests/test_ok.py
        └─ tests/otherproject/skipme.py
    """
    base: Path = tmp_path
    (base / "src/personalvibe").mkdir(parents=True)
    (base / "tests/otherproject").mkdir(parents=True)

    # populate dummy files
    for file_ in [
        "a.py",
        "config.json",
        "src/personalvibe/core.py",
        "tests/test_ok.py",
        "tests/otherproject/skipme.py",
    ]:
        (base / file_).write_text(f"# {file_}\n")

    # config equivalent to prompts/personalvibe/context/codefiles.txt
    cfg = base / "codefiles.txt"
    cfg.write_text(
        """\
# include everything under src
src/personalvibe/**
# top-level scripts
/*.py
/*.json
tests/*
X tests/otherproject/**
"""
    )

    # stub helpers inside the imported module
    dummy_gitignore = SimpleNamespace(match_file=lambda _: False)
    monkeypatch.syspath_prepend(str(base))
    module = importlib.import_module(MODULE)

    monkeypatch.setattr(module, "load_gitignore", lambda _p: dummy_gitignore)
    monkeypatch.setattr(module, "get_base_path", lambda: base)
    monkeypatch.setattr(module, "_process_file", lambda p: f"<<{p.name}>>\n")

    return module, cfg


def test_get_context_includes_and_excludes(dummy_project):
    module, cfg = dummy_project
    result = module.get_context([cfg.name])

    # included
    assert "<<a.py>>" in result
    assert "<<config.json>>" in result
    assert "<<core.py>>" in result
    assert "<<test_ok.py>>" in result
    # manually excluded
    assert "<<skipme.py>>" not in result
