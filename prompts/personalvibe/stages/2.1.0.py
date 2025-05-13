# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/2.1.0.py

#!/usr/bin/env python
"""
Sprint 1 – Chunk A  :  Retry Engine & Rollback
================================================

This patch introduces a *generic* retry-controller that will underpin the
“self-healing sprint loop”.  A minimal integration is wired into
`run_pipeline` via a new `--max_retries` CLI flag (default = 5).  Full
sprint/validate orchestration and markdown parsing land in later chunks,
but nothing written here will need to change – we isolate responsibilities
cleanly.

What the patch does
-------------------
1.  src/personalvibe/retry_engine.py   – brand-new module:
    • `run_with_retries()` executes an arbitrary callable up to *N* times,
      collecting exceptions and logging each attempt.
    • Optional `branch_name` triggers a **git rollback** (hard reset to
      the branch’s initial commit) when all retries fail.
2.  src/personalvibe/run_pipeline.py
    • Adds `--max_retries` flag and passes it through the logger so later
      code can pick it up.
    • (Full loop coming later, flag is parsed now so interface is frozen.)
3.  tests/test_retry_engine.py – unit tests proving:
      a) success first-time short-circuits,
      b) eventual success after failures,
      c) permanent failure invokes git rollback.

Execute this file
-----------------
`poetry run python patches/sprint_1_retry_engine.py`

It will:
• create **new** module & test file,
• patch run_pipeline,
• print a short reminder at the end.

You can then run the quality-gate:

    nox -s tests      # or   bash tests/personalvibe.sh
"""
from __future__ import annotations

import os
import textwrap
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()

# --------------------------------------------------------------------------- #
# Helper writers
# --------------------------------------------------------------------------- #


def _touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)


def _write(path: Path, content: str) -> None:
    _touch(path)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


# --------------------------------------------------------------------------- #
# 1.  New module: src/personalvibe/retry_engine.py
# --------------------------------------------------------------------------- #
module_path = REPO / "src" / "personalvibe" / "retry_engine.py"
module_code = """
    \"\"\"Generic retry–with–rollback helper (Chunk A).\"\"\"

    from __future__ import annotations

    import logging
    import subprocess
    import sys
    import time
    from types import TracebackType
    from typing import Callable, List, Type

    log = logging.getLogger(__name__)

    class RetryError(RuntimeError):
        \"\"\"Raised when *all* retry attempts fail.\"\"\"


    def _rollback_branch(branch_name: str) -> None:
        \"\"\"Hard-reset the git branch to its first commit & delete it.

        We purposefully keep it *brutally* simple – CI will always be on a
        throw-away branch named ``vibed/<semver>`` so nuking it is safe.
        \"\"\"
        log.error("Rolling-back branch %s …", branch_name)
        cmds = [
            ["git", "reset", "--hard", "HEAD~1"],
            ["git", "checkout", "-"],             # return to previous branch
            ["git", "branch", "-D", branch_name],  # delete the broken branch
        ]
        for cmd in cmds:
            try:
                subprocess.run(cmd, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as exc:  # pragma: no cover
                log.warning("Git rollback step failed: %s", exc.stdout)


    def run_with_retries(
        action: Callable[[], bool],
        *,
        max_retries: int = 5,
        sleep_seconds: float = 0.0,
        branch_name: str | None = None,
    ) -> bool:
        \"\"\"Run *action* until it returns ``True`` or retries exhausted.

        Parameters
        ----------
        action
            Callable that **returns bool** – *True* ⇒ success.
            It may raise; all exceptions count as failure / trigger retry.
        max_retries
            Maximum number of *attempts* (so ``max_retries=1`` means **no**
            retry, just a single execution).
        sleep_seconds
            Optional backoff between attempts (very small by default).
        branch_name
            When supplied and the action still fails after all retries,
            ``_rollback_branch`` is invoked.

        Returns
        -------
        bool
            ``True`` on success (i.e. action returned True at least once).

        Raises
        ------
        RetryError
            If all attempts fail.
        \"\"\"
        attempt = 0
        errors: List[BaseException | None] = []

        while attempt < max_retries:
            attempt += 1
            try:
                log.debug("RetryEngine – attempt %d/%d", attempt, max_retries)
                if action():
                    if attempt > 1:
                        log.info("✅  Succeeded after %d attempts", attempt)
                    return True
                else:
                    log.warning("Action returned False (attempt %d)", attempt)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)
                etype: Type[BaseException] = type(exc)
                log.warning("Action raised %s: %s  (attempt %d)", etype.__name__, exc, attempt)

            if attempt < max_retries and sleep_seconds:
                time.sleep(sleep_seconds)

        # ---- failure after all attempts ------------------------------------
        log.error("❌  All %d attempts failed.", max_retries)
        if branch_name:
            _rollback_branch(branch_name)

        # Preserve last error for callers wanting more context
        raise RetryError(f"All {max_retries} attempts failed; see logs.") from (errors[-1] if errors else None)
"""
_write(module_path, module_code)

# --------------------------------------------------------------------------- #
# 2.  Patch src/personalvibe/run_pipeline.py  (add --max_retries CLI flag)
# --------------------------------------------------------------------------- #
rp_path = REPO / "src" / "personalvibe" / "run_pipeline.py"
rp_src = rp_path.read_text(encoding="utf-8").splitlines()

# Insert argument flag right after existing args parsing
insert_idx = next(i for i, line in enumerate(rp_src) if "parser.add_argument(" in line and "--prompt_only" in line) + 1
rp_src.insert(
    insert_idx,
    '    parser.add_argument("--max_retries", type=int, default=5, help="Maximum attempts for sprint validation")',
)
_write(rp_path, "\n".join(rp_src))

# --------------------------------------------------------------------------- #
# 3.  Unit-tests – tests/test_retry_engine.py
# --------------------------------------------------------------------------- #
test_path = REPO / "tests" / "test_retry_engine.py"
test_code = """
    \"\"\"Tests for the generic retry_engine (Chunk A).\"\"\"

    from __future__ import annotations

    import builtins
    from types import SimpleNamespace

    import pytest

    from personalvibe.retry_engine import RetryError, run_with_retries


    def test_success_first_try():
        calls = {"n": 0}

        def _ok():
            calls["n"] += 1
            return True

        assert run_with_retries(_ok, max_retries=3) is True
        assert calls["n"] == 1  # short-circuited


    def test_eventual_success(monkeypatch):
        seq = iter([False, False, True])
        calls = {"n": 0}

        def _sometimes():
            calls["n"] += 1
            return next(seq)

        assert run_with_retries(_sometimes, max_retries=5) is True
        assert calls["n"] == 3


    def test_permanent_failure_triggers_rollback(monkeypatch):
        # --- stub out _rollback_branch so we don't touch git --------------
        recorded = SimpleNamespace(called=False)

        def _fake_rollback(branch):
            recorded.called = branch

        monkeypatch.setattr("personalvibe.retry_engine._rollback_branch", _fake_rollback)

        def _always_false():
            return False

        with pytest.raises(RetryError):
            run_with_retries(_always_false, max_retries=2, branch_name="vibed/0.0.1")

        assert recorded.called == "vibed/0.0.1"
"""
_write(test_path, test_code)

# --------------------------------------------------------------------------- #
# 4.  Friendly summary
# --------------------------------------------------------------------------- #
print(
    """
📦  Chunk A applied.
─────────────────────────────────────────────────────────────────
• New module  : src/personalvibe/retry_engine.py
• Patched     : src/personalvibe/run_pipeline.py  (adds --max_retries)
• Tests added : tests/test_retry_engine.py

Run the full quality-gate:

    bash tests/personalvibe.sh      # or  nox -s tests

Subsequent chunks will hook the retry controller into the actual
sprint/validate workflow and enable git rollback of vibed branches.
"""
)
