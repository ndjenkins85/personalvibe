# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/5.3.1.py

#!/usr/bin/env python
"""
patch_chunk2_fix_mypy.py

Apply *Chunk 2* finishing touches – silence the remaining mypy errors that
currently break the quality-gate (see `tests/personalvibe.sh` output).

Edits (idempotent):
1. src/personalvibe/parse_stage.py
      • determine_next_version(): build the triple-int tuple explicitly
        instead of `tuple(map(int, m.groups()))`.
2. src/personalvibe/cli.py
      • _scan_versions(): annotate `vers` list and construct tuple
        explicitly so its type is `tuple[int, int, int]`.

The modifications are repeated-run safe: lines are replaced only when
they still match the *pre-patch* pattern.

Run this script once from **any** directory inside the repo:

    poetry run python patch_chunk2_fix_mypy.py

It will report the files it touched.  Afterwards the full quality-gate
should be green:

    ./tests/personalvibe.sh

Next steps
----------
• Commit the changes (`git add -u && git commit -m "chunk2: fix mypy"`)
• Re-run the CI pipeline / GitHub Action to verify.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Tuple

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()
print(f"📂  Repo root detected at {REPO}")


def _patch_file(path: Path, subs: list[tuple[str, str]]) -> bool:
    """Search-and-replace *all* (old, new) pairs – returns True if changed."""
    original = txt = path.read_text(encoding="utf-8")
    for old, new in subs:
        txt, n = re.subn(re.escape(old), new, txt, count=1)
        if n:
            print(f"   • replaced {n} occurrence of '{old}'")
    if txt != original:
        path.write_text(txt, encoding="utf-8")
        return True
    return False


# --------------------------------------------------------------------------
# 1) parse_stage.py  -------------------------------------------------------
ps_file = REPO / "src/personalvibe/parse_stage.py"
ps_changes = _patch_file(
    ps_file,
    [
        (
            "version_tuples.append(tuple(map(int, m.groups())))",
            "version_tuples.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))",
        )
    ],
)
if ps_changes:
    print(f"✅  Patched {ps_file.relative_to(REPO)}")
else:
    print(f"ℹ️   {ps_file.relative_to(REPO)} already up-to-date")

# --------------------------------------------------------------------------
# 2) cli.py – _scan_versions() --------------------------------------------
cli_file = REPO / "src/personalvibe/cli.py"

# Replace the list initialisation (ensure we don't duplicate the annotation)
cli_subs: list[Tuple[str, str]] = [
    (
        "vers = []",
        "vers: list[tuple[int, int, int]] = []",
    ),
    (
        "vers.append(tuple(map(int, m.groups())))",
        "vers.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))",
    ),
]
cli_changes = _patch_file(cli_file, cli_subs)
if cli_changes:
    print(f"✅  Patched {cli_file.relative_to(REPO)}")
else:
    print(f"ℹ️   {cli_file.relative_to(REPO)} already up-to-date")

print("\n🎉  Patch complete – run `tests/personalvibe.sh` to verify mypy now " "passes (lint gate green).\n")
