# Copyright © 2025 by Nick Jenkins. All rights reserved
"""Chunk-3 regression: vibe_utils.get_vibed must call llm_router.chat_completion."""

from pathlib import Path
from types import SimpleNamespace

from personalvibe import llm_router, vibe_utils


def test_get_vibed_uses_router(monkeypatch, tmp_path: Path):
    captured = SimpleNamespace(called=False, kwargs=None)

    def _fake_chat_completion(**kw):
        captured.called = True
        captured.kwargs = kw
        # minimal litellm-style stub
        return {"choices": [{"message": {"content": "hi there"}}]}

    monkeypatch.patch.object(llm_router, "chat_completion", _fake_chat_completion)

    prompt = "Hello integration test!"
    workspace = tmp_path / "ws"
    workspace.mkdir()

    res = vibe_utils.get_vibed(prompt, project_name="demo", workspace=workspace)

    assert res == "hi there"
    assert captured.called is True
    assert captured.kwargs["messages"][-1]["content"][0]["text"] == prompt
