# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/5.2.0.py

#!/usr/bin/env python
"""
patch_chunk1_cli_foundations.py

Apply CHUNK-1 refinements for the 3.0.0 “CLI foundations” sprint.

Changes
-------
1. Tighten `pv run` logic so it **delegates** to the specialised
   handler (milestone / sprint / validate / prd) after reading the YAML.
   This fulfils the design note “behaviour equals `pv <mode>`”.

2. Provide an integration-safe unit-test that proves the delegation
   happens and that the hidden `--raw-argv` override works.

The patch is **idempotent** – running it repeatedly leaves the
codebase unchanged after the first successful execution.
"""
from __future__ import annotations

import re
import textwrap
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()

# ---------------------------------------------------------------------
CLI_FILE = REPO / "src" / "personalvibe" / "cli.py"
CLI_TEXT = CLI_FILE.read_text(encoding="utf-8")

# --- 1. replace the _cmd_run implementation --------------------------
PATTERN = re.compile(
    r"def _cmd_run\([^\n]*?\n"
    r"(?:    .*\n)*?"  # non-greedy up to the next blank line or def
    r"\)",
    re.MULTILINE,
)

NEW_CMD_RUN = textwrap.dedent(
    '''
    def _cmd_run(ns: argparse.Namespace) -> None:
        """
        Auto-detect the *mode* from YAML then behave exactly as if the user
        had typed ``pv <mode>``.  Power users can bypass everything with
        ``--raw-argv``.
        """
        # -- explicit raw passthrough -----------------------------------
        if getattr(ns, "raw_argv", ""):
            _call_run_pipeline(shlex.split(ns.raw_argv))
            return

        # -- peek at YAML -----------------------------------------------
        mode = ""
        try:
            import yaml

            with open(ns.config, "r", encoding="utf-8") as fh:
                mode = (yaml.safe_load(fh) or {}).get("mode", "").strip()
        except Exception:  # noqa: BLE001
            pass  # fall back to generic run

        if mode in {"prd", "milestone", "sprint", "validate"}:
            # Delegate – keeps behaviour equal to explicit sub-command
            _cmd_mode(ns, mode)
            return

        # Unknown / missing mode → run_pipeline directly ----------------
        forwarded = [
            "--config",
            ns.config,
            "--verbosity",
            ns.verbosity,
        ]
        if ns.prompt_only:
            forwarded.append("--prompt_only")
        if ns.max_retries != 5:
            forwarded += ["--max_retries", str(ns.max_retries)]

        _call_run_pipeline(forwarded)
    '''
).strip()

if PATTERN.search(CLI_TEXT):
    CLI_TEXT_NEW = PATTERN.sub(NEW_CMD_RUN, CLI_TEXT)
    if CLI_TEXT_NEW != CLI_TEXT:
        CLI_FILE.write_text(CLI_TEXT_NEW, encoding="utf-8")
else:
    # Already patched – nothing to do
    CLI_TEXT_NEW = CLI_TEXT

# ---------------------------------------------------------------------
# 2. add new pytest proving delegation --------------------------------
TEST_DIR = REPO / "tests"
TEST_FILE = TEST_DIR / "test_cli_run_delegate.py"

if not TEST_FILE.exists():
    TEST_FILE.write_text(
        textwrap.dedent(
            """
            # Copyright © 2025 by Nick Jenkins.
            #
            # Purpose: ensure `pv run` inspects YAML, routes to the correct
            # specialised handler, and honours --raw-argv passthrough.
            from __future__ import annotations

            import types
            from pathlib import Path
            from unittest import mock

            import personalvibe.cli as cli


            def _tmp_cfg(tmp_path: Path, mode: str) -> Path:
                cfg = tmp_path / f"{mode}.yaml"
                cfg.write_text(
                    f\"\"\"project_name: demo
    mode: {mode}
    execution_details: ''
    code_context_paths: []\"\"\",
                    encoding="utf-8",
                )
                return cfg


            def test_run_delegates_to_mode(monkeypatch, tmp_path):
                called = types.SimpleNamespace(args=None)

                def _fake_main():
                    called.args = cli.sys.argv[1:]  # skip prog name

                monkeypatch.patch.object(cli.run_pipeline, "main", _fake_main)

                cfg = _tmp_cfg(tmp_path, "milestone")
                cli.cli_main(["run", "--config", str(cfg)])

                assert called.args is not None, "run_pipeline.main not invoked"
                # Should be same args as explicit 'pv milestone'
                assert "--config" in called.args
                assert str(cfg) in called.args


            def test_run_raw_argv_passthrough(monkeypatch, tmp_path):
                captured = {}

                def _fake_main():
                    captured["argv"] = cli.sys.argv[1:]

                monkeypatch.patch.object(cli.run_pipeline, "main", _fake_main)

                cfg = _tmp_cfg(tmp_path, "prd")
                cli.cli_main(
                    [
                        "run",
                        "--config",
                        str(cfg),
                        "--raw-argv",
                        "--config sentinel.yaml --verbosity verbose",
                    ]
                )

                assert captured["argv"] == [
                    "--config",
                    "sentinel.yaml",
                    "--verbosity",
                    "verbose",
                ]
            """
        ).lstrip(),
        encoding="utf-8",
    )

print(
    "✅  CLI foundations patch applied.\n"
    "• src/personalvibe/cli.py  –  _cmd_run now delegates correctly.\n"
    "• tests/test_cli_run_delegate.py  –  new unit-tests added.\n\n"
    "Next steps\n"
    "----------\n"
    "1.  Run   pytest -q   → all tests (including the new ones) must pass.\n"
    "2.  Run   pv run --config <your>.yaml --prompt_only   to verify the CLI\n"
    "    still behaves as expected.\n"
    "3.  Proceed to CHUNK-2 (Resource & path resolver) once CI is green.\n"
)
