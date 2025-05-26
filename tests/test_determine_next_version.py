# Copyright © 2025 by Nick Jenkins. All rights reserved

from pathlib import Path

from personalvibe import vibe_utils
from personalvibe.parse_stage import determine_next_version


def _prep(tmp_path: Path):
    root = tmp_path / "repo"
    stages = root / "prompts" / "demo" / "stages"
    stages.mkdir(parents=True)
    return root, stages


def test_sprint_increment(monkeypatch, tmp_path):
    root, stages = _prep(tmp_path)
    # fake repo root lookup
    monkeypatch.patch.object(vibe_utils, "get_base_path", lambda: root)
    # existing sprint file 4.3.0.py
    (stages / "4.3.0.py").write_text("# dummy")
    nxt = determine_next_version("demo", "sprint")
    assert nxt == "4.4.0"
