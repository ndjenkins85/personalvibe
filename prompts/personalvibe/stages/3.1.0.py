# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/3.1.0.py

# sprint_3.0.0_chunk_1_cli_foundations_patch.py
"""
CLI foundations – patch 1
Fixes:
• `pv run` now accepts the same common flags as other sub-commands
  (e.g.  pv run --config cfg.yaml --prompt_only)
Adds:
• tiny smoke-tests for all sub-commands to guard against “unknown
  argument” regressions.

Run via:
    poetry run python sprint_3.0.0_chunk_1_cli_foundations_patch.py
"""

from __future__ import annotations

import inspect
import sys
from pathlib import Path
from textwrap import dedent


# --------------------------------------------------------------------------- helpers
def repo_root() -> Path:
    from personalvibe import vibe_utils

    return vibe_utils.get_base_path()  # type: ignore[attr-defined]


def patch_file(path: Path, new_text: str) -> None:
    if not path.exists():
        raise FileNotFoundError(path)
    path.write_text(new_text, encoding="utf-8")
    print(f"📝  Patched: {path.relative_to(repo_root())}")


def append_file(path: Path, new_text: str) -> None:
    path.write_text(path.read_text(encoding="utf-8") + new_text, encoding="utf-8")
    print(f"➕  Appended: {path.relative_to(repo_root())}")


# --------------------------------------------------------------------------- 1) CLI fix
cli_path = repo_root() / "src/personalvibe/cli.py"
original = cli_path.read_text(encoding="utf-8")

# Inject `_common(run_sp)` right after creation of `run_sp`
patched = original.replace(
    'run_sp = sub.add_parser("run", help="Determine mode from YAML then execute.")',
    'run_sp = sub.add_parser("run", help="Determine mode from YAML then execute.")\n    _common(run_sp)',
)

if original == patched:
    print("✅  cli.py already contains common args for 'run' – nothing to patch.")
else:
    patch_file(cli_path, patched)

# --------------------------------------------------------------------------- 2) New tests
tests_dir = repo_root() / "tests"
tests_dir.mkdir(exist_ok=True)

test_cli_sub = tests_dir / "test_cli_subcommands.py"
if not test_cli_sub.exists():
    test_cli_sub.write_text(
        dedent(
            """
            # Copyright © 2025 by Nick Jenkins
            \"\"\"Argument-parsing smoke tests for every pv sub-command.\"\"\"

            import importlib
            import sys

            import pytest
            from personalvibe import cli as pv_cli


            @pytest.mark.parametrize(
                "argv",
                [
                    ["run", "--config", "dummy.yaml"],
                    ["run", "--config", "dummy.yaml", "--prompt_only"],
                    ["milestone", "--config", "dummy.yaml"],
                    ["sprint", "--config", "dummy.yaml", "--verbosity", "verbose"],
                    ["validate", "--config", "dummy.yaml", "--max_retries", "9"],
                    ["parse-stage", "--project_name", "personalvibe"],
                ],
            )
            def test_cli_arg_matrix(argv):
                parser = pv_cli._build_parser()
                # Argparse exits with SystemExit on failure – we intercept that
                try:
                    parser.parse_args(argv)
                except SystemExit as e:  # pragma: no cover
                    pytest.fail(f"Argparse raised SystemExit ({e.code}) for argv={argv}")
            """
        ),
        encoding="utf-8",
    )
    print(f"🆕  Added: {test_cli_sub.relative_to(repo_root())}")
else:
    print("✅  tests/test_cli_subcommands.py already exists – left untouched.")

# --------------------------------------------------------------------------- 3) Developer hint
print(
    dedent(
        """
        Patch applied.

        Next steps
        ----------
        1.  Run `pytest -q` – the new tests should pass alongside existing ones.
        2.  Manually verify the CLI:

                pv run --config path/to/2.0.0.yaml --prompt_only
                pv milestone --config path/to/2.0.0.yaml
                pv parse-stage --project_name personalvibe

            All commands must show *no* “unrecognised arguments” errors.
        3.  Commit + continue with the remaining milestone chunks.
        """
    )
)
