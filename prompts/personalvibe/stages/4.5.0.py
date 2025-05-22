# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/4.5.0.py

"""
chunk_e_release.py  –  Sprint “2.1.0 / Chunk E – final polish & release simulation”

Run with:

    poetry run python chunk_e_release.py

or let nox / CI pick it up automatically.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from textwrap import dedent

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()


# --------------------------------------------------------------------------- helpers
def _bump_version_in_file(path: Path, pattern: str, new_version: str) -> None:
    txt = path.read_text(encoding="utf-8")
    new_txt, n = re.subn(pattern, rf'\1"{new_version}"', txt, count=1, flags=re.M)
    if n == 0:
        print(f"[WARN]   pattern not found in {path}")
    path.write_text(new_txt, encoding="utf-8")
    print(f"[MOD]    {path}  – version → {new_version}")


def _ensure_line(path: Path, sentinel: str, block: str) -> None:
    txt = path.read_text(encoding="utf-8") if path.exists() else ""
    if sentinel in txt:
        return
    with path.open("a", encoding="utf-8") as fh:
        fh.write("\n" + block.strip() + "\n")
    print(f"[APPEND] {path}  – added release checklist")


# --------------------------------------------------------------------------- 1. bump versions
NEW_VERSION = "2.1.0"

_bump_version_in_file(
    REPO / "pyproject.toml",
    r'^(version\s*=\s*)"[0-9]+\.[0-9]+\.[0-9]+"',
    NEW_VERSION,
)

_bump_version_in_file(
    REPO / "src" / "personalvibe" / "__init__.py",
    r'(__version__\s*=\s*)"[0-9]+\.[0-9]+\.[0-9]+"',
    NEW_VERSION,
)

# --------------------------------------------------------------------------- 2. add RELEASE.md
release_md = REPO / "RELEASE.md"
if not release_md.exists():
    release_md.write_text(
        dedent(
            f"""
            # Release guide – Personalvibe {NEW_VERSION}

            This is a *living* checklist to cut an **Independence Day** style
            release.  Nothing here enforces policy – it is a reminder that the
            human-in-the-loop must still sanity-check artefacts.

            1. `git switch master && git pull`
            2. Ensure CI is green on *all* branches slated for merge.
            3. Run the full quality-gate locally:

                ./tests/personalvibe.sh {NEW_VERSION}

            4. Bump changelog / docs if needed.
            5. Tag & push:

                git tag v{NEW_VERSION} && git push origin v{NEW_VERSION}

            6. GitHub Actions will build & upload the wheel.
            7. Verify **PyPI** and **docs** artefacts.
            8. Tweet the release, grab ☕.

            ---
            *Generated automatically by chunk_e_release.py.*
            """
        ).lstrip(),
        encoding="utf-8",
    )
    print(f"[CREATE] {release_md}")
else:
    print(f"[SKIP]   {release_md} already exists")

# --------------------------------------------------------------------------- 3. patch noxfile
noxfile = REPO / "noxfile.py"
sentinel = "# === release session (chunk E) ==="
release_block = f"""
{sentinel}
from nox_poetry import session as _session_release  # type: ignore

@_session_release(python=["3.12"], reuse_venv=False)  # type: ignore[misc]
def release(session):
    \"\"\"Simulate a *real* release: bump, build, smoke, report location.\"\"\"
    _print_step = globals()["_print_step"]
    _print_step("🏗️   Building wheel for release…")
    session.run("poetry", "build", "-f", "wheel", external=True)

    _print_step("🧪  Running smoke_dist…")
    session.run("poetry", "run", "nox", "-s", "smoke_dist", external=True)

    _print_step("🎉  Release rehearsal for {NEW_VERSION} passed – wheel in ./dist")
"""

_ensure_line(noxfile, sentinel, release_block)

# --------------------------------------------------------------------------- 4. feedback
print(
    dedent(
        f"""
        ✅  Chunk E finished.

        Next steps
        ----------
        1.  git add -A && git commit -m "chore: bump version to {NEW_VERSION} and add release session"
        2.  poetry run nox -s release
        3.  If all green: push branch & open PR.

        Happy vibecoding! 🚀
        """
    )
)
