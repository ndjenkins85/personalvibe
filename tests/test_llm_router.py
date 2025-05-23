# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Unit-tests for the LiteLLM shim."""

from types import SimpleNamespace

import pytest

from personalvibe import llm_router


def test_chat_completion_default(monkeypatch):
    """Happy path – default model + passthrough args."""
    captured = SimpleNamespace(called=False, kwargs=None)

    def _fake_completion(**kw):
        captured.called = True
        captured.kwargs = kw
        # mimic litellm response object
        return {"choices": [{"message": {"content": "hi"}}]}

    monkeypatch.setattr("litellm.completion", _fake_completion)

    messages = [{"role": "user", "content": "hello"}]
    resp = llm_router.chat_completion(messages=messages)

    assert captured.called
    assert captured.kwargs["model"] == "openai/o3"
    assert captured.kwargs["messages"] == messages
    assert resp["choices"][0]["message"]["content"] == "hi"


def test_chat_completion_custom_model(monkeypatch):
    called = {}

    def _fake(**kw):
        called["model"] = kw["model"]
        return {"ok": True}

    monkeypatch.setattr("litellm.completion", _fake)

    llm_router.chat_completion(model="openrouter/mistral-7b", messages=[{"role": "user", "content": "x"}])
    assert called["model"] == "openrouter/mistral-7b"


def test_chat_completion_invalid_model():
    with pytest.raises(ValueError):
        llm_router.chat_completion(model="badmodel", messages=[{"role": "user", "content": "hey"}])
