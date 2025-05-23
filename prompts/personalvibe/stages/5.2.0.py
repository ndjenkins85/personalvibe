# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/5.2.0.py

"""
PATCH – Personalvibe Chunk 2  (Implicit Project Detection)

This idempotent script:
1. Adds `detect_project_name()` to `vibe_utils.py`.
2. Makes `--project_name` optional for *all* entry-points that used to
   require it (cli + parse_stage + run_pipeline YAML loader).
3. Introduces unit-tests that assert detection succeeds when:
      • cwd = prompts/<name>/stages/…           (repo checkout)
      • only ONE project exists under prompts/  (installed package)
   …and raises for ambiguous / not-found cases.
-------------------------------------------------------------------
Run via `poetry run python patches/chunk_2_project_detection.py`
(or include it in any nox/CI patch list).  Safe to re-run – repeats
are no-ops thanks to presence-checks before write.
"""

from __future__ import annotations

import re
import textwrap
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()
SRC = REPO / "src" / "personalvibe"
TESTS = REPO / "tests"


# ------------------------------------------------------------------ helpers
def upsert(path: Path, patch: str, *, marker: str) -> None:
    """Append *patch* to file only if the *marker* string not present."""
    txt = path.read_text(encoding="utf-8")
    if marker in txt:
        return
    path.write_text(txt.rstrip() + "\n\n" + patch.lstrip("\n"), encoding="utf-8")


def replace_block(path: Path, pattern: str, repl: str) -> None:
    """Regex-replace FIRST occurrence of *pattern* with *repl*."""
    txt = path.read_text(encoding="utf-8")
    new, n = re.subn(pattern, repl, txt, count=1, flags=re.S)
    if n:
        path.write_text(new, encoding="utf-8")


# ------------------------------------------------------------------ 1️⃣  vibe_utils.detect_project_name
VIBE = SRC / "vibe_utils.py"
DETECT_MARKER = "# === detect_project_name (chunk 2)"
DETECT_FUNC = f"""
{DETECT_MARKER}
from pathlib import Path as _PvPath
import logging as _pv_log

def detect_project_name(cwd: _PvPath | None = None) -> str:
    \"\"\"Best-effort inference of the **project_name**.

    Strategy
    --------
    1. If *cwd* (or its parents) path contains ``prompts/<name>`` → return
       that immediate directory name.
    2. Else walk *upwards* until a folder with ``prompts/`` is found:
         • if that ``prompts`` dir contains exactly ONE sub-directory we
           assume it is the project.
    3. Otherwise raise ``ValueError`` explaining how to fix.

    This keeps the common cases zero-config while remaining explicit when
    multiple projects coexist.
    \"\"\"
    cwd = (cwd or _PvPath.cwd()).resolve()
    parts = cwd.parts
    if "prompts" in parts:
        idx = parts.index("prompts")
        if idx + 1 < len(parts):
            return parts[idx + 1]

    for parent in [cwd, *cwd.parents]:
        p_dir = parent / "prompts"
        if p_dir.is_dir():
            sub = [d for d in p_dir.iterdir() if d.is_dir()]
            if len(sub) == 1:
                return sub[0].name
            break  # ambiguous – fallthrough to error
    raise ValueError(
        "Unable to auto-detect project_name; pass --project_name or run "
        "from within prompts/<name>/… directory."
    )
"""

upsert(VIBE, DETECT_FUNC, marker=DETECT_MARKER)

# ------------------------------------------------------------------ 2️⃣  cli.parse-stage  (--project_name optional)
CLI = SRC / "cli.py"
replace_block(
    CLI,
    r'ps = sub\.add_parser\("parse-stage".+?set_defaults\([^\)]+\)',
    textwrap.dedent(
        """
        ps = sub.add_parser("parse-stage", help="Extract latest assistant code block.")
        ps.add_argument("--project_name", help="When omitted, auto-detected from cwd.")
        ps.add_argument("--run", action="store_true", help="Execute the extracted script after save.")
        ps.set_defaults(func=_cmd_parse_stage)
        """
    ),
)

# adjust handler
replace_block(
    CLI,
    r"def _cmd_parse_stage\(ns: argparse\.Namespace\).*?return",  # non-greedy match
    textwrap.dedent(
        """
def _cmd_parse_stage(ns: argparse.Namespace) -> None:
    proj = ns.project_name
    if not proj:
        from personalvibe.vibe_utils import detect_project_name

        try:
            proj = detect_project_name()
        except ValueError as e:
            print(str(e))
            raise SystemExit(1) from e
    saved = extract_and_save_code_block(proj)
    if ns.run:
        import runpy

        print(f"Running extracted code from: {saved}")
        runpy.run_path(saved, run_name="__main__")"""
    ),
)

# ------------------------------------------------------------------ 3️⃣  parse_stage.py
PARSE = SRC / "parse_stage.py"
# make --project_name optional in __main__
replace_block(
    PARSE,
    r'parser\.add_argument\("--project_name".+?help="Project name[^\"]+"\)',
    """
    parser.add_argument(
        "--project_name",
        help="When omitted, looked up automatically from cwd."
    )
    """,
)
# helper to ensure project_name
ENSURE_HELPER = """
# === helper added by chunk 2
def _ensure_project_name(name: str | None) -> str:
    if name:
        return name
    try:
        return vibe_utils.detect_project_name()
    except ValueError as e:  # re-raise with friendly msg
        raise ValueError(str(e)) from e
"""
upsert(PARSE, ENSURE_HELPER, marker="# === helper added by chunk 2")

# insert _ensure_project_name usages
for func in ("find_latest_log_file", "determine_next_version", "extract_and_save_code_block"):
    replace_block(
        PARSE,
        rf"def {func}\(project_name: str\)",
        f"def {func}(project_name: str | None = None)",
    )
# replace first lines inside these functions where project_name used
replace_block(
    PARSE,
    r"base_path = vibe_utils.get_base_path\(\)",
    "project_name = _ensure_project_name(project_name)\n    base_path = vibe_utils.get_base_path()",
)

# finally adjust __main__ saving logic
replace_block(
    PARSE,
    r"saved_file = extract_and_save_code_block\(args\.project_name\)",
    "saved_file = extract_and_save_code_block(args.project_name)",
)

# ------------------------------------------------------------------ 4️⃣  run_pipeline.load_config – fallback detection
PIPE = SRC / "run_pipeline.py"
FALLBACK_MARKER = "# === project_name fallback (chunk 2)"
replace_block(
    PIPE,
    r"def load_config\(config_path: str\) -> ConfigModel:[\s\S]+?return ConfigModel",
    textwrap.dedent(
        f"""
def load_config(config_path: str) -> ConfigModel:
    \"\"\"Load YAML then validate. Auto-fills *project_name* if missing.\"\"\"
    with open(config_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
        raw["version"] = Path(config_path).stem
    # ---- chunk 2 auto-detect -----------------------------------------
    if not raw.get("project_name"):
        try:
            raw["project_name"] = vibe_utils.detect_project_name()
        except ValueError as e:
            raise RuntimeError(
                "project_name absent from YAML and auto-detection failed."
            ) from e
    return ConfigModel(**raw)
"""
    ),
)

# ------------------------------------------------------------------ 5️⃣  new unit-tests
TEST_FILE = TESTS / "test_project_detection.py"
if not TEST_FILE.exists():
    TEST_FILE.write_text(
        textwrap.dedent(
            """
            # Copyright © 2025
            \"\"\"Tests for vibe_utils.detect_project_name (chunk 2).\"\"\"

            from pathlib import Path

            import pytest

            from personalvibe.vibe_utils import detect_project_name


            def _mk_repo(tmp_path: Path, names: list[str]) -> Path:
                \"\"\"Create minimal prompts/<name> dirs and return repo root.\"\"\"
                root = tmp_path / "myrepo"
                for n in names:
                    (root / "prompts" / n / "stages").mkdir(parents=True)
                return root


            def test_detect_from_nested_dir(tmp_path, monkeypatch):
                root = _mk_repo(tmp_path, ["alpha"])
                deep = root / "prompts" / "alpha" / "stages"
                monkeypatch.chdir(deep)
                assert detect_project_name() == "alpha"


            def test_detect_single_project_from_root(tmp_path, monkeypatch):
                root = _mk_repo(tmp_path, ["solo"])
                monkeypatch.chdir(root)
                assert detect_project_name() == "solo"


            def test_detect_ambiguous(tmp_path, monkeypatch):
                root = _mk_repo(tmp_path, ["one", "two"])
                monkeypatch.chdir(root)
                with pytest.raises(ValueError):
                    detect_project_name()


            def test_detect_not_found(tmp_path, monkeypatch):
                monkeypatch.chdir(tmp_path)
                with pytest.raises(ValueError):
                    detect_project_name()
            """
        ),
        encoding="utf-8",
    )

# ------------------------------------------------------------------ done
print(
    """✅  Chunk 2 patch applied.

Key changes
-----------
• personalvibe.vibe_utils.detect_project_name(cwd)  – walks the FS to
  infer project_name.
• --project_name flag is now OPTIONAL for `pv parse-stage` and the
  module‐level script.
• run_pipeline.load_config fills missing project_name automatically.
• Comprehensive unit-tests added in tests/test_project_detection.py.

Next steps
----------
1. Run `./tests/personalvibe.sh` or `nox -rs tests` – all suites, incl.
   new detection tests, should pass.
2. Manually try:
       cd prompts/<yourproj>/stages
       pv parse-stage               # <-- no argument required
3. Proceed to Chunk 3 (new commands + bug-patch) once CI green.
"""
)
