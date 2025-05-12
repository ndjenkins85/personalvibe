# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Nox for python task automation."""
import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import List

import nox
from nox.sessions import Session
from nox_poetry import session

locations = "personalvibe", "tests", "noxfile.py", "docs/conf.py"
nox.options.sessions = "lint", "tests"
package = "personalvibe"


@session(python=["3.12"])
def lint(session: Session) -> None:
    """Runs code quality checks.

    Done in order so that easier to pass tests run first.
    This is in a single command to avoid too much time on environment setup.
    * black - codestyle alignment
    * xdoctest - any code snippets in docstrings are run for correctness
    * mypy - type checking
    * flake8 - code format and consistency checks
    """
    args = session.posargs or locations
    session.run_always("poetry", "install", external=True)
    session.run("black", *args)
    session.run("mypy", *args)
    session.run("flake8", *args)


@session(python=["3.12"])
def safety(session: Session) -> None:
    """Runs safety - security checks."""
    session.run_always("poetry", "install", external=True)
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@session(python=["3.12"])
def tests(session: Session) -> None:
    """Run the test suite, locally, and in CICD process."""
    args = session.posargs or ["-m", "not advanced"]
    session.run_always("poetry", "install", external=True)
    session.run("pytest", *args, "-W ignore::DeprecationWarning", external=True)


@session(python=["3.12"])
def docs(session: Session) -> None:
    """Build documentation and static files and push to codebase."""
    session.run_always("poetry", "install", external=True)
    session.run("rm", "-rf", "docs/_build", external=True)
    session.run("sphinx-build", "docs", "docs/_build", *session.posargs)


def _print_step(msg: str) -> None:
    session_log = "=" * len(msg)
    print(f"\n{session_log}\n{msg}\n{session_log}\n")


@contextmanager
def _log_to(path: Path):
    """Duplicate *all* stdout/stderr to **append** mode log file.

    The implementation purposefully:
    • opens the target file beforehand so it is never truncated
    • spawns one long-lived ``tee -a`` process
    • restores sys.std* even if exceptions occur
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    # Ensure file exists so tee -a never complains
    path.touch(exist_ok=True)

    proc = subprocess.Popen(
        ["tee", "-a", str(path)],
        stdin=subprocess.PIPE,
        text=True,
    )  # type: ignore[arg-type]
    saved_out, saved_err = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = proc.stdin  # type: ignore[assignment]
    try:
        yield
    finally:
        # Flush and close the tee input; restore
        try:
            sys.stdout.flush()
            sys.stderr.flush()
        finally:
            proc.stdin.close()  # type: ignore[attr-defined]
            proc.wait()
            sys.stdout, sys.stderr = saved_out, saved_err


@session(python=["3.12"], reuse_venv=True)
def vibed(session: Session) -> None:  # noqa: D401
    """
    Apply an auto-generated *patch* then run the full quality-gate.

    Usage:
        nox -s vibed -- 0.2.1           # <semver>
        nox -s vibed -- 0.2.1 mypatch.py
        nox -s vibed -- 3.1.0 data/storymaker/prompt_outputs/mypatch.py

    Steps:
      1. git checkout -b vibed/{semver}
      2. capture everything to logs/{semver}.log
      3. poetry run python <patch>
      4. tests/personalvibe.sh   (lint + pytest)

    Any non-zero return code aborts the session.
    """
    if not session.posargs:
        session.error("Semver identifier required, e.g. nox -s vibed -- 0.2.1")
    semver = session.posargs[0].strip()

    log_path = Path("logs") / f"{semver}.log"
    log_path.parent.mkdir(exist_ok=True)

    with _log_to(log_path):
        _print_step(f"Creating branch vibed/{semver}")
        session.run("git", "checkout", "-b", f"vibed/{semver}", external=True)

        _print_step("Executing quality-gate (tests/personalvibe.sh)")
        # the script already exits-on-error (`set -euo pipefail`)
        session.run("bash", "tests/personalvibe.sh", external=True)

    _print_step(f"✨  Vibe sprint '{semver}' finished – see {log_path}")
