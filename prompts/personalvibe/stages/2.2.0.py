# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/2.2.0.py

#!/usr/bin/env python
"""
Chunk A – CLI scaffolding patch-script.

Run via:

    poetry run python patch_cli_chunkA.py

It will:
• create  src/personalvibe/cli.py
• patch  pyproject.toml   (exposes `pv` + fixes broken script entry)
• add    tests/test_cli_basic.py
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

# --------------------------------------------------------------------------- #
# 1. Resolve repo root (works from *any* CWD thanks to pre-existing helper)
# --------------------------------------------------------------------------- #
from personalvibe import vibe_utils  # type: ignore

REPO = vibe_utils.get_base_path()

SRC = REPO / "src" / "personalvibe"
TESTS = REPO / "tests"


def write(path: Path, text: str) -> None:
    """(Over)write *path* with *text*, creating parent dirs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(text).lstrip(), encoding="utf-8")
    print(f"✅  wrote {path.relative_to(REPO)}")


# --------------------------------------------------------------------------- #
# 2. Create the CLI implementation
# --------------------------------------------------------------------------- #
CLI_PY = SRC / "cli.py"
CLI_CODE = """
    \"\"\"Personalvibe Command-Line Interface (Chunk A).

    After `poetry install`, a console-script named ``pv`` is available:

        pv milestone --config path/to/1.2.3.yaml --verbosity verbose
        pv sprint    --config cfg.yaml --prompt_only
        pv validate  --config cfg.yaml

    Internally this is just a *thin* wrapper that forwards options to
    :pyfunc:`personalvibe.run_pipeline.main`.
    \"\"\"

    from __future__ import annotations

    import argparse
    import sys
    from typing import List

    # Deferred import so we can monkey-patch ``sys.argv`` before the module’s
    # global-level argparse in run_pipeline is evaluated.
    def _forward_to_run_pipeline(argv: List[str]) -> None:
        sys.argv = ["personalvibe.run_pipeline"] + argv  # pretend we’re the module
        from personalvibe import run_pipeline  # local import

        run_pipeline.main()

    def cli_main() -> None:  # entry-point impl
        parser = argparse.ArgumentParser(prog="pv", description="Personalvibe CLI")
        sub = parser.add_subparsers(dest="mode", required=True, metavar="<mode>",
                                    help="Operation mode (yaml's 'mode' key should match).")

        def _add_common(p):
            p.add_argument("--config", required=True, help="Path to YAML config file.")
            p.add_argument("--verbosity", choices=["verbose", "none", "errors"], default="none")
            p.add_argument("--prompt_only", action="store_true")
            p.add_argument("--max_retries", type=int, default=5)

        for _mode in ("prd", "milestone", "sprint", "validate"):
            _add_common(sub.add_parser(_mode, help=f"{_mode} flow"))

        args = parser.parse_args()
        forwarded = [
            "--config",
            args.config,
            "--verbosity",
            args.verbosity,
        ]
        if args.prompt_only:
            forwarded.append("--prompt_only")
        if args.max_retries != 5:
            forwarded += ["--max_retries", str(args.max_retries)]

        _forward_to_run_pipeline(forwarded)

    # The entry-point declared in pyproject.toml
    def app() -> None:  # noqa: D401
        \"\"\"Poetry console-script shim.\"\"\"
        cli_main()

    if __name__ == "__main__":  # pragma: no cover
        cli_main()
"""
write(CLI_PY, CLI_CODE)

# --------------------------------------------------------------------------- #
# 3. Patch pyproject.toml  →  expose new console-script
# --------------------------------------------------------------------------- #
PYPROJECT = REPO / "pyproject.toml"
txt = PYPROJECT.read_text(encoding="utf-8")

# Capture the existing [tool.poetry.scripts] section (or create one)
if "[tool.poetry.scripts]" not in txt:
    txt += "\n[tool.poetry.scripts]\n"

pattern = r"(?s)(\[tool\.poetry\.scripts] *\n)(.*?)(\n\[|$)"
match = re.search(pattern, txt)
assert match, "Unable to locate [tool.poetry.scripts] section"
start, body, tail = match.group(1), match.group(2), match.group(3)


def _ensure(line: str, blob: str) -> str:
    return blob if line in blob else blob + line


body = _ensure('pv = "personalvibe.cli:app"\n', body)
body_lines = [ln for ln in body.splitlines() if not re.match(r"personalvibe\s*=", ln)]  # drop broken old entry
body_lines.append('personalvibe = "personalvibe.cli:app"')
body = "\n".join(sorted(set(body_lines), key=body_lines.index)) + "\n"

new_txt = txt.replace(start + match.group(2) + tail, start + body + tail)
PYPROJECT.write_text(new_txt, encoding="utf-8")
print("✅  patched pyproject.toml – console-script 'pv' added/fixed")

# --------------------------------------------------------------------------- #
# 4. Add minimal unit test  (subprocess call → pv --help)
# --------------------------------------------------------------------------- #
TEST_FILE = TESTS / "test_cli_basic.py"
TEST_CODE = """
    \"\"\"Smoke-test for the new ``pv`` entry-point.\"\"\"

    import subprocess
    import shutil
    from pathlib import Path

    def test_pv_help():
        exe = shutil.which("pv")
        assert exe, "'pv' console script not found – poetry install failed?"
        res = subprocess.run([exe, "--help"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert res.returncode == 0
        assert "Personalvibe CLI" in res.stdout
"""
write(TEST_FILE, TEST_CODE)

# --------------------------------------------------------------------------- #
# 5. Developer hint
# --------------------------------------------------------------------------- #
print(
    dedent(
        f"""
    --------------------------------------------------------------------
    Chunk A complete ✨

    • Run  `poetry install`  to refresh the entry-points.
    • Try `pv --help`          → CLI banner should appear.
    • `pytest -k cli`          → new test passes.

    Subsequent chunks will build on this CLI foundation.
    --------------------------------------------------------------------
    """
    )
)
