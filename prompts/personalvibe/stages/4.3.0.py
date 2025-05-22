# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/4.3.0.py

#!/usr/bin/env python
"""
Sprint 3 – Chunk C
==================

Consolidate the *quality-gate* so **one single entry-point** (tests/personalvibe.sh)
runs *all* critical sessions:

    1)  poetry install --sync --no-root
    2)  poetry run nox -rs lint tests smoke_dist

The bash script already installs deps & forwards output into the log file,
therefore we only have to **rewrite its core** and set executable bits.

Nothing else in the repository needs to change – the existing nox sessions
(lint / tests / smoke_dist) are green, and the vibed workflow continues to
delegate to the same script, so downstream tests keep passing.

Run this patch script from anywhere inside the repo tree:

    python sprint_chunk_c_patch.py
"""
from __future__ import annotations

import os
import stat
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()
SCRIPT = REPO / "tests" / "personalvibe.sh"

NEW_CONTENT = r"""#!/usr/bin/env bash
# tests/personalvibe.sh  —  consolidated quality-gate (Chunk C)
#
# Purpose:
#   • install *runtime* deps (`--no-root`) so wheel-building works
#   • delegate to **nox** for the actual quality-gate
#   • append *all* stdout/stderr to    logs/<semver>_base.log
#
# Sessions executed:
#   nox -rs lint tests smoke_dist
#
# Behaviour:
#   • `set -euo pipefail` → any failure exits non-zero (CI-friendly)
#   • first positional arg overrides the <semver> used for the log file
#   • keeps backward-compat banners so existing tests don’t break
set -euo pipefail

### ---------- derive SEMVER for log routing ---------------------------------
if [[ $# -ge 1 && -n "$1" ]]; then
  SEMVER="$1"; shift
else
  BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")"
  if [[ "$BRANCH" =~ ^vibed\/([^/]+)$ ]]; then
    SEMVER="${BASH_REMATCH[1]}"
  else
    SEMVER="${SEMVER:-dev}"
  fi
fi

LOG_DIR="logs"
LOG_FILE="${LOG_DIR}/${SEMVER}_base.log"
mkdir -p "${LOG_DIR}"
touch "${LOG_FILE}"

# Duplicate *everything* to the semver log (append mode)
exec > >(tee -a "${LOG_FILE}") 2>&1

echo "🔍  Installing project dependencies (poetry)…"
poetry install --sync --no-interaction --no-root

echo -e "\n🧹  Running quality-gate via nox (lint + tests + smoke_dist)…"
poetry run nox -rs lint tests smoke_dist "$@"

echo -e "\n✅  personalvibe.sh finished ok."
"""


def main() -> None:
    SCRIPT.parent.mkdir(parents=True, exist_ok=True)
    SCRIPT.write_text(NEW_CONTENT, encoding="utf-8")

    # Ensure executable bit is set (755)
    cur_mode = SCRIPT.stat().st_mode
    SCRIPT.chmod(cur_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print(f"✅  Re-wrote {SCRIPT.relative_to(REPO)} and ensured it is executable.")
    print("\nNext steps:")
    print("  • `bash tests/personalvibe.sh`        # manual smoke-run")
    print("  • `nox -s vibed -- 2.1.0`             # end-to-end quality-gate")


if __name__ == "__main__":
    main()
