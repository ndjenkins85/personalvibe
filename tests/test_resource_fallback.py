# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Resource loader fallback tests."""

import importlib.resources
from unittest import mock

from personalvibe import vibe_utils


def test_load_template_package():
    txt = vibe_utils._load_template("master.md")
    assert "you will be given the following information" in txt.lower()


def test_load_template_legacy(monkeypatch):
    """Force package path to fail → must fall back to legacy file."""

    def _raise(*_, **__):
        raise FileNotFoundError

    with mock.patch.object(importlib.resources, "files", _raise):
        txt = vibe_utils._load_template("master.md")
        assert "you will be given the following information" in txt.lower()
