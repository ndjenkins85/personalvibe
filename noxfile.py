# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Nox for python task automation."""

import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List

import nox
from nox.sessions import Session
from nox_poetry import session

from personalvibe.git_utils import apply_diff, validate_diff  # helper we wrote earlier

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


@session(name="sprint", python=["3.12"])
def sprint(session):
    """
    Usage:
        nox -s sprint -- data/storymaker_prompts/diffs/newdiff.md  3 1
        nox -s sprint -- path/to/diff.patch  <milestone>  <sprint>
    Example:
        nox -s sprint -- /tmp/m1s1.diff       1            1
    """
    if len(session.posargs) < 3:
        session.error("Need: diff_path  milestone  sprint")
    diff_path, milestone, sprint_no = session.posargs[:3]
    diff_path = Path(diff_path).expanduser().resolve()

    branch = f"milestone/{milestone}/sprint/{sprint_no}"
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"{branch.replace('/', '_')}.log"

    def tee(cmd: List[str], **kwargs):
        """Run shell cmd; append stdout+stderr to log and raise on failure."""
        session.log(" ".join(cmd))
        with log_file.open("a") as fh:
            proc = subprocess.run(
                cmd,
                stdout=fh,
                stderr=fh,
                text=True,
                **kwargs,
            )
        if proc.returncode:
            session.error(f"Command failed: {' '.join(cmd)}  (see {log_file})")

    # ---------- 1) create an isolated worktree + branch ----------
    tmp_worktree = Path(f".worktrees/{branch.replace('/', '_')}")
    tee(["git", "worktree", "add", str(tmp_worktree), "-b", branch])

    # All further commands run inside that worktree
    os.chdir(tmp_worktree)

    # ---------- 2) load & validate diff ----------
    diff_text = diff_path.read_text()
    validate_diff(diff_text, repo_root=Path.cwd())  # raises on danger
    try:
        apply_diff(diff_text, Path.cwd(), dry_run=True)  # sanity check
    except Exception as err:
        session.error(f"Patch dry-run failed: {err}  (see {log_file})")

    # ---------- 3) really apply, then install deps ----------
    apply_diff(diff_text, Path.cwd(), dry_run=False)
    tee(["poetry", "install"], check=True)

    # ---------- 4) run tests ----------
    tee(["pytest", "-m", "not advanced"])

    # ---------- 5) commit + (optional) push ----------
    tee(["git", "add", "-A"])
    tee(["git", "commit", "-m", f"Sprint {sprint_no} of milestone {milestone}"])
    # tee(["git", "push", "-u", "origin", branch])   # enable when ready

    session.log(f"✅ Sprint passed. Full log in {log_file}")
