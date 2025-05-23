# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/6.1.2.py

"""
chunk_3_patch.py  –  Personalvibe milestone “LiteLLM Integration”, Chunk-3

Run with:
    poetry run python chunk_3_patch.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()


def _patch_vibe_utils() -> None:
    tgt = REPO / "src" / "personalvibe" / "vibe_utils.py"
    txt = tgt.read_text(encoding="utf-8").splitlines()

    new_lines: list[str] = []
    skip_block = False
    for ln in txt:
        # -----------------------------------------------------------------
        # 1) drop openai-specific boot-strap & client
        # -----------------------------------------------------------------
        if re.search(r"from +openai", ln):
            continue  # kill import
        if "OPENAI_API_KEY" in ln or "client = OpenAI" in ln:
            continue  # kill legacy key boot-strap + client
        if 'os.environ["OPENAI_API_KEY"]' in ln:
            continue
        # -----------------------------------------------------------------
        # 2) ensure llm_router import (once, idempotent)
        # -----------------------------------------------------------------
        if "import tiktoken" in ln and "llm_router" not in txt:
            new_lines.append(ln)
            new_lines.append("from personalvibe import llm_router  # ← LiteLLM shim (chunk-3)")
            continue
        # -----------------------------------------------------------------
        # 3) replace the OpenAI create() call with llm_router.chat_completion
        # -----------------------------------------------------------------
        if "client.chat.completions.create" in ln:
            # Skip the multiline old call until the line containing ".message.content"
            skip_block = True
            new_lines.append(
                "    resp = llm_router.chat_completion("
                "\n        model=model,"
                "\n        messages=messages,"
                "\n        max_tokens=max_completion_tokens,"
                "\n    )"
            )
            new_lines.append("    response = resp['choices'][0]['message']['content']")
            continue

        if skip_block:
            if ".message.content" in ln:
                skip_block = False
            continue  # drop old block lines

        new_lines.append(ln)

    # ---------------------------------------------------------------------
    # Insert llm_router import if not already present
    # ---------------------------------------------------------------------
    if not any("import llm_router" in l for l in new_lines):
        for idx, l in enumerate(new_lines):
            if l.startswith("import tiktoken"):
                new_lines.insert(idx + 1, "from personalvibe import llm_router  # ← LiteLLM shim (chunk-3)")
                break

    tgt.write_text("\n".join(new_lines), encoding="utf-8")


def _add_test() -> None:
    """Create a new test ensuring get_vibed routes via llm_router."""
    test_path = REPO / "tests" / "test_get_vibed_router.py"
    if test_path.exists():
        return  # idempotent

    test_path.write_text(
        '''
# Copyright © 2025 by Nick Jenkins. All rights reserved
"""Chunk-3 regression: vibe_utils.get_vibed must call llm_router.chat_completion."""

from types import SimpleNamespace
from pathlib import Path

from personalvibe import vibe_utils, llm_router


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
''',
        encoding="utf-8",
    )


def main() -> None:
    _patch_vibe_utils()
    _add_test()


if __name__ == "__main__":
    main()
    print(
        """
🔧  Chunk 3 patch applied successfully.

WHAT CHANGED
============
1. src/personalvibe/vibe_utils.py
   • Removed all OpenAI-specific code (import, API-key bootstrap, client creation).
   • Added `from personalvibe import llm_router` import.
   • get_vibed() now calls
       llm_router.chat_completion(model, messages, max_tokens=…)
     and extracts `choices[0]['message']['content']`.
   • OPENAI_API_KEY fallback logic deleted – LiteLLM will locate
     provider credentials via its own env-var conventions.

2. tests/test_get_vibed_router.py  (NEW)
   • Verifies that get_vibed() delegates to llm_router by monkey-patching
     the helper and checking call params + returned content.

IDEMPOTENCY
-----------
Running this script again is safe:
 • Import insertion checks for duplicates.
 • New test creation is skipped when file already exists.
 • OpenAI removal patterns simply ignore absent lines.

NEXT STEPS
----------
• `poetry run nox -s tests` – all suites (including new one) must pass.
• Observe that **no** network calls hit OpenAI; litellm is fully mocked.
• Chunk 4 will introduce a custom provider and register it inside
  personalvibe/llm_router.py.

"""
    )
