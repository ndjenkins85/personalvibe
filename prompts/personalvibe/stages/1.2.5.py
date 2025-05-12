# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/1.2.5.py
#!/usr/bin/env python
"""
patch_sprint_2.py  – Apply sprint-2 “nox vibed enhancements”.

Run via:

    poetry run python tests/patch_sprint_2.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from textwrap import dedent

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()  # project root


def write(path: Path, text: str) -> None:
    """Write *exactly* the given text (mkdir parents first)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(text).lstrip(), encoding="utf-8")


def patch_dummy_patch() -> None:
    """Overwrite tests/dummy_patch.py with a harmless implementation.

    The previous version triggered mypy/black noise – keep it tiny.
    """
    text = r"""
    \"\"\"tests/dummy_patch.py – No-op patch used by vibed integration test.\"\"\"

    if __name__ == "__main__":  # pragma: no cover
        print("✅ dummy_patch.py executed – nothing to do.")
    """
    write(REPO / "tests" / "dummy_patch.py", text)


def patch_vibed_session_test() -> None:
    """Create/replace tests/test_vibed_session.py.

    Marked with @pytest.mark.advanced so the default test run
    (nox -s tests) skips it, avoiding infinite recursion.
    """
    text = r"""
    \"\"\"Integration test for `nox -s vibed` (advanced).

    It spawns a **sub-process** that executes:

        nox -s vibed -- 0.0.2 tests/dummy_patch.py

    The session should:
      • create logs/0.0.2_base.log (append mode)
      • contain the three main step banners.
    \"\"\"
    import subprocess
    from pathlib import Path
    import pytest


    @pytest.mark.advanced
    def test_vibed_creates_base_log(tmp_path):
        log_path = Path("logs") / "0.0.2_base.log"
        # Start clean
        if log_path.exists():
            log_path.unlink()

        # Record current branch to restore later
        current_branch = (
            subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
        )

        try:
            subprocess.run(
                ["nox", "-s", "vibed", "--", "0.0.2", "tests/dummy_patch.py"],
                check=True,
                text=True,
            )
        finally:
            # Switch back & drop test branch to keep workspace tidy
            subprocess.run(["git", "checkout", current_branch], check=True, text=True)
            subprocess.run(["git", "branch", "-D", "vibed/0.0.2"], check=False, text=True)

        assert log_path.exists(), "vibed should create logs/0.0.2_base.log"
        content = log_path.read_text()

        expected = [
            "Creating branch vibed/0.0.2",
            "Running patch script: tests/dummy_patch.py",
            "Executing quality-gate (tests/personalvibe.sh)",
        ]
        for phrase in expected:
            assert phrase in content, f"Missing banner line: {phrase}"
    """
    write(REPO / "tests" / "test_vibed_session.py", text)


def main() -> None:
    patch_dummy_patch()
    patch_vibed_session_test()

    print(
        "\nSprint-2 patch applied:\n"
        "  • tests/dummy_patch.py replaced with a minimal no-op stub\n"
        "  • tests/test_vibed_session.py rewritten (marked @advanced)\n\n"
        "Run the full quality-gate:\n"
        "    nox -s vibed -- 0.0.2 tests/patch_sprint_2.py\n"
        "or simply execute the new test suite (advanced skipped by default):\n"
        "    nox -s tests\n"
    )


if __name__ == "__main__":
    main()
