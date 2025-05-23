# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/6.3.1.py

#!/usr/bin/env python3
import os
import re
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()


def patch_llm_router():
    llm_router_path = REPO / "src" / "personalvibe" / "llm_router.py"
    text = llm_router_path.read_text(encoding="utf-8")
    changed = False

    # 1) Insert imports for os and requests if missing
    if "import requests" not in text:
        # after litellm import
        text = re.sub(
            r"(import litellm\s*)",
            r"\1\nimport os\nimport requests\n",
            text,
            count=1,
        )
        changed = True

    # 2) Insert MyCustomLLM class if missing
    if "class MyCustomLLM" not in text:
        custom_class = '''
class MyCustomLLM:
    """Custom Sharp_Boe LLM provider wrapper."""
    API_URL = "https://api.sharpboe.com"

    def __init__(self):
        secret = os.getenv("SHARP_USER_SECRET")
        if not secret:
            raise ValueError("SHARP_USER_SECRET env var not set")
        self.secret = secret

    def completion(self, model: str, messages: list, **kwargs):
        """Call the Sharp_Boe HTTP API for chat completions."""
        # Expect model format "sharp_boe/<model_name>"
        try:
            _, model_name = model.split("/", 1)
        except ValueError:
            raise ValueError(f"Invalid custom model string: {model!r}")
        url = f"{self.API_URL}/{model_name}/completions"
        headers = {"Authorization": f"Bearer {self.secret}"}
        payload = {"messages": messages, **kwargs}
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()
'''
        # Insert before existing chat_completion definition
        text = re.sub(
            r"(def chat_completion\s*\()",
            custom_class + r"\n\1",
            text,
            count=1,
        )
        changed = True

    # 3) Patch chat_completion to route sharp_boe models
    pattern = r"(_model = model or _DEFAULT_MODEL)"
    if 'startswith("sharp_boe/"' not in text:
        # After setting _model, add dispatch
        replacement = r"""\1
    # route custom Sharp_Boe provider
    if _model.startswith("sharp_boe/"):
        return MyCustomLLM().completion(_model, messages, **kwargs)
"""
        text = re.sub(pattern, replacement, text, count=1)
        changed = True

    if changed:
        llm_router_path.write_text(text, encoding="utf-8")
        print(f"Patched llm_router at {llm_router_path}")
    else:
        print("llm_router.py already patched; no changes made.")


def add_custom_provider_test():
    test_dir = REPO / "tests"
    test_file = test_dir / "test_custom_sharp_boe.py"
    if test_file.exists():
        print(f"Test file {test_file} already exists; skipping creation.")
        return

    test_code = '''# Copyright © 2025
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
        calls['url'] = url
        calls['json'] = json
        calls['headers'] = headers
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
'''
    test_file.write_text(test_code, encoding="utf-8")
    print(f"Created new test file {test_file}")


def main():
    patch_llm_router()
    add_custom_provider_test()
    print(
        "\nDone patching Chunk-4 (Custom provider sharp_boe).\n"
        "Next steps:\n"
        "1. Ensure 'requests' is available in your environment (it's a project dependency).\n"
        "2. Run `pytest tests/test_custom_sharp_boe.py tests/test_llm_router.py` to verify custom provider integration.\n"
        "3. Run full test suite to catch regressions: `pytest`.\n"
        "4. If all tests pass, commit changes and proceed to Chunk-5 (docs & cleanup)."
    )


if __name__ == "__main__":
    main()
