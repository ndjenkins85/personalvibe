# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Integration test for the Sharp_Boe custom LLM provider."""

import os
from types import SimpleNamespace

import pytest

from personalvibe import llm_router


class FakeResponse:
    def __init__(self, data):
        self._data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self._data


def test_sharp_boe_chat_completion(monkeypatch):
    # Arrange: set the secret and capture requests.post
    monkeypatch.setenv("SHARP_USER_SECRET", "supersecret")
    calls = {}

    def fake_post(url, json=None, headers=None):
        calls["url"] = url
        calls["json"] = json
        calls["headers"] = headers
        return FakeResponse({"choices": [{"message": {"content": "👍"}}]})

    # Patch requests.post in the llm_router module
    monkeypatch.setattr("personalvibe.llm_router.requests.post", fake_post)

    # Act: call chat_completion with a sharp_boe model
    model = "sharp_boe/test-model"
    messages = [{"role": "user", "content": "Hello"}]
    result = llm_router.chat_completion(model=model, messages=messages, max_tokens=5)

    # Assert: custom provider was used and returned expected data
    assert result["choices"][0]["message"]["content"] == "👍"
    assert "sharp_boe/test-model".startswith("sharp_boe/")
    # URL should include the model name
    assert calls["url"].endswith("/test-model/completions")
    # Authorization header present
    assert calls["headers"]["Authorization"] == "Bearer supersecret"
    # Payload includes our messages and kwargs
    assert calls["json"]["messages"] == messages
    assert calls["json"]["max_tokens"] == 5
