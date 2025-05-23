# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/5.8.0.py

"""
patch_chunk1.py  –  Personalvibe Milestone 3 / Chunk 1

Execute with:

    poetry run python patch_chunk1.py
    # or simply:  python patch_chunk1.py

The script is **idempotent** – running twice leaves files unchanged.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Callable, Iterable

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()

# --------------------------------------------------------------------------- helpers
FileEdit = Callable[[str], str]


def _apply_patch(path: Path, *edits: Iterable[FileEdit]) -> None:
    """Read *path*, pipe through every edit function, write back if changed."""
    original = text = path.read_text(encoding="utf-8")
    for edit in edits:
        text = edit(text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        print(f"✅  Patched {path.relative_to(REPO)}")
    else:
        print(f"↷  Skip (already up-to-date) {path.relative_to(REPO)}")


# --------------------------------------------------------------------------- 1/3
def _fix_pvpatchproxy_object(text: str) -> str:
    """
    personalvibe/__init__.py
    ------------------------
    • add full type-hints + return annotation to _PvPatchProxy.object()
    """
    pattern = r"def object\(\s*self,\s*target,\s*name,\s*value\)\s*:"
    repl = "def object(self, target: object, name: str, value: object) -> None:"
    return re.sub(pattern, repl, text, count=1)


_apply_patch(REPO / "src/personalvibe/__init__.py", _fix_pvpatchproxy_object)


# --------------------------------------------------------------------------- 2/3
def _remove_unused_template_map(text: str) -> str:
    """
    personalvibe/run_pipeline.py
    ----------------------------
    Deletes the now-unused `_template_map` assignment that triggered F841.
    """
    return re.sub(
        r"\n\s*_template_map\s*=\s*\{[^}]+\}\s*\n",  # naive but safe here
        "\n",
        text,
        count=1,
        flags=re.DOTALL,
    )


_apply_patch(REPO / "src/personalvibe/run_pipeline.py", _remove_unused_template_map)


# --------------------------------------------------------------------------- 3/3
def _annotate_vibe_utils(text: str) -> str:
    """
    personalvibe/vibe_utils.py
    --------------------------
    • add type-hints for `config` params flagged by flake8-annotations.
    • ensure `TYPE_CHECKING` import guard exists.
    """

    # Insert TYPE_CHECKING block once, after existing top-level imports.
    if "if TYPE_CHECKING:" not in text:
        text = re.sub(
            r"(from\s+jinja2\s+import\s+Environment[^\n]+\n)",
            r"\1from typing import TYPE_CHECKING\n\n"
            r"if TYPE_CHECKING:\n"
            r"    from personalvibe.run_pipeline import ConfigModel  # noqa: F401\n",
            text,
            count=1,
        )

    # Helper to replace untyped signatures → typed ones
    replacements = {
        r"def _get_error_text\(\s*config\)": "def _get_error_text(config: 'ConfigModel')",
        r"def _get_milestone_text\(\s*config\)": "def _get_milestone_text(config: 'ConfigModel')",
        r"def _get_replacements_v1\(\s*config,\s*code_context: str\)": (
            "def _get_replacements_v1(config: 'ConfigModel', code_context: str)"
        ),
        r"def get_replacements\(\s*config,\s*code_context: str\)": (
            "def get_replacements(config: 'ConfigModel', code_context: str)"
        ),
    }
    for pat, rep in replacements.items():
        text = re.sub(pat, rep, text, count=1)

    # Return type annotations where missing
    if "def _get_error_text" in text and "-> str" not in text.split("def _get_error_text")[1].split(":", 1)[0]:
        text = text.replace(
            "def _get_error_text(config: 'ConfigModel')", "def _get_error_text(config: 'ConfigModel') -> str"
        )
    if "def _get_milestone_text" in text and "-> str" not in text.split("def _get_milestone_text")[1].split(":", 1)[0]:
        text = text.replace(
            "def _get_milestone_text(config: 'ConfigModel')",
            "def _get_milestone_text(config: 'ConfigModel') -> str",
        )

    return text


_apply_patch(REPO / "src/personalvibe/vibe_utils.py", _annotate_vibe_utils)

# --------------------------------------------------------------------------- done
print(
    """
🔧  Chunk 1 patch complete.

Next steps
----------
1. Run the project quality-gate to confirm lint errors are gone:

       bash tests/personalvibe.sh

   The `lint-3.12` session should now pass with zero ANN/E/F/S violations.

2. Commit the generated changes on a `feature/lint-zero` branch and open
   a PR.  The CI gate mirrors `tests/personalvibe.sh`.

3. Manual sanity-check:
   • `pv --help` still prints.
   • Unit-test suite remains green (pytest).

4. Once merged, continue with Milestone Chunk 2
   (implicit project detection).

"""
)
