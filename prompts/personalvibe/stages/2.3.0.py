# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/2.3.0.py

#!/usr/bin/env python
"""
Sprint 3️⃣ – Chunk C  •  Data-directory bootstrap
================================================

This patch
• adds *workspace-aware* bootstrap helpers to personalvibe.vibe_utils
• makes run_pipeline call the bootstrap before any IO happens
• drops a tiny migration notice when the old in-repo data folder is
  detected
• ships a new pytest file that asserts:
      – the helper builds the expected folder tree
      – duplicate prompts are not re-written

The code is fully self-contained; simply run

    poetry run nox -s tests

to execute the new suite.
"""
from __future__ import annotations

import re
import sys
import textwrap
from pathlib import Path


# --------------------------------------------------------------------------- #
# Small utility helpers
# --------------------------------------------------------------------------- #
def _repo_root() -> Path:
    """Return repository root by searching for *pyproject.toml* upwards."""
    p = Path.cwd().resolve()
    while p != p.parent:
        if (p / "pyproject.toml").is_file():
            return p
        p = p.parent
    raise RuntimeError("Repo root (pyproject.toml) not found")


def _patch_file(path: Path, new_code: str, anchor_regex: str, comment_banner: str) -> None:
    """Idempotently insert *new_code* **after** the first matching regex."""
    src = path.read_text(encoding="utf-8")
    if comment_banner in src:
        print(f"[skip] {path} already patched")
        return

    anchor_match = re.search(anchor_regex, src)
    if not anchor_match:
        raise RuntimeError(f"Anchor pattern not found in {path}")

    insert_at = anchor_match.end()
    updated = src[:insert_at] + f"\n{comment_banner}\n{new_code}\n" + src[insert_at:]
    path.write_text(updated, encoding="utf-8")
    print(f"[ok] patched {path.relative_to(_repo_root())}")


# --------------------------------------------------------------------------- #
# 1. Patch  src/personalvibe/vibe_utils.py
# --------------------------------------------------------------------------- #
VU_PATH = _repo_root() / "src/personalvibe/vibe_utils.py"

NEW_VU_CODE = textwrap.dedent(
    """
    # ----------------------------------------------------------------------
    # ✨  Data-directory bootstrap  (Chunk C)
    # ----------------------------------------------------------------------
    from typing import Dict

    def bootstrap_project_dirs(
        project_name: str,
        workspace: Union[Path, None] = None,
        *,
        ensure_prompts: bool = True,
    ) -> Dict[str, Path]:
        \"\"\"Create ``data/<project>/…`` tree inside *workspace*.

        Returns a mapping with keys ::
            {'data': Path, 'inputs': Path, 'outputs': Path}

        The function is *idempotent* and safe to call many times.

        Migration helper
        ----------------
        If the **old** in-repo storage location ``<repo>/data/<project>``
        exists and differs from the new workspace, we leave the files in
        place but emit an *UPGRADE_NOTICE.txt* beside the new workspace
        root so users are aware of the change.
        \"\"\"
        workspace = workspace or get_workspace_root()

        data_dir = get_data_dir(project_name, workspace)
        inputs_dir = data_dir / "prompt_inputs"
        outputs_dir = data_dir / "prompt_outputs"

        for d in (inputs_dir, outputs_dir):
            d.mkdir(parents=True, exist_ok=True)

        # --------- gentle migration notice (once) -------------------------
        legacy_dir = get_base_path() / "data" / project_name
        if legacy_dir.exists() and legacy_dir.resolve() != data_dir.resolve():
            notice = workspace / "UPGRADE_NOTICE.txt"
            if not notice.exists():
                notice.write_text(
                    textwrap.dedent(
                        f\"\"\"\
                        Personalvibe 2.x has moved runtime artefacts to:

                            {data_dir}

                        Your previous files remain in:

                            {legacy_dir}

                        You can delete or migrate them at your convenience.
                        \"\"\"
                    ),
                    encoding="utf-8",
                )
                log.warning("⚠️  Old data dir detected – wrote %s", notice)

        return {"data": data_dir, "inputs": inputs_dir, "outputs": outputs_dir}
    """
)

_PATCH_COMMENT = "# --- PERSONALVIBE CHUNK C PATCH ---"
ANCHOR_PATTERN = r"# ─{5,} # ✨  New workspace-root helpers  \(Chunk B\)"

_patch_file(VU_PATH, NEW_VU_CODE, ANCHOR_PATTERN, _PATCH_COMMENT)


# --------------------------------------------------------------------------- #
# 2. Patch  src/personalvibe/run_pipeline.py  (import + bootstrap call)
# --------------------------------------------------------------------------- #
RP_PATH = _repo_root() / "src/personalvibe/run_pipeline.py"
RP_SRC = RP_PATH.read_text(encoding="utf-8")
if "_BOOTSTRAP_DONE" not in RP_SRC:  # crude idempotency check
    NEW_LINE_IMPORT = "from personalvibe.vibe_utils import bootstrap_project_dirs"
    RP_SRC = RP_SRC.replace(
        "from personalvibe import logger, vibe_utils", f"from personalvibe import logger, vibe_utils\n{NEW_LINE_IMPORT}"
    )

    # inject the bootstrap immediately after workspace is resolved
    INJECT_AFTER = "workspace = vibe_utils.get_workspace_root()"
    BOOTSTRAP_CALL = "\n    # Ensure workspace/data/<project>/prompt_* exist\n    bootstrap_project_dirs(config.project_name, workspace)\n"
    RP_SRC = RP_SRC.replace(INJECT_AFTER, INJECT_AFTER + BOOTSTRAP_CALL)
    RP_PATH.write_text(RP_SRC, encoding="utf-8")
    print(f"[ok] patched {RP_PATH.relative_to(_repo_root())}")
else:
    print(f"[skip] {RP_PATH.relative_to(_repo_root())} already contains bootstrap")


# --------------------------------------------------------------------------- #
# 3. New tests  tests/test_data_bootstrap.py
# --------------------------------------------------------------------------- #
TEST_DIR = _repo_root() / "tests"
TEST_DIR.mkdir(exist_ok=True)
TEST_FILE = TEST_DIR / "test_data_bootstrap.py"
if not TEST_FILE.exists():
    TEST_FILE.write_text(
        textwrap.dedent(
            """
            # Copyright © 2025 by Nick Jenkins. All rights reserved
            \"\"\"Tests for workspace-aware data-directory bootstrap (Chunk C).\"\"\"

            import os
            from pathlib import Path

            from personalvibe.vibe_utils import bootstrap_project_dirs, save_prompt


            def test_bootstrap_creates_dirs(tmp_path, monkeypatch):
                monkeypatch.setenv("PV_DATA_DIR", str(tmp_path))
                dirs = bootstrap_project_dirs("myproj")
                assert dirs["data"].exists()
                assert dirs["inputs"].exists()
                assert dirs["outputs"].exists()


            def test_save_prompt_deduplication(tmp_path, monkeypatch):
                monkeypatch.setenv("PV_DATA_DIR", str(tmp_path))
                dirs = bootstrap_project_dirs("dup_proj")
                inputs = dirs["inputs"]

                p1 = save_prompt("hello world", inputs)
                p2 = save_prompt("hello world", inputs)
                assert p1 == p2, "Duplicate prompt should not create new file"
            """
        ),
        encoding="utf-8",
    )
    print(f"[ok] created {TEST_FILE.relative_to(_repo_root())}")
else:
    print(f"[skip] {TEST_FILE.relative_to(_repo_root())} exists")


# --------------------------------------------------------------------------- #
# 4. Done – friendly message
# --------------------------------------------------------------------------- #
print(
    textwrap.dedent(
        """
        ✅  Chunk C patch applied.
        • Run `poetry run nox -s tests` to execute the new suite.
        • Set PV_DATA_DIR to steer runtime artefacts when using the CLI.

        """
    )
)
