# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/1.2.6.py
#!/usr/bin/env python
"""
patches/sprint_0_0_2.py
=======================

Sprint-2 (“nox vibed enhancements”) patcher.

• Re-implements **noxfile.vibed** once (removing the duplicate logic that
  caused “branch already exists” errors).
• Keeps _log_to behaviour (already append-mode).
• Adds an integration-style unit-test that ensures the *Creating branch*
  banner only appears **once** for a given run.
• Silences the Pytest warning for the custom *advanced* mark.

Run this file once (from *any* sub-folder) then execute:

    nox -s tests          # all suites (including the new one) must pass
    nox -s vibed -- 0.0.2 # manual smoke-check if desired

Nothing is deleted – we only append / create files.
"""
from __future__ import annotations

import textwrap
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from personalvibe import vibe_utils

REPO: Path = vibe_utils.get_base_path()


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()


def _append_once(path: Path, snippet: str, unique_key: str) -> None:
    """Append `snippet` to `path` unless `unique_key` already present."""
    content = path.read_text(encoding="utf-8") if path.exists() else ""
    if unique_key not in content:
        path.write_text(content + "\n" + snippet, encoding="utf-8")


@contextmanager
def _edit_file(path: Path) -> Generator[list[str], None, None]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    yield lines
    path.write_text("".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------- #
# 1. Patch `noxfile.py` (new clean implementation, once)
# --------------------------------------------------------------------------- #
noxfile_path = REPO / "noxfile.py"
unique_tag = "# --- PERSONALVIBE SPRINT 0.0.2 PATCH START"

new_func = textwrap.dedent(
    f"""
    {unique_tag}
    from pathlib import Path
    from nox_poetry import session as _p_session  # reuse already-installed decorator

    @_p_session(python=["3.12"], reuse_venv=True)  # type: ignore[misc]
    def vibed(session):  # noqa: D401
        \"\"\"Create **fresh** ``vibed/<semver>`` branch then run quality-gate.

        Usage examples
        --------------
        nox -s vibed -- 1.2.3
        nox -s vibed -- 1.2.3 my_patch.py other.py
        \"\"\"
        if not session.posargs:
            session.error("Semver identifier required, e.g. nox -s vibed -- 0.2.1")

        semver, *patches = (arg.strip() for arg in session.posargs)

        log_path = Path("logs") / f"{{semver}}_base.log"
        from noxfile import _log_to, _print_step  # local reuse

        with _log_to(log_path):
            _print_step(f"Creating branch vibed/{{semver}}")

            tmp_branch = "__temp_vibed_branch__"
            session.run("git", "checkout", "-B", tmp_branch, external=True)

            # ensure idempotency
            session.run("git", "branch", "-D", f"vibed/{{semver}}", external=True, success_codes=[0, 1])
            session.run("git", "checkout", "-b", f"vibed/{{semver}}", external=True)
            session.run("git", "branch", "-D", tmp_branch, external=True, success_codes=[0, 1])

            # optional user-supplied patch scripts
            for patch in patches:
                _print_step(f"Running patch script: {{patch}}")
                session.run("poetry", "run", "python", patch, external=True)

            _print_step("Executing quality-gate (tests/personalvibe.sh)")
            session.run("bash", "tests/personalvibe.sh", external=True)

        _print_step(f"✨  Vibe sprint '{{semver}}' finished – see {{log_path}}")
    # --- PERSONALVIBE SPRINT 0.0.2 PATCH END
    """
)

_append_once(noxfile_path, new_func, unique_tag)


# --------------------------------------------------------------------------- #
# 2. Add the new unit-test
# --------------------------------------------------------------------------- #
test_path = REPO / "tests" / "test_vibed_no_duplicates.py"
if not test_path.exists():
    test_code = textwrap.dedent(
        """
        import builtins
        from contextlib import contextmanager

        import pytest

        import noxfile


        class DummySession:
            \"\"\"Mimics minimal `nox.sessions.Session` behaviour.\"\"\"

            def __init__(self, posargs):
                self.posargs = posargs
                self.runs = []

            # nox`Session.run` signature is flexible – we ignore **kwargs
            def run(self, *cmd, **_):
                self.runs.append(cmd)

            def run_always(self, *cmd, **_):
                self.run(*cmd)

            def error(self, msg):
                raise RuntimeError(msg)

        @contextmanager
        def _noop_log_to(_):
            \"\"\"Stub that bypasses `tee`, making stdout capturable.\"\"\"
            yield

        def test_vibed_prints_single_branch_banner(monkeypatch, capsys):
            # --- isolate side-effects -------------------------------------------------
            monkeypatch.setattr(noxfile, "_log_to", _noop_log_to, raising=True)

            session = DummySession(["0.0.2"])
            noxfile.vibed(session)

            captured = capsys.readouterr().out
            assert captured.count("Creating branch vibed/0.0.2") == 1, captured
        """
    )
    _touch(test_path)
    test_path.write_text(test_code, encoding="utf-8")


# --------------------------------------------------------------------------- #
# 3. Silence unknown mark warning (nice-to-have)
# --------------------------------------------------------------------------- #
init_test_path = REPO / "tests" / "__init__.py"
mark_snippet = textwrap.dedent(
    """
    # -- auto-added by sprint-0.0.2 ------------------------------------------
    import pytest  # noqa: E402

    if not hasattr(pytest, "advanced"):
        pytest.register_mark("advanced")
    """
)
_append_once(init_test_path, mark_snippet, "sprint-0.0.2")


# --------------------------------------------------------------------------- #
# 4. Final notes
# --------------------------------------------------------------------------- #
print(
    "\n✅  Sprint-2 patch applied.\n"
    "Run `nox -s tests` to verify all suites, then "
    "`nox -s vibed -- 0.0.2` for a manual smoke-check.\n"
)
