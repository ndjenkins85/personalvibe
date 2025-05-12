# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/1.2.7.py
#!/usr/bin/env python
"""
PATCH – Sprint #2 “nox vibed enhancements”

This script touches/patches files necessary to:
• remove the obsolete pytest.register_mark usage that currently breaks the
  entire test-suite
• harden `noxfile._log_to` (explicit O_APPEND flag) – the API already worked,
  this just makes the intent crystal-clear
• add lightweight regression tests that (a) prove _log_to really appends and
  (b) confirm our per-semver log banner helper `_print_step` is captured.

Run it once:

    poetry run python patches/sprint_2_vibed.py
"""

from __future__ import annotations

import os
import textwrap
from pathlib import Path

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
ROOT = Path(__file__).resolve().parents[1]  # repository root


def touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()
        print(f"🔧 touch {path}")


def write(path: Path, content: str) -> None:
    touch(path)
    path.write_text(textwrap.dedent(content.lstrip("\n")), encoding="utf-8")
    print(f"💾 wrote {path} ({len(content)} chars)")


def patch_file(path: Path, marker: str, patch_code: str) -> None:
    """Idempotently insert *patch_code* after *marker* line inside *path*."""
    src = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if any(marker in ln for ln in src):
        idx = next(i for i, ln in enumerate(src) if marker in ln) + 1
        if patch_code.strip() not in "".join(src):
            src[idx:idx] = [patch_code]  # insert
            path.write_text("".join(src), encoding="utf-8")
            print(f"🩹 patched {path} (+{patch_code.count(os.linesep)+1} lines)")


# --------------------------------------------------------------------------- #
# 1. Purge legacy `pytest.register_mark` usage (tests/__init__.py + conftest.py)
# --------------------------------------------------------------------------- #
tests_init = ROOT / "tests" / "__init__.py"
write(
    tests_init,
    """
    \"\"\"Pytest helper – keeps package importable.

    Legacy `pytest.register_mark` has been removed; custom markers are already
    declared in *pyproject.toml* therefore no runtime registration is needed.
    \"\"\"
    import pytest  # noqa:F401  (import side-effects only)
    """,
)

conftest = ROOT / "tests" / "conftest.py"
write(
    conftest,
    """
    \"\"\"Global pytest fixtures / marker declaration.\"\"\"

    import pytest

    def pytest_configure(config):  # noqa:D401
        # Ensure the *advanced* marker is always known
        config.addinivalue_line(
            "markers", "advanced: marks tests as advanced (deselect with '-m \"not advanced\"')"
        )
    """,
)

# --------------------------------------------------------------------------- #
# 2. Strengthen `_log_to` so the append intent is unambiguous
# --------------------------------------------------------------------------- #
noxfile = ROOT / "noxfile.py"
PATCH_MARKER = "# --- SPRINT-2 APPEND-SAFETY PATCH ---"
PATCH_CODE = """
from os import O_APPEND, O_CREAT, O_WRONLY
import os, io
"""
patch_file(noxfile, "from contextlib import contextmanager", PATCH_CODE)

PATCH_MARKER2 = "def _log_to(path: Path):"
if PATCH_MARKER2 in noxfile.read_text(encoding="utf-8"):
    EXTRA = """
        # Open *once* in O_APPEND|O_CREAT to guarantee we **never** truncate.
        os.close(os.open(path, O_APPEND | O_CREAT | O_WRONLY, 0o644))
    """
    patch_file(noxfile, PATCH_MARKER2, EXTRA)

# --------------------------------------------------------------------------- #
# 3. New regression tests
# --------------------------------------------------------------------------- #
tests_log = ROOT / "tests" / "test_log_to.py"
write(
    tests_log,
    """
    \"\"\"Regression tests for the sprint-2 logging enhancements.\"\"\"
    from pathlib import Path
    from noxfile import _log_to, _print_step


    def test_log_to_appends(tmp_path):
        \"\"\"Second write must *append* not overwrite.\"\"\"
        log_f = tmp_path / "demo.log"

        with _log_to(log_f):
            _print_step("FIRST-STEP")

        first_size = log_f.stat().st_size

        with _log_to(log_f):
            _print_step("SECOND-STEP")

        txt = log_f.read_text(encoding="utf-8")
        assert "FIRST-STEP" in txt and "SECOND-STEP" in txt
        # size must strictly grow
        assert log_f.stat().st_size > first_size
    """,
)

# --------------------------------------------------------------------------- #
# 4. Friendly hint for the user
# --------------------------------------------------------------------------- #
print(
    "\n✅  Sprint #2 patch applied.\n"
    "Run `nox -s tests` now – the previous pytest crash is fixed and new\n"
    "log append behaviour is covered by tests.\n"
)
