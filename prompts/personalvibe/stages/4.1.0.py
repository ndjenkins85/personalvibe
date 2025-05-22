# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/4.1.0.py

# patch_chunkA_trim_deps.py
"""
Chunk A – Dependency Diet
=========================
This one-off patch script rewrites *pyproject.toml* so **Personalvibe**
ships ONLY the libraries it truly needs at runtime and wires an
assertion into the project-wide bash test-runner that the “main”
dependency set can be exported without error.

What it does
------------
1.  Removes Storymaker / server-side packages from the
    `[tool.poetry.dependencies]` section:

        Flask, Flask-Cors, Flask-SSLify,
        eventlet, gunicorn, gevent,
        email-validator, pyjwt,
        Markdown, MarkupSafe, pandas

2.  Keeps core libs (jinja2, openai, …) untouched.

3.  Updates *tests/personalvibe.sh* so that **every** quality-gate run
    executes

        poetry export --only main --without-hashes -o /dev/null

    — a fast sanity-check proving the dependency list is consistent.

Run me
------
    poetry run python patch_chunkA_trim_deps.py

The script is idempotent (safe to re-run) and will print a short diff
summary of affected files.

"""
from __future__ import annotations

import fileinput
import re
import sys
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()

PYPROJECT = REPO / "pyproject.toml"
TEST_SCRIPT = REPO / "tests" / "personalvibe.sh"

REMOVE_DEPS = {
    "Flask",
    "Flask-Cors",
    "Flask-SSLify",
    "eventlet",
    "gunicorn",
    "gevent",
    "email-validator",
    "pyjwt",
    "Markdown",
    "MarkupSafe",
    "pandas",
}


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _patch_pyproject() -> bool:
    """Return True if file changed."""
    new_lines: list[str] = []
    changed = False
    in_deps = False

    with PYPROJECT.open(encoding="utf-8") as fh:
        for line in fh:
            # Track whether we are inside [tool.poetry.dependencies]
            if re.match(r"\[tool\.poetry\.dependencies\]", line.strip()):
                in_deps = True
                new_lines.append(line)
                continue
            elif line.startswith("[") and in_deps:
                # leaving the section
                in_deps = False

            if in_deps:
                dep_key = line.split("=")[0].strip()
                if dep_key in REMOVE_DEPS:
                    print(f"  – removing {dep_key}")
                    changed = True
                    continue  # skip writing this line
            new_lines.append(line)

    if changed:
        PYPROJECT.write_text("".join(new_lines), encoding="utf-8")
    return changed


def _ensure_export_smoketest() -> bool:
    """Inject `poetry export` line into bash script if missing."""
    marker = "poetry export --only main"
    changed = False

    if TEST_SCRIPT.exists():
        content = TEST_SCRIPT.read_text(encoding="utf-8").splitlines()
    else:
        print(f"⚠️  {TEST_SCRIPT} not found – creating fresh file")
        content = ["#!/usr/bin/env bash", "set -euo pipefail", ""]

    if not any(marker in ln for ln in content):
        # Insert right after the 'poetry install' command
        for idx, ln in enumerate(content):
            if "poetry install" in ln and "--sync" in ln:
                content.insert(
                    idx + 1,
                    "poetry export --only main --without-hashes -o /dev/null",
                )
                changed = True
                print("  + added poetry export smoke-test to tests/personalvibe.sh")
                break
        else:  # no install line found, just append near top
            content.insert(0, marker)
            changed = True

    if changed:
        TEST_SCRIPT.write_text("\n".join(content) + "\n", encoding="utf-8")
        # Ensure executable bit stays intact (important on *nix CI)
        TEST_SCRIPT.chmod(TEST_SCRIPT.stat().st_mode | 0o111)
    return changed


# --------------------------------------------------------------------------- #
# Execute patch steps
# --------------------------------------------------------------------------- #
print("🔧  Chunk A – Trimming dependencies")

files_changed = 0
if _patch_pyproject():
    files_changed += 1
if _ensure_export_smoketest():
    files_changed += 1

if files_changed == 0:
    print("✅  Nothing to change – repository already lean.")
else:
    print(f"✅  Patch applied – {files_changed} file(s) modified.")

print(
    "\nNext steps:\n"
    "1)  Run  `poetry lock --no-update`  to regenerate the lean lock-file.\n"
    "2)  Execute the quality-gate:  bash tests/personalvibe.sh\n"
    "    (it now includes a poetry-export smoke-test).\n"
    "Happy vibecoding! 🚀"
)
