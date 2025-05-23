# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/5.3.3.py

"""
patch_chunk_4.py  –  Personalvibe “IO & UX Hardening” sprint

Run once from anywhere inside the repo:

    poetry run python patch_chunk_4.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()


# --------------------------------------------------------------------------- generic helpers
def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: Path, txt: str) -> None:
    path.write_text(txt, encoding="utf-8")


def _patch_file(path: Path, pattern: str, replacement: str) -> None:
    txt = _read(path)
    if replacement.strip() in txt:  # idempotent – already patched
        return
    new = txt.replace(pattern, replacement)
    if new == txt:
        raise RuntimeError(f"Pattern not found while patching {path}")
    _write(path, new)


def _ensure_new_file(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    _write(path, content)


# --------------------------------------------------------------------------- 1) YAML sanitiser util
_yaml_utils_py = REPO / "src/personalvibe/yaml_utils.py"
_ensure_new_file(
    _yaml_utils_py,
    """
\"\"\"Utility helpers for **robust YAML loading** (Chunk-4).

Public API
----------
sanitize_yaml_text(text: str, *, origin: str | None = None) -> str
    • strips ASCII control chars 0x00-0x1F (except \\n, \\r, \\t)
    • raises *ValueError* on any remaining surrogate code-points
\"\"\"

from __future__ import annotations

import re

# Control characters excluding \\n, \\r, \\t
_CTRL = ''.join(chr(i) for i in range(32) if chr(i) not in '\\n\\r\\t')
_CTRL_RE = re.compile(f'[{re.escape(_CTRL)}]')

# UTF-16 surrogate range (invalid in well-formed Unicode text)
_SURROGATE_RE = re.compile(r'[\\uD800-\\uDFFF]')


def sanitize_yaml_text(text: str, *, origin: str | None = None) -> str:
    \"\"\"Strip *dangerous* runes before YAML parsing.

    Parameters
    ----------
    text
        Raw YAML string.
    origin
        Helpful file-path inserted into raised error messages.

    Returns
    -------
    str
        Cleaned text suitable for ``yaml.safe_load``.
    \"\"\"
    cleaned = _CTRL_RE.sub(' ', text)

    # Surrogates should never appear in valid UTF-8 files
    m = _SURROGATE_RE.search(cleaned)
    if m:
        bad = repr(m.group(0))
        raise ValueError(f'Invalid Unicode rune {bad} found while reading YAML {origin or ""}'.strip())

    return cleaned
""",
)

# --------------------------------------------------------------------------- 2) patch run_pipeline.load_config
_run_pipeline_py = REPO / "src/personalvibe/run_pipeline.py"
_pattern = "raw = yaml.safe_load(f)"
_replacement = """from personalvibe.yaml_utils import sanitize_yaml_text as _pv_yaml_sanitise
            _yaml_txt = sanitize_yaml_text(f.read(), origin=config_path)
            raw = yaml.safe_load(_yaml_txt)"""
_patch_file(_run_pipeline_py, _pattern, _replacement)  # noqa: E501

# --------------------------------------------------------------------------- 3) thread-safe save_prompt
_vibe_utils_py = REPO / "src/personalvibe/vibe_utils.py"
if "atomic write (Chunk-4)" not in _read(_vibe_utils_py):
    patt = "filepath.write_text("
    new_block = """
    # --- atomic write (Chunk-4) -----------------------------------------
    content = f\"\"\"{prompt}
### END PROMPT
\"\"\"
    try:
        with filepath.open('x', encoding='utf-8') as fh:  # exclusive create
            fh.write(content)
        log.info("Prompt saved to: %s", filepath)
    except FileExistsError:
        # Race: another process created the file in the tiny gap – fine.
        log.warning("Prompt already exists (race-condition handled): %s", filepath)
    return filepath
"""
    # remove existing write_text implementation (up to return filepath)
    txt = _read(_vibe_utils_py)
    txt = re.sub(
        r"filepath\.write_text\([^\n]+\n\s*log\.info\([^\n]+\)\n\s*return filepath",
        new_block.strip("\n"),
        txt,
        count=1,
    )
    _write(_vibe_utils_py, txt)

# --------------------------------------------------------------------------- 4) --open flag in tests/personalvibe.sh
_pv_sh = REPO / "tests/personalvibe.sh"
if "--open" not in _read(_pv_sh):
    txt = _read(_pv_sh)
    header_pat = "set -euo pipefail"
    open_logic = r"""
# ------------------------------ flag parsing (Chunk-4) -------------------------
OPEN_LOG=0
_REST_ARGS=()
for arg in "$@"; do
  if [[ "$arg" == "--open" ]]; then
      OPEN_LOG=1
  else
      _REST_ARGS+=("$arg")
  fi
done
# refill $@ with *remaining* args (passed through to nox)
set -- "${_REST_ARGS[@]}"
"""
    txt = txt.replace(header_pat, f"{header_pat}\n{open_logic}")
    # insert open invocation before final success banner
    txt = txt.replace(
        'echo -e "\\n✅  personalvibe.sh finished ok."',
        """# Auto-open log if caller requested -------------------------------------
if [[ "$OPEN_LOG" -eq 1 ]]; then
  echo "📂  Opening log file ${LOG_FILE} …"
  if command -v open &>/dev/null; then
      open "${LOG_FILE}"
  elif command -v xdg-open &>/dev/null; then
      xdg-open "${LOG_FILE}"
  else
      echo "WARN: could not locate a suitable 'open' command." >&2
  fi
fi

echo -e "\\n✅  personalvibe.sh finished ok."
""",
    )
    _write(_pv_sh, txt)

# --------------------------------------------------------------------------- 5) new unit-tests ---------------------------------------------------
_tests_dir = REPO / "tests"
_ensure_new_file(
    _tests_dir / "test_yaml_sanitiser.py",
    """
# Copyright © 2025

\"\"\"Tests for the YAML sanitiser introduced in Chunk-4.\"\"\"

from pathlib import Path

import pytest

from personalvibe.run_pipeline import load_config


def _mk_cfg(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "cfg.yaml"
    p.write_text(body, encoding="utf-8")
    return p


def test_control_chars_stripped(tmp_path: Path):
    txt = (
        "project_name: demo\\n"
        "mode: milestone\\n"
        "execution_details: \\"bad\\x07value\\"\\n"
        "code_context_paths: []\\n"
    )
    cfg = load_config(str(_mk_cfg(tmp_path, txt)))
    assert cfg.execution_details == "bad value"


def test_invalid_surrogate_raises(tmp_path: Path):
    bad = (
        "project_name: demo\\n"
        "mode: milestone\\n"
        "execution_details: \\"oops\\ud800oops\\"\\n"
        "code_context_paths: []\\n"
    )
    with pytest.raises(ValueError):
        load_config(str(_mk_cfg(tmp_path, bad)))
""",
)

_ensure_new_file(
    _tests_dir / "test_personalvibe_sh_open_flag.py",
    """
\"\"\"Static test ensuring the '--open' enhancement exists in script.\"\"\"

from pathlib import Path

from personalvibe import vibe_utils


def test_open_flag_present():
    script = vibe_utils.get_base_path() / "tests/personalvibe.sh"
    txt = script.read_text(encoding="utf-8")
    assert "--open" in txt
    assert "open \\\"${LOG_FILE}\\\"" in txt or "xdg-open \\\"${LOG_FILE}\\\"" in txt
""",
)

# --------------------------------------------------------------------------- done
print(
    """
✅  Chunk-4 patch applied.

What changed?
-------------
1.  src/personalvibe/yaml_utils.py
    • new sanitize_yaml_text() helper to strip control chars and
      reject UTF-16 surrogate runes.

2.  src/personalvibe/run_pipeline.py
    • load_config() now sanitises YAML before yaml.safe_load().

3.  src/personalvibe/vibe_utils.py
    • save_prompt() rewired to atomic 'x' mode write for race-safety.

4.  tests/personalvibe.sh
    • added '--open' flag.  When supplied, opens the generated log
      file via `open` (mac) or `xdg-open` (Linux).

5.  New tests
      tests/test_yaml_sanitiser.py
      tests/test_personalvibe_sh_open_flag.py

Next steps
----------
• Run `tests/personalvibe.sh --open` locally to verify UX on your OS.
• CI should now pass all tests including the new sanitiser path.
• Keep an eye on any downstream YAML readers that bypass
  run_pipeline.load_config – they may also need sanitisation.

"""
)
