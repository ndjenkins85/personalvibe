# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/4.4.0.py

"""
patch_semver_arg.py – Sprint 1

Adds **optional CLI argument** to `tests/personalvibe.sh` so callers can
explicitly pass the semver:

    bash tests/personalvibe.sh 4.1.4     # logs/4.1.4_base.log
    bash tests/personalvibe.sh           # auto-detect (unchanged)

Behaviour
---------
1. *If* the first positional argument is non-empty we treat it as the
   semver and skip the git branch inspection completely.
2. Otherwise we fall back to the previous logic (`vibed/<semver>` branch
   pattern, or “dev”).

The change is 100 % backward compatible – `nox -s vibed` still works
unchanged because it invokes the script **without** an argument.

Run this patch file once:

    poetry run python patch_semver_arg.py
"""

from __future__ import annotations

import re
from pathlib import Path

SCRIPT = Path("tests", "personalvibe.sh")
if not SCRIPT.exists():
    raise SystemExit(f"Error: {SCRIPT} not found – run from repo root.")

text = SCRIPT.read_text(encoding="utf-8")

# ------------------------------------------------------------------ locate
START_MARKER = "# Detect semver"
END_MARKER = "LOG_DIR="
m_start = text.find(START_MARKER)
m_end = text.find(END_MARKER)

if m_start == -1 or m_end == -1 or m_end < m_start:
    raise SystemExit("Unable to patch; markers not found in personalvibe.sh")

pre = text[:m_start]
post = text[m_end:]

# ---------------------------------------------------------------- new block
new_block = """# ------------------------------------------------------------------- #
# Detect semver (optional CLI arg OR from current git branch)
#   • First positional argument wins (allows: bash personalvibe.sh 4.1.4)
#   • Else fall back to vibed/<semver> branch pattern
#   • Defaults to 'dev' when neither is available
# ------------------------------------------------------------------- #
if [[ $# -ge 1 && -n "$1" ]]; then
  SEMVER="$1"
  shift                     # keep "$@" clean for potential future args
else
  BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")"
  if [[ "$BRANCH" =~ ^vibed\\/([^/]+)$ ]]; then
    SEMVER="${BASH_REMATCH[1]}"
  else
    SEMVER="${SEMVER:-dev}"
  fi
fi
"""

# keep newline alignment
if not new_block.endswith("\n"):
    new_block += "\n"

# ---------------------------------------------------------------- write
patched = pre + new_block + post
SCRIPT.write_text(patched, encoding="utf-8")

# print(f"✅ Patched {SCRIPT.relative_to(Path.cwd())}")
print("   • Now accepts optional semver argument:")
print("       bash tests/personalvibe.sh 4.1.4")
print("   • Existing calls without argument remain unchanged.")
print("\nYou can commit the changes with:")
print("   git add tests/personalvibe.sh && git commit -m 'feat: personalvibe.sh accepts semver arg'")
