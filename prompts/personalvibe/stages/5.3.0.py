# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/5.3.0.py

#!/usr/bin/env python
"""Chunk 3 – New milestone / sprint helpers + patch-version fix.

Run via:

    poetry run python chunks/chunk3_patch.py

The script is **idempotent** – re-running never duplicates code.
"""

from __future__ import annotations

import os
import re
import sys
import textwrap
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()
SRC = REPO / "src" / "personalvibe"


# --------------------------------------------------------------------------- #
# Utility helpers
# --------------------------------------------------------------------------- #
def replace_block(path: Path, anchor: str, new_block: str) -> None:
    """Insert or replace a named code-block inside *path* (idempotent)."""
    txt = path.read_text(encoding="utf-8")
    pattern = re.compile(rf"(?s)# === {re.escape(anchor)} START ===.*?# === {re.escape(anchor)} END ===")
    wrapped = f"# === {anchor} START ===\n{new_block}\n# === {anchor} END ==="
    if pattern.search(txt):
        txt = pattern.sub(wrapped, txt)
    else:
        # append right before EOF so re-import order unaffected
        txt = f"{txt.rstrip()}\n\n{wrapped}\n"
    path.write_text(txt, encoding="utf-8")


def ensure_line_in_file(path: Path, line: str) -> None:
    txt = path.read_text(encoding="utf-8").splitlines()
    if line not in txt:
        txt.append(line)
        path.write_text("\n".join(txt) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# 1)  Patch parse_stage.determine_next_version  (bug-fix → bump BUGFIX)
# --------------------------------------------------------------------------- #
parse_stage_path = SRC / "parse_stage.py"
new_logic = textwrap.dedent(
    '''
    def determine_next_version(project_name: str | None = None) -> str:  # noqa: C901
        """Return the *next* semantic version for **patch-files** (x.y.Z).

        Rules
        -----
        • If **no** existing stage files ⇒ ``1.1.0`` (first sprint).
        • Else **always increment the *bug-fix* component** of the latest
          file found, e.g.  ``4.3.0 → 4.3.1``  or  ``2.7.4 → 2.7.5``.
        • Version scan looks at ``prompts/<project>/stages/*.(md|py)``.

        This fixes the long-standing bug where _determine_next_version()
        bumped the *sprint* instead of the *bug-fix* number.
        """
        base_path = vibe_utils.get_base_path()
        if project_name is None:
            raise ValueError("project_name must be provided")
        stages_dir = Path(base_path, "prompts", project_name, "stages")
        stages_dir.mkdir(parents=True, exist_ok=True)

        files = list(stages_dir.glob("*.py")) + list(stages_dir.glob("*.md"))
        version_tuples: list[tuple[int, int, int]] = []
        for f in files:
            m = re.match(r"^(\\d+)\\.(\\d+)\\.(\\d+)\\..*$", f.name)
            if m:
                version_tuples.append(tuple(map(int, m.groups())))

        if not version_tuples:
            # first ever sprint under major-1
            return "1.1.0"

        version_tuples.sort()
        latest_major, latest_sprint, latest_bug = version_tuples[-1]
        return f"{latest_major}.{latest_sprint}.{latest_bug + 1}"
'''
)

replace_block(parse_stage_path, "CHUNK3_determine_next_version", new_logic)

# --------------------------------------------------------------------------- #
# 2)  Add milestone / sprint YAML templates under package-data
# --------------------------------------------------------------------------- #
data_dir = SRC / "data"
data_dir.mkdir(parents=True, exist_ok=True)

templates = {
    "milestone_template.yaml": textwrap.dedent(
        """\
        # Personalvibe milestone configuration
        project_name: {{ project_name }}
        mode: milestone
        execution_details: ''
        code_context_paths: []
        """
    ),
    "sprint_template.yaml": textwrap.dedent(
        """\
        # Personalvibe sprint configuration
        project_name: {{ project_name }}
        mode: sprint
        execution_details: ''
        code_context_paths: []
        """
    ),
}

for fname, body in templates.items():
    fpath = data_dir / fname
    if not fpath.exists():
        fpath.write_text(body, encoding="utf-8")

# Ensure build includes *.yaml
pyproject = REPO / "pyproject.toml"
ensure_line_in_file(
    pyproject, 'include = ["LICENSE", "README.md", "src/personalvibe/data/*.md", "src/personalvibe/data/*.yaml"]'
)

# --------------------------------------------------------------------------- #
# 3)  Extend CLI with  pv new-milestone  &  pv prepare-sprint
# --------------------------------------------------------------------------- #
cli_path = SRC / "cli.py"

cli_block = textwrap.dedent(
    '''
    # ----------------------------------------------------------------- helpers
    def _open_in_editor(path: Path) -> None:
        """Best-effort open *path* either in $EDITOR or OS default viewer."""
        import subprocess
        import platform
        editor = os.getenv("EDITOR")
        try:
            if editor:
                subprocess.call([editor, str(path)])
            elif platform.system() == "Darwin":
                subprocess.call(["open", str(path)])
            else:
                subprocess.call(["xdg-open", str(path)])
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] Unable to open {path}: {exc}", file=sys.stderr)

    def _scan_versions(stages_dir: Path) -> list[tuple[int, int, int]]:
        vers = []
        for f in stages_dir.glob("*.*"):
            m = re.match(r"^(\\d+)\\.(\\d+)\\.(\\d+)\\..*$", f.name)
            if m:
                vers.append(tuple(map(int, m.groups())))
        return sorted(vers)

    # ----------------------------------------------------------------- NM
    def _cmd_new_milestone(ns: argparse.Namespace) -> None:
        proj = ns.project_name or vibe_utils.detect_project_name()
        stages = vibe_utils.get_base_path() / "prompts" / proj / "stages"
        stages.mkdir(parents=True, exist_ok=True)
        versions = _scan_versions(stages)
        next_major = (versions[-1][0] + 1) if versions else 1
        ver_str = f"{next_major}.0.0"
        dest = Path.cwd() / f"{ver_str}.yaml"

        # copy template
        tmpl = vibe_utils._load_template("milestone_template.yaml")
        dest.write_text(tmpl.replace("{{ project_name }}", proj), encoding="utf-8")
        print(f"Created new milestone YAML: {dest}")
        if not ns.no_open:
            _open_in_editor(dest)

    # ----------------------------------------------------------------- PS
    def _cmd_prepare_sprint(ns: argparse.Namespace) -> None:
        proj = ns.project_name or vibe_utils.detect_project_name()
        stages = vibe_utils.get_base_path() / "prompts" / proj / "stages"
        stages.mkdir(parents=True, exist_ok=True)
        versions = _scan_versions(stages)

        if not versions:
            # no sprints yet – assume major 1
            next_ver = "1.1.0"
        else:
            latest = versions[-1]
            next_ver = f"{latest[0]}.{latest[1] + 1}.0"  # bump sprint

        dest = Path.cwd() / f"{next_ver}.yaml"
        tmpl = vibe_utils._load_template("sprint_template.yaml")
        dest.write_text(tmpl.replace("{{ project_name }}", proj), encoding="utf-8")
        print(f"Created sprint YAML: {dest}")
        if not ns.no_open:
            _open_in_editor(dest)
'''
)
replace_block(cli_path, "CHUNK3_cli_helpers_cmds", cli_block)

# --------------------------------------------------------------------------- #
# 3b)  Patch CLI parser additions
# --------------------------------------------------------------------------- #
parser_patch = textwrap.dedent(
    """
        # new-milestone -------------------------------------------------
        nm = sub.add_parser("new-milestone", help="Scaffold next milestone YAML")
        nm.add_argument("--project_name", help="Override auto detection.")
        nm.add_argument("--no-open", action="store_true", help="Skip opening editor/viewer.")
        nm.set_defaults(func=_cmd_new_milestone)

        # prepare-sprint -----------------------------------------------
        pspr = sub.add_parser("prepare-sprint", help="Scaffold next sprint YAML")
        pspr.add_argument("--project_name", help="Override auto detection.")
        pspr.add_argument("--no-open", action="store_true")
        pspr.set_defaults(func=_cmd_prepare_sprint)
"""
)

# inject right before "parse-stage ---" banner
cli_txt = cli_path.read_text(encoding="utf-8")
if "prepare-sprint" not in cli_txt:
    cli_txt = cli_txt.replace(
        "# parse-stage ---",
        parser_patch + "\n    # parse-stage ---",
    )
    cli_path.write_text(cli_txt, encoding="utf-8")

# --------------------------------------------------------------------------- #
# 4)  Add regression tests
# --------------------------------------------------------------------------- #
tests_dir = REPO / "tests"

# 4.1 determine_next_version bug-fix
test_bugfix = tests_dir / "test_determine_next_version.py"
if not test_bugfix.exists():
    test_bugfix.write_text(
        textwrap.dedent(
            """
            from pathlib import Path
            from personalvibe.parse_stage import determine_next_version
            from personalvibe import vibe_utils

            def _prep(tmp_path: Path):
                root = tmp_path / "repo"
                stages = root / "prompts" / "demo" / "stages"
                stages.mkdir(parents=True)
                return root, stages

            def test_bugfix_increment(monkeypatch, tmp_path):
                root, stages = _prep(tmp_path)
                # fake repo root lookup
                monkeypatch.patch.object(vibe_utils, "get_base_path", lambda: root)
                # existing sprint file 4.3.0.py
                (stages / "4.3.0.py").write_text("# dummy")
                nxt = determine_next_version("demo")
                assert nxt == "4.3.1"
            """
        ),
        encoding="utf-8",
    )

# 4.2 new CLI commands
test_cli_new = tests_dir / "test_cli_new_cmds.py"
if not test_cli_new.exists():
    test_cli_new.write_text(
        textwrap.dedent(
            """
            import os
            from pathlib import Path
            from personalvibe import cli, vibe_utils

            def _mk_repo(tmp_path: Path):
                root = tmp_path / "repo"
                stages = root / "prompts" / "demo" / "stages"
                stages.mkdir(parents=True)
                # baseline milestone 1.0.0
                (stages / "1.0.0.md").write_text("Milestone 1")
                return root

            def test_prepare_sprint(monkeypatch, tmp_path):
                root = _mk_repo(tmp_path)
                monkeypatch.chdir(root)
                monkeypatch.setenv("EDITOR", "true")  # no-op cmd
                cli.cli_main(["prepare-sprint", "--project_name", "demo", "--no-open"])
                assert Path(root, "1.1.0.yaml").exists()

            def test_new_milestone(monkeypatch, tmp_path):
                root = _mk_repo(tmp_path)
                monkeypatch.chdir(root)
                monkeypatch.setenv("EDITOR", "true")
                cli.cli_main(["new-milestone", "--project_name", "demo", "--no-open"])
                assert Path(root, "2.0.0.yaml").exists()
            """
        ),
        encoding="utf-8",
    )

# --------------------------------------------------------------------------- #
print(
    """
✅ Chunk 3 patch applied.

WHAT CHANGED
------------
1. Fixed patch-version logic (determine_next_version now bumps BUGFIX).
2. Added pv sub-commands:
     • pv new-milestone   – scaffolds next <N+1>.0.0.yaml
     • pv prepare-sprint  – scaffolds next sprint  <N>.<m+1>.0.yaml
   Flags:
     --project_name  override auto-detection
     --no-open       skip opening editor/viewer (handy for CI)
3. Bundled sample templates under  src/personalvibe/data/*.yaml
4. Included *.yaml in package manifest.
5. Added unit-tests covering both the bug-fix & new CLI helpers.

NEXT STEPS
----------
• Run  ./tests/personalvibe.sh   to execute full quality-gate.
• Manually try:
      pv new-milestone      # inside your repo
      pv prepare-sprint
• Review generated YAML then commit as usual.

Enjoy the smoother workflow!"""
)
