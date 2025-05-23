# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/6.1.1.py

"""
patch_chunk_2.py  – Milestone *LiteLLM Integration*  (Chunk-2)

Apply **in-place** edits so that:

• YAML schema accepts optional `model:` field
• `load_config()` now robustly dedents YAML (fixes ScannerError in tests)
• run-time plumbing passes the value down into `vibe_utils.get_vibed`
• `vibe_utils` hardens typing + default handling for the new argument
• mypy complaint about str|None fixed

Run via:  `python patch_chunk_2.py`
This script is **idempotent** – repeated executions re-write the same
sections without duplication.
"""
from __future__ import annotations

import re
import textwrap
from pathlib import Path
from typing import Callable

from personalvibe import vibe_utils
from personalvibe.vibe_utils import get_base_path

REPO = get_base_path()  # project root
SRC = REPO / "src" / "personalvibe"


def _patch(path: Path, modifier: Callable[[str], str]) -> None:
    txt = path.read_text(encoding="utf-8")
    new = modifier(txt)
    if new != txt:
        path.write_text(new, encoding="utf-8")


# ---------------------------------------------------------------------------
# 1)  ConfigModel: add `model` field + validator
# ---------------------------------------------------------------------------
def _update_run_pipeline(txt: str) -> str:
    # a) add import
    if "import re" not in txt:
        txt = txt.replace("from pathlib import Path", "import re\nfrom pathlib import Path")

    # b) insert model field inside ConfigModel if missing
    if "model: str" not in txt:
        pat = r"class ConfigModel\(BaseModel\):(.+?)conversation_history"
        m = re.search(pat, txt, flags=re.S)
        if not m:
            raise RuntimeError("ConfigModel block not located")
        block = m.group(0)
        indent = " " * 4
        new_line = f'{indent}model: str = ""  # provider/model, e.g. openai/gpt-4o-mini\n'
        block = block.replace("code_context_paths: List[str]\n", "code_context_paths: List[str]\n" + new_line)
        txt = txt.replace(m.group(0), block)

    # c) add validator only once
    if "validate_model(" not in txt:
        validator_code = textwrap.dedent(
            """
                # --- field validation --------------------------------------------------
                @field_validator("model", mode="before")
                def validate_model(cls, v: str):  # noqa: D401,N805
                    if v in ("", None):
                        return ""
                    if isinstance(v, str) and re.match(r"^[^/]+/.+$", v.strip()):
                        return v.strip()
                    raise ValueError("model must be <provider>/<model_name>")
            """
        )
        txt = txt.replace("class ConfigModel(BaseModel):", "class ConfigModel(BaseModel):" + validator_code)

    # d) pass model through get_vibed call
    if "model=config.model" not in txt:
        txt = txt.replace(
            "vibe_utils.get_vibed(",
            "vibe_utils.get_vibed(",
        )
        # replace args block – naive but safe because call appears once
        call_pat = r"vibe_utils\.get_vibed\([^\)]*\)"
        call_match = re.search(call_pat, txt, flags=re.S)
        if call_match:
            call_block = call_match.group(0)
            if "model=" not in call_block:
                new_block = call_block[:-1] + ",\n            model=(config.model or None),\n        )"
                txt = txt.replace(call_block, new_block)
    # e) dedent YAML text in load_config
    if "textwrap.dedent" not in txt:
        txt = txt.replace(
            "_yaml_txt = sanitize_yaml_text(f.read(), origin=config_path)",
            "_raw = f.read()\n            _yaml_txt = textwrap.dedent(_raw)\n            _yaml_txt = sanitize_yaml_text(_yaml_txt, origin=config_path)",
        )
        if "import textwrap" not in txt:
            txt = txt.replace("import logging", "import logging\nimport textwrap")
    return txt


_patch(SRC / "run_pipeline.py", _update_run_pipeline)


# ---------------------------------------------------------------------------
# 2)  vibe_utils.get_vibed & helpers – accept Optional[str]
# ---------------------------------------------------------------------------
def _update_vibe_utils(txt: str) -> str:
    # a) widen typing in signature
    txt = txt.replace('model: str = "o3"', "model: str | None = None")

    # b) defaulting logic (inside function) – ensure only 1 replacement
    if 'model = model or "o3"' not in txt:
        txt = txt.replace(
            "message_tokens = num_tokens(str(messages), model=model)",
            '    model = model or "o3"\n    message_tokens = num_tokens(str(messages), model=model)',
        )

    # c) openai call currently uses 'model' variable – already fine

    # d) num_tokens helper accept None
    if 'def num_tokens(text: str, model: str = "o3")' in txt:
        txt = txt.replace(
            'def num_tokens(text: str, model: str = "o3") -> int:',
            "def num_tokens(text: str, model: str | None = None) -> int:",
        )
        txt = txt.replace(
            "enc = tiktoken.encoding_for_model(model)",
            'enc = tiktoken.encoding_for_model(model or "o3")',
        )
    return txt


_patch(SRC / "vibe_utils.py", _update_vibe_utils)


# ---------------------------------------------------------------------------
# 3)  mypy complaint came from mismatch in param – no code change needed
#     beyond the edits above.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 4)  print helpful next-step guidance
# ---------------------------------------------------------------------------
print(
    """
✅  Chunk-2 patch applied.

Key changes
-----------
• ConfigModel gains optional `model` + regex validation (<provider>/<model>)
• load_config() now textwrap.dedent()s raw YAML to tolerate indented fixtures
• run_pipeline passes the value down to vibe_utils.get_vibed(model=…)
• vibe_utils.get_vibed / num_tokens accept None and fallback to "o3"
• mypy arg-type error resolved

Next steps
----------
1. Run the full quality-gate:
        bash tests/personalvibe.sh
   All previously failing tests (model schema + mypy) should pass.

2. Verify manual CLI flow, e.g.:
        pv run --config examples/hello_world.yaml --prompt_only
   Behaviour remains identical if `model:` omitted.

3. Proceed to Chunk-3 (replace direct OpenAI call with llm_router).

"""
)
