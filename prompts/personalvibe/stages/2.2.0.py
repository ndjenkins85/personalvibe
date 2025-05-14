# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/2.2.0.py

#!/usr/bin/env python
"""
Sprint 1 – Chunk A  |  Schema v2 scaffolding patch

This executable script:
• updates `src/personalvibe/run_pipeline.py` with the new Pydantic model
  (adds `conversation_history`, removes *required* `milestone_file_name`,
  ignores unknown legacy keys),
• ships a sample config `prompts/personalvibe/configs/1.2.0.yaml`,
• introduces a focused pytest module `tests/test_config_schema_v2.py`
  that exercises the new schema and legacy-compat behaviour.

Run this file once, then execute:

    nox -s tests        # or  simply  pytest -q

to verify that the whole suite—including the fresh tests—passes.
"""
from __future__ import annotations

import re
import sys
import textwrap
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _rel(path: Path) -> str:
    return str(path.relative_to(REPO))


def _write(path: Path, data: str, *, exist_ok: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not exist_ok:
        raise FileExistsError(f"{path} already exists")
    path.write_text(data, encoding="utf-8")
    print(f"✓ wrote {_rel(path)}")


# --------------------------------------------------------------------------- #
# 1. Patch `run_pipeline.py`  (ConfigModel v2)
# --------------------------------------------------------------------------- #
def patch_run_pipeline() -> None:
    target = REPO / "src" / "personalvibe" / "run_pipeline.py"
    code = target.read_text(encoding="utf-8")

    new_class_def = textwrap.dedent(
        """
        class ConfigModel(BaseModel):
            \"\"\"Schema **v2**

            • adds optional ``conversation_history`` (list of {role, content})
            • drops *required* ``milestone_file_name`` (legacy keys tolerated)
            \"\"\"

            version: str
            project_name: str
            mode: str = Field(..., pattern="^(prd|milestone|sprint|validate)$")
            execution_task: Optional[str] = None
            execution_details: str = ""
            code_context_paths: List[str]
            # ---- NEW --------------------------------------------------------
            conversation_history: Optional[List[dict[str, str]]] = None
            # ---- still used by validate flow --------------------------------
            error_file_name: str = ""

            class Config:
                extra = "ignore"  # silently discard unknown legacy fields
        """
    ).strip()

    # naïve but reliable: replace the entire previous class block
    pattern = re.compile(
        r"class ConfigModel\(BaseModel\):.*?^def load_config",
        re.DOTALL | re.MULTILINE,
    )
    if not pattern.search(code):
        print("ERROR: could not locate existing ConfigModel definition", file=sys.stderr)
        sys.exit(1)

    code = pattern.sub(f"{new_class_def}\n\ndef load_config", code, count=1)
    target.write_text(code, encoding="utf-8")
    print(f"✓ patched {_rel(target)}")


# --------------------------------------------------------------------------- #
# 2. Add sample YAML config (1.2.0)
# --------------------------------------------------------------------------- #
def add_sample_yaml() -> None:
    sample_cfg = textwrap.dedent(
        """\
        # python -m personalvibe.run_pipeline --config prompts/personalvibe/configs/1.2.0.yaml

        project_name: "personalvibe"
        mode: milestone
        execution_details: |
          Demonstration of schema v2 (conversation_history enabled).

        code_context_paths:
          - "prompts/personalvibe/context/codefiles.txt"

        conversation_history:
          - role: user
            content: "Hi personalvibe — what’s next?"
          - role: assistant
            content: "We should upgrade the schema to v2!"
        """
    )
    dst = REPO / "prompts" / "personalvibe" / "configs" / "1.2.0.yaml"
    _write(dst, sample_cfg, exist_ok=True)


# --------------------------------------------------------------------------- #
# 3. New pytest module for schema validation
# --------------------------------------------------------------------------- #
def add_tests() -> None:
    test_code = textwrap.dedent(
        '''
        """Schema v2 tests – conversation_history + legacy compatibility."""
        from pathlib import Path

        from pydantic import ValidationError
        from personalvibe.run_pipeline import load_config, ConfigModel


        def _tmp_cfg(tmp_path: Path, yaml_txt: str) -> Path:
            p = tmp_path / "cfg.yaml"
            p.write_text(yaml_txt, encoding="utf-8")
            return p


        def test_valid_history(tmp_path: Path):
            yaml_txt = """
            project_name: personalvibe
            mode: milestone
            execution_details: ""
            code_context_paths: []
            conversation_history:
              - role: user
                content: hi
              - role: assistant
                content: hello
            """
            cfg = load_config(str(_tmp_cfg(tmp_path, yaml_txt)))
            assert isinstance(cfg, ConfigModel)
            assert cfg.conversation_history[0]["role"] == "user"


        def test_history_optional(tmp_path: Path):
            yaml_txt = """
            project_name: personalvibe
            mode: prd
            execution_details: ""
            code_context_paths: []
            """
            cfg = load_config(str(_tmp_cfg(tmp_path, yaml_txt)))
            assert cfg.conversation_history is None


        def test_legacy_milestone_file_name_ignored(tmp_path: Path):
            yaml_txt = """
            project_name: personalvibe
            mode: sprint
            execution_details: ""
            code_context_paths: []
            milestone_file_name: legacy.txt  # obsolete
            """
            cfg = load_config(str(_tmp_cfg(tmp_path, yaml_txt)))
            assert not hasattr(cfg, "milestone_file_name")
        '''
    ).lstrip()
    dst = REPO / "tests" / "test_config_schema_v2.py"
    _write(dst, test_code, exist_ok=True)


# --------------------------------------------------------------------------- #
# Entrypoint
# --------------------------------------------------------------------------- #
def main() -> None:
    patch_run_pipeline()
    add_sample_yaml()
    add_tests()

    print(
        "\n➡  Schema v2 patch applied.\n"
        "   • run `nox -s tests` (or `pytest -q`) to ensure all suites pass.\n"
        "   • once green, proceed to Chunk B – Pipeline & Utils Wiring."
    )


if __name__ == "__main__":
    main()
