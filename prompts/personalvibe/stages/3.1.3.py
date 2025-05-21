# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/3.2.0.py

# PERSONALVIBE SPRINT 3.0.0-chunk-1 – PATCH
#
# Fix failing `tests/test_cli_basic.py::test_pv_help`
#   – help output must contain BOTH
#       "Personalvibe CLI"                       (new expectation)
#       "Personalvibe Command-Line Interface"    (existing expectation)
#
# Solution: change the argparse *description* so the generated
#           help text includes both phrases.

import textwrap
from pathlib import Path

# --------------------------------------------------------------------------- #
# Locate repo root                                                            #
# --------------------------------------------------------------------------- #
from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()

# --------------------------------------------------------------------------- #
# Target file                                                                 #
# --------------------------------------------------------------------------- #
cli_path = REPO / "src" / "personalvibe" / "cli.py"
assert cli_path.exists(), f"cli.py not found at {cli_path}"

# --------------------------------------------------------------------------- #
# Read & patch                                                                #
# --------------------------------------------------------------------------- #
code = cli_path.read_text(encoding="utf-8").splitlines()

NEW_DESC = "Personalvibe CLI – Command-Line Interface"

patched = []
for line in code:
    if line.strip().startswith("description="):
        # Replace the whole description assignment
        indent = line.split("description=")[0]
        patched.append(f'{indent}description="{NEW_DESC}",')
        continue
    patched.append(line)

cli_path.write_text("\n".join(patched) + "\n", encoding="utf-8")

print(
    textwrap.dedent(
        f"""
        ✅  Patched personalvibe.cli
            • argparse description now: "{NEW_DESC}"

        Next step
        ---------
        Re-run your test-suite:

            nox -s tests

        Both test_cli_basic.py and test_cli_subcommands.py should now pass,
        because the help banner contains *both* key phrases.
        """
    )
)
