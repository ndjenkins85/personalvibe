# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/5.3.2.py

#!/usr/bin/env python
"""
Chunk-4 patch –  IO & UX hardening
==================================

This script applies the **Chunk 4** sprint changes:

1. YAML sanitiser  (`vibe_utils.sanitize_yaml_text`)
   • integrated into *all* YAML loads (run_pipeline & CLI)

2. Thread-safe `save_prompt()` (atomic create, race-safe)

3. `_open_in_editor()` honour `PV_SKIP_OPEN=1`

4. `tests/personalvibe.sh` gets `--open` flag (+ viewer logic)

5. New unit-tests:
   • tests/test_yaml_sanitizer.py
   • tests/test_open_in_editor.py

Run once – subsequent executions detect that the patch is already
present so nothing happens (idempotent).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()


# --------------------------------------------------------------------------- helpers
def _patch_file(path: Path, pattern: str, replacement: str) -> None:
    txt = path.read_text(encoding="utf-8")
    if re.search(pattern, txt, re.MULTILINE | re.DOTALL):
        # already patched
        return
    new_txt = re.sub(pattern, replacement, txt, flags=re.MULTILINE | re.DOTALL, count=1)
    if txt == new_txt:
        raise RuntimeError(f"Pattern not found while patching {path}")
    path.write_text(new_txt, encoding="utf-8")


def _ensure_contains(path: Path, snippet_marker: str, snippet_text: str) -> None:
    txt = "" if not path.exists() else path.read_text(encoding="utf-8")
    if snippet_marker in txt:
        return  # idempotent
    path.write_text(txt + "\n" + snippet_text, encoding="utf-8")


# --------------------------------------------------------------------------- 1. yaml sanitiser
vibe_utils_py = REPO / "src/personalvibe/vibe_utils.py"
if "def sanitize_yaml_text" not in vibe_utils_py.read_text(encoding="utf-8"):
    sanitize_fn = '''
# ----------------------------------------------------------------------
# YAML sanitiser  (Chunk-4)
# ----------------------------------------------------------------------
def sanitize_yaml_text(yaml_txt: str) -> str:
    """
    Strip ASCII control characters **except** TAB (\\x09), LF (\\x0A),
    CR (\\x0D).  Return the cleaned string **or** raise ``ValueError``
    if any disallowed rune remains after processing.
    """
    allowed = {9, 10, 13}
    cleaned = ''.join(
        (ch if (ord(ch) >= 32 or ord(ch) in allowed) else ' ')
        for ch in yaml_txt
    )
    if any(ord(ch) < 32 and ord(ch) not in allowed for ch in cleaned):
        raise ValueError("Invalid control character found in YAML after sanitisation.")
    return cleaned
'''
    # append at EOF
    _ensure_contains(vibe_utils_py, "YAML sanitiser  (Chunk-4)", sanitize_fn)

# --------------------------------------------------------------------------- 2. thread-safe save_prompt
if "FileExistsError" not in vibe_utils_py.read_text(encoding="utf-8"):
    _patch_file(
        vibe_utils_py,
        r"def save_prompt\([^\n]+?\n(.*?)return filepath",
        lambda m: re.sub(
            r"filepath\.write_text\([^)]*?\)",
            (
                "try:\n"
                "        # atomic create – fail if another process already wrote it\n"
                "        with filepath.open('x', encoding='utf-8') as _fh:\n"
                '            _fh.write(f"""{prompt}\\n### END PROMPT\\n""")\n'
                "    except FileExistsError:\n"
                "        log.info('Prompt was concurrently written – reusing existing file %s', filepath)\n"
                "    else:\n"
                "        log.info('Prompt saved to: %s', filepath)",
            ),
            m.group(0),
            flags=re.DOTALL,
        ),
    )

# --------------------------------------------------------------------------- 3. integrate sanitiser into YAML loads
run_pipeline_py = REPO / "src/personalvibe/run_pipeline.py"
if ".sanitize_yaml_text(" not in run_pipeline_py.read_text(encoding="utf-8"):
    _patch_file(
        run_pipeline_py,
        r"with open\(config_path,[^\n]+\) as f:\n\s+raw = yaml\.safe_load\(f\)",
        "text = Path(config_path).read_text(encoding='utf-8')\n"
        "        text = vibe_utils.sanitize_yaml_text(text)\n"
        "        raw = yaml.safe_load(text)",
    )

cli_py = REPO / "src/personalvibe/cli.py"
if ".sanitize_yaml_text(" not in cli_py.read_text(encoding="utf-8"):
    _patch_file(
        cli_py,
        r"with open\(ns\.config,[^\n]+\) as f:[^\n]+\n\s+_unused_mode = yaml\.safe_load\(f\)",
        "with open(ns.config, 'r', encoding='utf-8') as f:\n"
        "        _yaml_txt = vibe_utils.sanitize_yaml_text(f.read())\n"
        "        _unused_mode = yaml.safe_load(_yaml_txt).get('mode', '').strip()",
    )

# --------------------------------------------------------------------------- 4. _open_in_editor skip env
if "PV_SKIP_OPEN" not in cli_py.read_text(encoding="utf-8"):
    _patch_file(
        cli_py,
        r"def _open_in_editor\(path: Path\)[\s\S]+?try:",
        "def _open_in_editor(path: Path) -> None:\n"
        '    """Open *path* via $EDITOR or OS viewer – honour ``PV_SKIP_OPEN``."""\n'
        "    if os.getenv('PV_SKIP_OPEN') == '1':\n"
        "        return\n"
        "    editor = os.getenv('EDITOR')\n"
        "    try:",
    )

# --------------------------------------------------------------------------- 5. personalvibe.sh  --open flag
sh_path = REPO / "tests/personalvibe.sh"
if "--open" not in sh_path.read_text(encoding="utf-8"):
    sh_txt = sh_path.read_text(encoding="utf-8")
    # a) inject flag parser AFTER shebang & set -euo …
    sh_txt = sh_txt.replace(
        "set -euo pipefail",
        "set -euo pipefail\n\n"
        "# parse optional --open flag ---------------------------------\n"
        "OPEN_AFTER=0\n"
        "NEW_ARGS=()\n"
        'for a in "$@"; do\n'
        '  if [[ "$a" == "--open" ]]; then\n'
        "    OPEN_AFTER=1\n"
        "  else\n"
        '    NEW_ARGS+=("$a")\n'
        "  fi\n"
        "done\n"
        'set -- "${NEW_ARGS[@]}"',
    )
    # b) append viewer logic just before final success echo
    sh_txt = sh_txt.replace(
        'echo -e "\\n✅  personalvibe.sh finished ok."',
        'if [[ "$OPEN_AFTER" -eq 1 ]]; then\n'
        '  if [[ "${PV_SKIP_OPEN:-}" == "1" ]]; then\n'
        '    echo "Skipping automatic log open (PV_SKIP_OPEN=1)"\n'
        "  else\n"
        '    if command -v open &>/dev/null; then open "${LOG_FILE}";\n'
        '    elif command -v xdg-open &>/dev/null; then xdg-open "${LOG_FILE}";\n'
        '    else echo "No viewer available to open ${LOG_FILE}"; fi\n'
        "  fi\n"
        "fi\n\n"
        'echo -e "\\n✅  personalvibe.sh finished ok."',
    )
    sh_path.write_text(sh_txt, encoding="utf-8")
    os.chmod(sh_path, 0o755)

# --------------------------------------------------------------------------- 6. add new tests
tests_dir = REPO / "tests"
yaml_test = tests_dir / "test_yaml_sanitizer.py"
if not yaml_test.exists():
    yaml_test.write_text(
        """
from pathlib import Path

from personalvibe.run_pipeline import load_config


def test_yaml_control_chars_ok(tmp_path: Path):
    cfg = tmp_path / "bad.yaml"
    # stray \\x01 in the middle of the file
    cfg.write_text("project_name: demo\\x01\\nmode: milestone\\nexecution_details: ''\\ncode_context_paths: []", "utf-8")
    model = load_config(str(cfg))
    assert model.project_name == "demo"
""",
        encoding="utf-8",
    )

open_test = tests_dir / "test_open_in_editor.py"
if not open_test.exists():
    open_test.write_text(
        """
import subprocess
from pathlib import Path
from unittest import mock

import personalvibe.cli as cli


def test_open_in_editor_linux(monkeypatch, tmp_path):
    dummy = tmp_path / "x.txt"
    dummy.write_text("hello", "utf-8")
    called = {}

    def _fake_call(cmd, **_):
        called["cmd"] = cmd
        return 0

    monkeypatch.setenv("PV_SKIP_OPEN", "0")
    monkeypatch.delenv("EDITOR", raising=False)
    monkeypatch.setattr(subprocess, "call", _fake_call)
    monkeypatch.setattr(cli.platform, "system", lambda: "Linux")

    cli._open_in_editor(dummy)
    assert called["cmd"][0] in ("xdg-open", "open")
    assert called["cmd"][1] == str(dummy)
""",
        encoding="utf-8",
    )

# --------------------------------------------------------------------------- done
print(
    """
✅  Chunk-4 patch applied.

WHAT CHANGED
------------
• vibe_utils.sanitize_yaml_text – strips naughty control chars (<0x20)
  and is now used by run_pipeline & cli for every YAML read.

• save_prompt – atomic, race-safe (`open('x')`) to avoid duplicates when
  parallel jobs hit the same hash concurrently.

• _open_in_editor – respects  PV_SKIP_OPEN=1  (handy for CI) and is
  used by new-milestone / prepare-sprint helpers.

• tests/personalvibe.sh  now accepts a  --open  flag that launches the
  log file with  open/xdg-open  unless PV_SKIP_OPEN=1.

NEW TESTS
---------
• test_yaml_sanitizer.py    – verifies control-char YAML loads OK.
• test_open_in_editor.py    – stubs subprocess.call to ensure correct
  viewer command on Linux path.

NEXT STEPS
----------
1.  poetry run nox -s lint tests
    # all tests (incl. new ones) should pass

2.  Manually try:
        bash tests/personalvibe.sh dev --open
    then:
        PV_SKIP_OPEN=1 bash tests/personalvibe.sh dev --open
    to confirm viewer behaviour.

3.  Proceed with Chunk 5 documentation restructure.

"""
)
