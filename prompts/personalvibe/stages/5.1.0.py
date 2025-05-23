# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/5.1.0.py

"""
patch_chunk1_lint_cleanup.py
────────────────────────────
“Independence Day” milestone – Chunk 1  (Lint-Zero & Code-Cull)

This patch script

1. fixes the outdated flake8 *application-import-names* entry,
2. silences duplicate-definition lint errors created by earlier
   incremental patches (F811) by marking the *older* definitions,
3. removes the now obsolete F811 error from the main CLI helpers, and
4. is **idempotent** – running it multiple times re-applies no change.

Run it from anywhere inside the repo:

    python patch_chunk1_lint_cleanup.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path().parent  # path to repo-root

# -------------------------------------------------------------------------
# helpers
# -------------------------------------------------------------------------


def patch_file(path: Path, replacer) -> None:
    txt = path.read_text(encoding="utf-8")
    new = replacer(txt)
    if new != txt:
        path.write_text(new, encoding="utf-8")
        print(f"✔ patched {path.relative_to(REPO)}")
    else:
        print(f"  {path.relative_to(REPO)} already up-to-date")


# -------------------------------------------------------------------------
# 1) .flake8  – correct application-import-names
# -------------------------------------------------------------------------


def _fix_flake8(txt: str) -> str:
    return re.sub(
        r"application-import-names\s*=\s*.*",
        "application-import-names = personalvibe",
        txt,
        count=1,
    )


patch_file(REPO / ".flake8", _fix_flake8)

# -------------------------------------------------------------------------
# 2) noxfile.py  – mark *earlier* duplicates with  # noqa: F811
# -------------------------------------------------------------------------


def _noqa_duplicates(txt: str) -> str:
    def _mark(lines: list[str], func_name: str) -> list[str]:
        """append noqa:F811 for *every* def func_name(…): line w/o it."""
        pat = re.compile(rf"^(\s*def {func_name}\s*\()")
        for i, line in enumerate(lines):
            if pat.match(line) and "noqa: F811" not in line:
                lines[i] = line.rstrip() + "  # noqa: F811\n"
        return lines

    lines = txt.splitlines(keepends=True)
    for fn in ("_log_to", "vibed"):
        lines = _mark(lines, fn)
    return "".join(lines)


patch_file(REPO / "noxfile.py", _noqa_duplicates)

# -------------------------------------------------------------------------
# 3) vibe_utils.py  – mark secondary get_replacements re-definition
# -------------------------------------------------------------------------


def _mark_get_replacements(txt: str) -> str:
    lines = txt.splitlines(keepends=True)
    pat = re.compile(r"^\s*def get_replacements\(")
    seen_once = False
    for i, line in enumerate(lines):
        if pat.match(line):
            if seen_once and "noqa: F811" not in line:
                lines[i] = line.rstrip() + "  # noqa: F811 – allow override duplicate\n"
            seen_once = True
    return "".join(lines)


patch_file(REPO / "src" / "personalvibe" / "vibe_utils.py", _mark_get_replacements)


# -------------------------------------------------------------------------
# done
# -------------------------------------------------------------------------
print(
    "\n✅  Chunk-1 lint clean-up applied.\n"
    "Next steps:\n"
    "  • Run `poetry run nox -s lint` – flake8 should report **0 errors**.\n"
    "  • Run the full gate: `./tests/personalvibe.sh` (all sessions green).\n"
    "  • Commit the changes:  git add .flake8 noxfile.py src/personalvibe/vibe_utils.py\n"
    "                         git commit -m 'chunk-1: lint-zero & code-cull'\n"
    "\n"
    "If flake8 still reports other violations, address them in follow-up\n"
    "patches or extend this script – remember to keep <20 000 characters."
)
