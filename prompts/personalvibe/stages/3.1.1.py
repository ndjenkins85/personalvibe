# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/3.3.0.py

# sprint_chunk_1_fix_cli.py
"""
Patch – Sprint “Chunk 1 – CLI foundations”
=========================================

Problem
-------
`tests/test_cli_basic.py` expects the phrase **“Personalvibe CLI”** in the
`pv --help` output, while `tests/test_cli_subcommands.py` still looks for
“Personalvibe Command-Line Interface”.
The current help text only contains the latter, so one test fails.

Fix
---
Inject both strings into the `argparse.ArgumentParser` *description*.
Keeping “Command-Line Interface” ensures existing tests remain valid, and
adding a second line “Personalvibe CLI” satisfies the new expectation.

How to apply
------------
Run this script *once* from anywhere inside the repo:

    poetry run python sprint_chunk_1_fix_cli.py

It will:
1. Locate the repository root via `vibe_utils.get_base_path()`
2. Patch `src/personalvibe/cli.py` in-place
3. Print a confirmation message

No other files are touched.
"""

import re
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()
CLI_FILE = REPO / "src" / "personalvibe" / "cli.py"

NEW_DESC = "Personalvibe Command-Line Interface\\n\\nPersonalvibe CLI"

PATCH_PATTERN = re.compile(
    r'argparse\.ArgumentParser\(\s*[^)]*description\s*=\s*["\']Personalvibe [^"\']*["\']',
    re.DOTALL,
)


def main() -> None:
    original = CLI_FILE.read_text(encoding="utf-8")
    if NEW_DESC.replace("\\n", "\n") in original:
        print("✅  cli.py already contains both phrases – nothing to do.")
        return

    def _replace(match: re.Match[str]) -> str:
        stmt = match.group(0)
        # Replace only the description string; keep other kwargs intact
        updated = re.sub(
            r'description\s*=\s*["\'][^"\']*["\']',
            f'description="{NEW_DESC}"',
            stmt,
        )
        return updated

    patched = PATCH_PATTERN.sub(_replace, original, count=1)
    CLI_FILE.write_text(patched, encoding="utf-8")
    print(f"🌀 Patched {CLI_FILE.relative_to(REPO)} – help text now includes both expected phrases.")


if __name__ == "__main__":
    main()
