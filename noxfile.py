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

locations = "src/personalvibe", "tests", "noxfile.py", "docs/conf.py"
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
    """Create vibed/<semver> branch, apply patch(es), run quality-gate.

    Usage examples
    --------------
    nox -s vibed -- 1.2.3
    nox -s vibed -- 1.2.3 path/to/patch.py other_patch.py
    """
    if not session.posargs:
        session.error("Semver identifier required, e.g. nox -s vibed -- 0.2.1")

    semver, *patches = session.posargs
    semver = semver.strip()

    log_path = Path("logs") / f"{semver}_base.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with _log_to(log_path):
        _print_step(f"Creating branch vibed/{semver}")

        _temp_branch = "__temp_vibed_branch__"

        # Step 1: Checkout to a temporary branch (safe branch to delete from)
        session.run("git", "checkout", "-B", _temp_branch, external=True)

        # Step 2: Delete the target branch if it exists
        session.run("git", "branch", "-D", f"vibed/{semver}", external=True, success_codes=[0, 1])

        # Step 3: Create and switch to the new target branch
        session.run("git", "checkout", "-b", f"vibed/{semver}", external=True)

        # Step 4: Delete the temporary branch
        session.run("git", "branch", "-D", _temp_branch, external=True, success_codes=[0, 1])

        # ------------------------------------------------ Patch scripts
        for patch in patches:
            _print_step(f"Running patch script: {patch}")
            session.run("poetry", "run", "python", patch, external=True)

        _print_step("Executing quality-gate (tests/personalvibe.sh)")
        session.run("bash", "tests/personalvibe.sh", external=True)

    _print_step(f"✨  Vibe sprint '{semver}' finished – see {log_path}")
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


# --- PERSONALVIBE SPRINT 0.0.2 PATCH START
from pathlib import Path

from nox_poetry import session as _p_session  # reuse already-installed decorator


@_p_session(python=["3.12"], reuse_venv=True)  # type: ignore[misc]
def vibed(session):  # noqa: D401
    """Create **fresh** ``vibed/<semver>`` branch then run quality-gate.

    Usage examples
    --------------
    nox -s vibed -- 1.2.3
    nox -s vibed -- 1.2.3 my_patch.py other.py
    """
    if not session.posargs:
        session.error("Semver identifier required, e.g. nox -s vibed -- 0.2.1")

    semver, *patches = (arg.strip() for arg in session.posargs)

    log_path = Path("logs") / f"{semver}_base.log"
    from noxfile import _log_to, _print_step  # local reuse

    with _log_to(log_path):
        _print_step(f"Creating branch vibed/{semver}")

        tmp_branch = "__temp_vibed_branch__"
        session.run("git", "checkout", "-B", tmp_branch, external=True)

        # ensure idempotency
        session.run("git", "branch", "-D", f"vibed/{semver}", external=True, success_codes=[0, 1])
        session.run("git", "checkout", "-b", f"vibed/{semver}", external=True)
        session.run("git", "branch", "-D", tmp_branch, external=True, success_codes=[0, 1])

        # optional user-supplied patch scripts
        for patch in patches:
            _print_step(f"Running patch script: {patch}")
            session.run("poetry", "run", "python", patch, external=True)

        _print_step("Executing quality-gate (tests/personalvibe.sh)")
        session.run("bash", "tests/personalvibe.sh", external=True)

    _print_step(f"✨  Vibe sprint '{semver}' finished – see {log_path}")


# --- PERSONALVIBE SPRINT 0.0.2 PATCH END


# --- PERSONALVIBE CHUNK D PATCH START
@session(python=["3.12"], reuse_venv=False)
def smoke_dist(session: Session) -> None:  # noqa: D401
    """Build wheel, install into **fresh** temp venv, run `pv --help`."""
    _print_step("🏗️  Building wheel …")
    session.run("poetry", "build", "-f", "wheel", external=True)

    dist_dir = Path("dist")
    wheels = sorted(dist_dir.glob("personalvibe-*.whl"))
    if not wheels:
        session.error("Wheel not found in ./dist – build failed?")
    wheel = max(wheels, key=lambda p: p.stat().st_mtime)
    _print_step(f"Wheel built: {wheel.name}")

    import os
    import subprocess
    import sys
    import tempfile

    venv_dir = Path(tempfile.mkdtemp(prefix="pv_smoke_"))
    _print_step(f"🧪  Creating temp venv at {venv_dir}")
    session.run("python", "-m", "venv", str(venv_dir), external=True)

    bin_dir = venv_dir / ("Scripts" if os.name == "nt" else "bin")
    pip = bin_dir / ("pip.exe" if os.name == "nt" else "pip")
    pv_exe = bin_dir / ("pv.exe" if os.name == "nt" else "pv")

    _print_step("📦  Installing wheel into temp venv …")
    session.run(str(pip), "install", str(wheel), external=True)

    _print_step("🚀  Running `pv --help` smoke test …")
    session.run(str(pv_exe), "--help", external=True)

    _print_step("✅  smoke_dist completed successfully")


# --- PERSONALVIBE CHUNK D PATCH END
