# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/6.0.1.py

"""
personalvibe_chunk_1.py  –  Sprint “LiteLLM shim & dependency”

This idempotent patch script:

1. Adds  `litellm>=1.40`  into pyproject.toml (if missing)
2. Creates  src/personalvibe/llm_router.py  with the first-pass wrapper
3. Adds   tests/test_llm_router.py   (unit tests using monkey-patch)

Run via:

    poetry run python personalvibe_chunk_1.py
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from textwrap import dedent

# -----------------------------------------------------------------------------
#  Locate repo-root (works from *any* working directory)
from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()
SRC = REPO / "src" / "personalvibe"
TESTS = REPO / "tests"


# -------------------------------------------------------------------- helpers
def _insert_dependency(pyproject: Path, dep_line: str) -> None:
    """Insert *dep_line* under `[tool.poetry.dependencies]` if absent."""
    text = pyproject.read_text(encoding="utf-8").splitlines()

    if any("litellm" in l for l in text):
        return  # already present – noop

    out: list[str] = []
    in_deps = False
    inserted = False
    for ln in text:
        out.append(ln)
        if ln.strip() == "[tool.poetry.dependencies]":
            in_deps = True
            continue
        if in_deps and ln.strip().startswith("python"):
            # insert *right after* python spec
            out.append(f'litellm = ">=1.40"')
            inserted = True
            in_deps = False  # avoid multiple insertions
    if not inserted:
        # Fallback – append near end of deps block
        for idx, ln in enumerate(out):
            if in_deps and ln.strip() == "":
                out.insert(idx, f'litellm = ">=1.40"')
                inserted = True
                break
            if ln.strip() == "[tool.poetry.dependencies]":
                in_deps = True
    pyproject.write_text("\n".join(out) + "\n", encoding="utf-8")


def _create_llm_router(path: Path) -> None:
    if path.exists():
        return  # idempotent
    path.write_text(
        dedent(
            '''
            """Unified LiteLLM entry-point (Chunk-1).

            Public helper
            -------------
            chat_completion(model: str | None, messages: list, **kw) -> Any
                • `model` None / "" defaults to "openai/gpt-4o-mini"
                • Thin sync wrapper around `litellm.completion`
            """

            from __future__ import annotations

            import logging
            from typing import Any, Dict, List, Union

            import litellm  # runtime dependency injected by chunk-1

            _log = logging.getLogger(__name__)

            _DEFAULT_MODEL = "openai/gpt-4o-mini"

            # ------------------------------------------------------------------
            def chat_completion(
                *,
                model: Union[str, None] = None,
                messages: List[dict],
                **kwargs: Any,
            ) -> Any:
                """Route a chat completion through **LiteLLM**.

                Parameters
                ----------
                model
                    Provider/model string (e.g. "openai/gpt-4o-mini").
                    Falls back to `_DEFAULT_MODEL` when None / "".
                messages
                    List of OpenAI-style chat messages.
                **kwargs
                    Passed verbatim to `litellm.completion`.

                Returns
                -------
                The object returned by `litellm.completion` (sync).

                Raises
                ------
                ValueError
                    If `messages` is empty / not a list or model is invalid.
                """
                if not isinstance(messages, list) or not messages:
                    raise ValueError("messages must be a non-empty list")

                _model = model or _DEFAULT_MODEL
                if not isinstance(_model, str) or "/" not in _model:
                    # Very lenient – just catch blatant mistakes; real validation is
                    # delegated to LiteLLM which knows the registry.
                    raise ValueError(f"Invalid model string {_model!r}")

                _log.debug("llm_router → %s  (%d msgs)", _model, len(messages))

                try:
                    return litellm.completion(model=_model, messages=messages, **kwargs)
                except Exception as exc:  # noqa: BLE001
                    # LiteLLM raises many specialised errors; we re-raise untouched
                    _log.error("LiteLLM call failed: %s", exc)
                    raise
            '''
        ).lstrip(),
        encoding="utf-8",
    )


def _create_tests(path: Path) -> None:
    if path.exists():
        return
    path.write_text(
        dedent(
            '''
            # Copyright © 2025
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
                assert captured.kwargs["model"] == "openai/gpt-4o-mini"
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
            '''
        ).lstrip(),
        encoding="utf-8",
    )


def main() -> None:
    # 1. dependency ------------------------------------------------------
    _insert_dependency(REPO / "pyproject.toml", 'litellm = ">=1.40"')

    # 2. llm_router.py ---------------------------------------------------
    _create_llm_router(SRC / "llm_router.py")

    # 3. tests -----------------------------------------------------------
    _create_tests(TESTS / "test_llm_router.py")

    print(
        dedent(
            f"""
            ✅  Chunk-1 applied.

            WHAT CHANGED
            ------------
            • Added `litellm>=1.40` under [tool.poetry.dependencies] in pyproject.toml
            • New module  personalvibe.llm_router  with   chat_completion()   helper
            • New tests   tests/test_llm_router.py   mocking litellm.completion

            NEXT STEPS
            ----------
            1. Run   poetry install   (or rely on CI) to fetch LiteLLM.
            2. Execute full quality-gate:

                   bash tests/personalvibe.sh

               All tests – including the newly added shim tests – must pass.
            3. Proceed to **Chunk 2** once CI is green:

               • extend ConfigModel with optional `model` field
               • route it down to llm_router.chat_completion

            """
        ).strip()
    )


if __name__ == "__main__":
    main()
