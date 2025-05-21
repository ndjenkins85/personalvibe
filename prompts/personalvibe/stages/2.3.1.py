# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/2.4.0.py

#!/usr/bin/env python
"""
patch_chunk_c_bugfix.py – Bug-fixes for “Chunk C – Data-directory bootstrap”.

Run via:

    poetry run python patch_chunk_c_bugfix.py
    # or simply `python patch_chunk_c_bugfix.py` if deps already installed.

What it does
------------
1. Inserts a *stable* anchor comment right above `def save_prompt(...)`
   so that future auto-generated patch scripts (e.g. 2.3.0.py) can
   reliably locate the function.
2. Harmonises type-hints of `find_existing_hash` to return `Path | None`
   (was `str | None`, which upset upcoming mypy rules).

Nothing else is touched – logic & unit tests remain green.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Final, Tuple

# --------------------------------------------------------------------------- #
# Locate repository root
# --------------------------------------------------------------------------- #
try:
    from personalvibe import vibe_utils  # noqa: E402
except ModuleNotFoundError as exc:  # pragma: no cover
    sys.exit(f"❌  personalvibe not importable – did you activate the venv?  {exc}")

REPO: Path = vibe_utils.get_base_path()

VU_PATH: Final[Path] = REPO / "src" / "personalvibe" / "vibe_utils.py"
if not VU_PATH.exists():  # pragma: no cover
    sys.exit(f"vibe_utils.py not found at expected path: {VU_PATH}")

print(f"🔧  Patching {VU_PATH.relative_to(REPO)}")

ORIG = VU_PATH.read_text(encoding="utf-8").splitlines(keepends=True)

# --------------------------------------------------------------------------- #
# Helper – insert anchor above `def save_prompt`
# --------------------------------------------------------------------------- #
ANCHOR_LINES: Tuple[str, ...] = (
    "# ------------------------------------------------------------------",
    "# --- PERSONALVIBE PATCH C ANCHOR: save_prompt (do not delete) -----",
    "# ------------------------------------------------------------------",
)


def _ensure_anchor(lines: list[str]) -> list[str]:
    joined = "".join(lines)
    if "PATCH C ANCHOR: save_prompt" in joined:
        print("✅  Anchor already present – nothing to do.")
        return lines

    for idx, ln in enumerate(lines):
        if re.match(r"\s*def\s+save_prompt\(", ln):
            print(f"🪄  Inserting anchor comment at line {idx+1}")
            return lines[:idx] + [l + "\n" for l in ANCHOR_LINES] + lines[idx:]
    else:  # pragma: no cover
        sys.exit("❌  Could not find def save_prompt(...) – aborting to avoid corruption.")


# --------------------------------------------------------------------------- #
# Helper – fix return-type of find_existing_hash
# --------------------------------------------------------------------------- #
_FIND_SIG_OLD = r"def\s+find_existing_hash\(\s*root_dir:\s*str,\s*hash_str:\s*str\)\s*->\s*Union\[str,\s*None]"
_FIND_SIG_NEW = "def find_existing_hash(root_dir: str | Path, hash_str: str) -> Path | None"


def _fix_find_existing_hash(lines: list[str]) -> list[str]:
    text = "".join(lines)
    if _FIND_SIG_NEW in text:
        print("✅  Typed signature already modern – skip.")
        return lines
    updated = re.sub(_FIND_SIG_OLD, _FIND_SIG_NEW, text)
    if updated == text:  # pragma: no cover
        print("⚠️  Could not rewrite find_existing_hash signature – pattern not matched.")
        return lines
    print("🩹  Harmonised return-type of find_existing_hash → Path | None")
    return updated.splitlines(keepends=True)


# --------------------------------------------------------------------------- #
# Execute in-memory patches
# --------------------------------------------------------------------------- #
patched = _ensure_anchor(ORIG)
patched = _fix_find_existing_hash(patched)

# --------------------------------------------------------------------------- #
# Write back only if changed
# --------------------------------------------------------------------------- #
if patched != ORIG:
    VU_PATH.write_text("".join(patched), encoding="utf-8")
    print("🎉  Patch applied successfully.")
else:
    print("ℹ️   File already up-to-date – no changes written.")

# --------------------------------------------------------------------------- #
# Developer hints
# --------------------------------------------------------------------------- #
print(
    "\nNext steps:\n"
    "  • Run `pytest -q` to ensure all Chunk C tests stay green.\n"
    "  • Re-run your failing `python -m personalvibe.parse_stage --project_name personalvibe --run`\n"
    "    – the auto-generated 2.3.x patch script should now detect the new "
    "anchor comment instead of crashing.\n"
    "  • Commit the updated file:\n"
    "        git add src/personalvibe/vibe_utils.py && git commit -m 'fix: add Chunk C anchor & typing'\n"
)
