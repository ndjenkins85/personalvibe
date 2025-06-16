# flake8: noqa
# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Nox for python task automation."""
import io
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

locations = ("src/personalvibe", "tests", "noxfile.py", "docs/conf.py")

nox.options.sessions = "lint", "tests"
package = "personalvibe"


@session(python=["3.9", "3.12"])
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
    session.run(
        "mypy",
        "-p",
        package,  # analyse the installed package
    )
    session.run("flake8", *args, "--select=ANN,E,F")


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


@session(python=["3.9", "3.12"])
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


@session(python=["3.12"], reuse_venv=True)
def vibed_legacy(session: Session) -> None:  # noqa: D401
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
def vibed(session):  # noqa: D401  # type: ignore[no-redef]
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

    # --- PERSONALVIBE CHUNK 4 PATCH START
    import tempfile
    from datetime import datetime
    from pathlib import Path as _Path

    from nox_poetry import session as _pv_session  # reuse already-installed decorator

    @_pv_session(python=["3.12"], reuse_venv=False)  # type: ignore[misc]
    def smoke_dist(session):  # noqa: D401
        """Extended smoke-test: wheel install + core CLI commands."""
        _print_step = globals()["_print_step"]  # late-bind from module globals

        # 1) build wheel --------------------------------------------------
        _print_step("🏗️  Building wheel …")
        session.run("poetry", "build", "-f", "wheel", external=True)
        dist_dir = _Path("dist")
        wheels = sorted(dist_dir.glob("personalvibe-*.whl"))
        if not wheels:
            session.error("Wheel build failed – no file in ./dist")
        wheel = max(wheels, key=lambda p: p.stat().st_mtime)

        # 2) temp venv ----------------------------------------------------
        venv_dir = _Path(tempfile.mkdtemp(prefix="pv_smoke_"))
        _print_step(f"🧪  Creating temp venv at {venv_dir}")
        session.run("python", "-m", "venv", str(venv_dir), external=True)

        bindir = venv_dir / ("Scripts" if session.platform == "win32" else "bin")
        pip_exe = bindir / ("pip.exe" if session.platform == "win32" else "pip")
        pv_exe = bindir / ("pv.exe" if session.platform == "win32" else "pv")

        # 3) install wheel -------------------------------------------------
        _print_step("📦  Installing wheel …")
        session.run(str(pip_exe), "install", str(wheel), external=True)

        # 4) pv --help -----------------------------------------------------
        _print_step("🚀  Running `pv --help` …")
        session.run(str(pv_exe), "--help", external=True)

        # 5) prepare minimal workspace (prompts + cfg) --------------------
        repo_root = _Path.cwd()  # still the mono-repo root
        prompts_dir = repo_root / "prompts" / "sampleproj"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        (prompts_dir / "prd.md").write_text(
            "# dummy template used by smoke_dist\nHello {{ execution_task }}.",
            encoding="utf-8",
        )

        cfg_dir = repo_root / "tmp_smoke_cfg"
        cfg_dir.mkdir(exist_ok=True)
        cfg_file = cfg_dir / "1.0.0.yaml"
        cfg_file.write_text(
            textwrap.dedent(
                """                project_name: sampleproj
            mode: milestone
            execution_details: ''
            code_context_paths: []
            """
            ),
            encoding="utf-8",
        )

        # 6) run pv run --prompt_only --------------------------------------
        _print_step("🎯  pv run --prompt_only …")
        session.run(
            str(pv_exe),
            "run",
            "--config",
            str(cfg_file),
            "--prompt_only",
            "--verbosity",
            "errors",
            external=True,
        )

        # 7) create dummy assistant output so parse-stage succeeds ---------
        outputs_dir = repo_root / "data" / "sampleproj" / "prompt_outputs"
        outputs_dir.mkdir(parents=True, exist_ok=True)
        dummy_path = outputs_dir / f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_dummyhash.md"
        dummy_path.write_text(
            """```python
print('hello world')
```""",
            encoding="utf-8",
        )

        # 8) pv parse-stage -----------------------------------------------
        _print_step("🔎  pv parse-stage …")
        session.run(
            str(pv_exe),
            "parse-stage",
            "--project_name",
            "sampleproj",
            external=True,
        )

        _print_step("✅  smoke_dist finished without errors")

    # --- PERSONALVIBE CHUNK 4 PATCH END


# --- FIXED _log_to IMPLEMENTATION ---
@contextmanager
def _log_to(path: Path):  # type: ignore[override]  # type: ignore[no-redef]
    """
    Duplicate *all* stdout / stderr – including child-process output – to
    ``path`` **in append mode** without dead-locking.

    Key fix:
        Close the per-context TextIOWrapper duplicates **before** waiting
        on the underlying ``tee`` process so that the pipe write-end is
        fully closed (otherwise tee never terminates and pytest hangs).
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

    # Spawn persistent tee (-a so we append)
    tee_proc = subprocess.Popen(
        ["tee", "-a", str(path)],
        stdin=subprocess.PIPE,
        text=False,  # binary FD handing
    )
    if tee_proc.stdin is None:  # pragma: no cover
        raise RuntimeError("tee failed to provide stdin")

    tee_fd = tee_proc.stdin.fileno()

    # Save original low-level fds
    saved_out_fd = os.dup(1)
    saved_err_fd = os.dup(2)

    # Route fd1/fd2 to tee
    os.dup2(tee_fd, 1)
    os.dup2(tee_fd, 2)

    # High-level Python objects (wrappers around *new* duped fds)
    saved_stdout_obj, saved_stderr_obj = sys.stdout, sys.stderr
    wrapper_stdout = io.TextIOWrapper(os.fdopen(os.dup(1), "wb"), encoding="utf-8", line_buffering=True)
    wrapper_stderr = io.TextIOWrapper(os.fdopen(os.dup(2), "wb"), encoding="utf-8", line_buffering=True)
    sys.stdout, sys.stderr = wrapper_stdout, wrapper_stderr

    try:
        yield
    finally:
        # Flush & CLOSE wrappers so no fd points to the pipe afterwards
        try:
            wrapper_stdout.flush()
            wrapper_stderr.flush()
        finally:
            wrapper_stdout.close()
            wrapper_stderr.close()

        # Restore original low-level fds
        os.dup2(saved_out_fd, 1)
        os.dup2(saved_err_fd, 2)
        os.close(saved_out_fd)
        os.close(saved_err_fd)

        # Close tee stdin and wait for it to finish writing
        tee_proc.stdin.close()
        tee_proc.wait()

        # Restore original Python objects
        sys.stdout, sys.stderr = saved_stdout_obj, saved_stderr_obj


# --- END FIXED _log_to IMPLEMENTATION ---

# === release session (chunk E) ===
from nox_poetry import session as _session_release  # type: ignore


@_session_release(python=["3.12"], reuse_venv=False)  # type: ignore[misc]
def release(session):
    """Simulate a *real* release: bump, build, smoke, report location."""
    _print_step = globals()["_print_step"]
    _print_step("🏗️   Building wheel for release…")
    session.run("poetry", "build", "-f", "wheel", external=True)

    _print_step("🧪  Running smoke_dist…")
    session.run("poetry", "run", "nox", "-s", "smoke_dist", external=True)

    _print_step("🎉  Release rehearsal for 2.1.0 passed – wheel in ./dist")
