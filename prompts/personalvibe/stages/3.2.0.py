# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/3.2.0.py

#!/usr/bin/env python
"""
Patch-script  –  Milestone 3.0.0 / Chunk 2
================================================
Resource & path resolver
    • move command templates into package  `personalvibe.data`
    • add flexible loader that prefers importlib.resources
    • override get_replacements() to use the new loader
    • ship regression tests

Run with:  poetry run python patch_chunk2.py
"""
from __future__ import annotations

import shutil
import textwrap
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()

# --------------------------------------------------------------------------- #
# 1.  Create package  src/personalvibe/data/  with the *.md templates
# --------------------------------------------------------------------------- #
data_pkg = REPO / "src" / "personalvibe" / "data"
data_pkg.mkdir(parents=True, exist_ok=True)
(data_pkg / "__init__.py").touch(exist_ok=True)

# Helper: copy existing cmds OR write stub
cmd_dir = REPO / "src" / "personalvibe" / "commands"
for name in ("milestone.md", "sprint.md", "validate.md"):
    target = data_pkg / name
    if target.exists():
        continue

    src_file = cmd_dir / name
    if src_file.exists():
        shutil.copy(src_file, target)
    else:  # fallback stub
        target.write_text(
            textwrap.dedent(
                f"""
                # {name}
                This is a *placeholder* template created by Chunk 2.
                Future sprints will overwrite it with real content.
                """
            ).lstrip(),
            encoding="utf-8",
        )

print(f"✅  Templates confirmed inside package: {list(p.name for p in data_pkg.glob('*.md'))}")


# --------------------------------------------------------------------------- #
# 2.  Patch vibe_utils.py  (append helper + new get_replacements)
# --------------------------------------------------------------------------- #
vu_path = REPO / "src" / "personalvibe" / "vibe_utils.py"
assert vu_path.exists(), f"vibe_utils.py not found at {vu_path}"

patch_txt = """
# ----------------------------------------------------------------------
# PERSONALVIBE CHUNK 2 – Resource loader
# ----------------------------------------------------------------------
from importlib import resources
from pathlib import Path as _Path
import logging as _logging

_log = _logging.getLogger(__name__)


def _load_template(fname: str) -> str:
    \"\"\"Return the *text* of a template shipped as package-data.

    Resolution order
    ----------------
    1. `importlib.resources.files('personalvibe.data')/fname`
    2. Legacy path  src/personalvibe/commands/<fname>
    \"\"\"
    try:
        pkg_file = resources.files("personalvibe.data").joinpath(fname)
        return pkg_file.read_text(encoding="utf-8")
    except Exception:  # noqa: BLE001
        legacy = _Path(__file__).parent / "commands" / fname
        if legacy.exists():
            _log.debug("Template %s loaded from legacy path %s", fname, legacy)
            return legacy.read_text(encoding="utf-8")
        raise FileNotFoundError(f"Template {fname!s} not found in package or legacy path")


# ----------------------------- override -------------------------------------
def get_replacements(config, code_context: str) -> dict:  # type: ignore[override]
    \"\"\"Build the Jinja replacement map (rev-2 using _load_template).\"\"\"

    _log.info("Running config version: %s", config.version)
    _log.info("Running mode = %s", config.mode)
    milestone_ver, sprint_ver, bugfix_ver = config.version.split(".")  # noqa: F841

    if config.mode == "prd":
        exec_task = config.execution_task
        instructions = ""
    elif config.mode == "milestone":
        exec_task = "conduct milestone analysis according to guidelines"
        instructions = _load_template("milestone.md")
    elif config.mode == "sprint":
        exec_task = f"perform the sprint number marked {sprint_ver}"
        instructions = _load_template("sprint.md") + "\\n" + _get_milestone_text(config)
    elif config.mode == "validate":
        exec_task = f"validate the following logs following the generation of sprint {sprint_ver}"
        instructions = (
            _load_template("validate.md") + "\\n" + _get_milestone_text(config) + "\\n" + _get_error_text(config)
        )
    else:  # pragma: no cover
        raise ValueError(f"Unsupported mode {config.mode}")

    return {
        "execution_task": exec_task,
        "execution_details": config.execution_details,
        "instructions": instructions,
        "code_context": code_context,
    }
"""
# Append once – guard against duplicate
marker = "PERSONALVIBE CHUNK 2 – Resource loader"
src_txt = vu_path.read_text(encoding="utf-8")
if marker not in src_txt:
    vu_path.write_text(src_txt + patch_txt, encoding="utf-8")
    print("✅  vibe_utils patched with _load_template & new get_replacements()")
else:
    print("ℹ️  vibe_utils already patched – skipping")

# --------------------------------------------------------------------------- #
# 3.  Add pytest  tests/test_resource_fallback.py
# --------------------------------------------------------------------------- #
tests_dir = REPO / "tests"
tests_dir.mkdir(exist_ok=True)
test_file = tests_dir / "test_resource_fallback.py"

if not test_file.exists():
    test_file.write_text(
        textwrap.dedent(
            '''
            # Copyright © 2025 by Nick Jenkins.

            """Resource loader fallback tests."""

            import importlib.resources
            from unittest import mock

            from personalvibe import vibe_utils


            def test_load_template_package():
                txt = vibe_utils._load_template("milestone.md")
                assert "language model" in txt.lower() or len(txt) > 20


            def test_load_template_legacy(monkeypatch):
                """Force package path to fail → must fall back to legacy file."""
                def _raise(*_, **__):
                    raise FileNotFoundError

                with mock.patch.object(importlib.resources, "files", _raise):
                    txt = vibe_utils._load_template("milestone.md")
                    assert "language model" in txt.lower() or len(txt) > 20
            '''
        ).lstrip(),
        encoding="utf-8",
    )
    print(f"✅  Added {test_file.relative_to(REPO)}")

# --------------------------------------------------------------------------- #
# 4.  Developer hint
# --------------------------------------------------------------------------- #
print(
    """
    --------------------------------------------------------------------
    Chunk 2 completed.

    • Templates are now loaded via importlib.resources, ensuring they are
      available both inside the source repo *and* when installed as a wheel.
    • vibe_utils.get_replacements has been overridden; all callers get
      the new behaviour automatically.
    • New pytest suite: tests/test_resource_fallback.py

    Next step:  run  `poetry run nox -s tests`  to verify green tests.
    --------------------------------------------------------------------
    """
)
