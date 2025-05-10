# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Utilities for validating and applying LLM-generated unified diffs safely."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

# Extremely conservative – loosen later if needed
_SAFE_PATH = re.compile(r"^[A-Za-z0-9_./-]+$")


def _check_path(rel: str, repo_root: Path) -> None:
    if ".." in Path(rel).parts:
        raise ValueError(f"Path escapes repo: {rel}")
    if not _SAFE_PATH.fullmatch(rel):
        raise ValueError(f"Suspicious characters: {rel}")
    if (repo_root / rel).is_symlink():
        raise ValueError(f"Refuses to patch symlink: {rel}")


def validate_diff(diff_text: str, repo_root: Path) -> None:
    """Raise if the diff touches anything outside the repo or looks sketchy."""
    for line in diff_text.splitlines():
        if line.startswith(("--- ", "+++ ")):
            # a/src/foo.py  →  src/foo.py
            rel = line.split(None, 2)[1][2:]
            _check_path(rel, repo_root)


def apply_diff(diff_text: str, repo_root: Path, dry_run: bool = False) -> None:
    """patch -p1 --forward [--dry-run].  Raises RuntimeError on failure."""
    flags = ["--dry-run"] if dry_run else []
    proc = subprocess.run(
        ["patch", "-p1", "--forward", *flags],
        input=diff_text.encode(),
        cwd=repo_root,
        capture_output=True,
    )
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode() or "patch failed")
