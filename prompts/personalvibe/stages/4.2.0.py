# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/4.2.0.py

"""
personalvibe_sprint_patch_chunk_b.py

Sprint: “Independence Day” – Chunk B
Task : Once deps are correct, tidy up the automation entry-points.

Goal for this patch
───────────────────
1. Update the *locations* tuple in **noxfile.py** so that follow-up
   auto-patchers (e.g. `pv parse-stage …`) can reliably locate it.
   • The pattern they look for is   locations = (<tuple>)
   • The current file missed the explicit parentheses which broke the
     regex → RuntimeError in earlier runs.

2. Keep the change minimal – we do NOT delete any sessions or behaviour
   yet (that will come in later clean-ups).  We simply ensure the
   canonical tuple is present exactly once in the preferred format.

What this script does
────────────────────
• Locates the repository root via personalvibe.vibe_utils.
• Reads *noxfile.py*, patches the first assignment line that starts
  with “locations =”.
• Writes back the modified file.
• Creates a tiny marker file “logs/patch_chunk_b.ok” so CI can check.

Run it via:

    poetry run python personalvibe_sprint_patch_chunk_b.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from personalvibe import vibe_utils

# --------------------------------------------------------------------- helpers
REPO = vibe_utils.get_base_path()
NOXFILE = REPO / "noxfile.py"

NEW_TUPLE_TEXT = 'locations = ("src/personalvibe", "tests", "noxfile.py", "docs/conf.py")\n'


def patch_locations() -> None:
    """Ensure `locations = (... )` tuple uses parentheses."""
    if not NOXFILE.exists():
        print(f"❌  noxfile.py not found at {NOXFILE}", file=sys.stderr)
        sys.exit(1)

    text = NOXFILE.read_text(encoding="utf-8").splitlines(keepends=True)
    out_lines: list[str] = []

    patched = False
    for line in text:
        if re.match(r"\s*locations\s*=", line) and "(" not in line:
            out_lines.append(NEW_TUPLE_TEXT)
            patched = True
        else:
            out_lines.append(line)

    if not patched:
        # Maybe it already looks correct; make sure exactly one canonical line
        occurrences = [i for i, ln in enumerate(text) if re.match(r"\s*locations\s*=", ln)]
        if len(occurrences) == 1 and "(" in text[occurrences[0]]:
            print("ℹ️  locations tuple already formatted – no changes made.")
            return
        else:
            print("❌  Could not locate simple `locations =` assignment to patch.", file=sys.stderr)
            sys.exit(2)

    NOXFILE.write_text("".join(out_lines), encoding="utf-8")
    print(f"✅  Patched locations tuple in {NOXFILE.relative_to(REPO)}")


def main() -> None:
    patch_locations()

    # simple success marker so CI / manual runs can verify quickly
    marker = REPO / "logs" / "patch_chunk_b.ok"
    marker.parent.mkdir(exist_ok=True)
    marker.write_text("OK", encoding="utf-8")
    print(f"📄  Wrote marker {marker}")


if __name__ == "__main__":
    main()
