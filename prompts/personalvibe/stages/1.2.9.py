# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/1.2.9.py
#!/usr/bin/env python
"""
Sprint-2 patch – “nox vibed enhancements”
========================================

This script applies the *minimum* code changes required for the failing
test-suite:

1.  **Remove deprecated `pytest.register_mark` call**
    Pytest ≥ 7 dropped that helper; our own `conftest.py` already
    declares the project-wide “advanced” marker via
    `pytest_configure`.  We therefore patch `tests/__init__.py` so it
    simply imports pytest (keeps the file but avoids the old API).

2.  **Implement `RunContext` utility**
    `tests/test_run_context.py` expected `personalvibe.run_context`
    which was missing.  A tiny class is added that generates an ID like
    `yyyyMMdd_HHmmss_8hexchars` (UTC timestamp + 8 random hex digits).

After running this patch you can re-run the quality-gate:

    nox -s tests            # unit tests only
    nox -s vibed -- 0.0.2   # full branch + script integration test

Both should now pass.

"""

from __future__ import annotations

import secrets
from datetime import datetime
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()


# ────────────────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────────────────
def write(filepath: Path, content: str) -> None:
    """(Over)write *content* to *filepath* ensuring parent dirs exist."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")


# ────────────────────────────────────────────────────────────────────────────
# 1. Patch tests/__init__.py  (remove deprecated API)
# ────────────────────────────────────────────────────────────────────────────
tests_init = REPO / "tests" / "__init__.py"

new_tests_init = '''\
"""
Pytest package initialiser.

Older code called the now-removed `pytest.register_mark("advanced")`.
Project-wide markers are declared in `tests/conftest.py`, so all we
need is the import to make `tests` a package.
"""
import pytest  # noqa: F401
'''

write(tests_init, new_tests_init)
print(f"✅ Patched {tests_init.relative_to(REPO)}")


# ────────────────────────────────────────────────────────────────────────────
# 2. Add src/personalvibe/run_context.py
# ────────────────────────────────────────────────────────────────────────────
run_ctx_path = REPO / "src" / "personalvibe" / "run_context.py"

if not run_ctx_path.exists():
    run_ctx_code = '''\
"""Lightweight per-process context object.

The current use-case is test isolation (each test gets a unique ID for
log-file or temp-dir names).  A *stable yet unique* identifier is
generated once on construction:

    >>> from personalvibe.run_context import RunContext
    >>> ctx = RunContext()
    >>> ctx.id
    '20250130_134501_a1b2c3d4'

Format: ``YYYYMMDD_HHMMSS_8hex`` (UTC).
"""

from __future__ import annotations

import secrets
from datetime import datetime
from typing import Final


class RunContext:
    """Container for a single run identifier."""

    _TS_FORMAT: Final[str] = "%Y%m%d_%H%M%S"

    def __init__(self) -> None:
        ts = datetime.utcnow().strftime(self._TS_FORMAT)
        rand_hex = secrets.token_hex(4)  # 8 hex chars
        self.id: str = f"{ts}_{rand_hex}"

    # Helpful dunder methods – makes debugging nicer
    def __str__(self) -> str:  # pragma: no cover
        return self.id

    def __repr__(self) -> str:  # pragma: no cover
        return f"<RunContext {self.id}>"
'''

    write(run_ctx_path, run_ctx_code)
    print(f"✅ Created {run_ctx_path.relative_to(REPO)}")
else:
    print(f"ℹ️  {run_ctx_path.relative_to(REPO)} already exists – not touched.")


# ────────────────────────────────────────────────────────────────────────────
# Finish
# ────────────────────────────────────────────────────────────────────────────
print(
    "\n🏁  Sprint-2 patch applied.\n"
    "Next steps:\n"
    "  • Run `nox -s tests` – all unit tests should now be green.\n"
    "  • Optionally run `nox -s vibed -- 0.0.2` for the full\n"
    "    branch-creation + integration flow (writes to logs/0.0.2_base.log)."
)
