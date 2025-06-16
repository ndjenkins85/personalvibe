# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/8.1.0.py

"""
streamline_patch.py

Deletes dead helper `_log_to_legacy` from noxfile.py and removes the now-unused
`Iterator` import.  This eliminates ~65 lines (>1 % of repo) without touching
any public API or tests.
"""

from __future__ import annotations

import re
from pathlib import Path
from textwrap import dedent

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()
NOXFILE = REPO / "noxfile.py"


def _drop_log_to_legacy(code: str) -> str:
    """
    Remove the entire @contextmanager def _log_to_legacy(...) block.
    Implementation: crude but safe line-based scan – we delete from the
    decorator line *inclusive* up to (but **not** including) the first
    `def _log_to(` that follows.
    """
    lines = code.splitlines(keepends=True)
    start, end = None, None
    for i, ln in enumerate(lines):
        if start is None and "@contextmanager" in ln and "_log_to_legacy" in lines[i + 1]:
            start = i  # include decorator
            continue
        if start is not None and "def _log_to(" in ln:
            end = i
            break
    if start is not None and end is not None:
        del lines[start:end]
    return "".join(lines)


def _prune_iterator_import(code: str) -> str:
    """
    Drop the unused typing.Iterator import from the `import` stanza.
    """
    return re.sub(r",\s*Iterator\b", "", code, count=1)


def main() -> None:
    original = NOXFILE.read_text(encoding="utf-8")
    modified = _drop_log_to_legacy(original)
    modified = _prune_iterator_import(modified)

    if modified == original:
        print("No changes made – patterns not found (already streamlined?).")
        return

    NOXFILE.write_text(modified, encoding="utf-8")
    print(
        dedent(
            f"""
            ✅  streamline_patch.py applied:
                • Removed _log_to_legacy context-manager
                • Removed unused Iterator import

            Next steps
            ----------
            1. Run `pytest -q` or `tests/personalvibe.sh` – all 40 tests should pass.
            2. Commit the patch with message: "chore: prune dead _log_to_legacy helper".
            3. Enjoy slightly leaner code (≈-65 LOC).

            """
        )
    )


if __name__ == "__main__":
    main()
