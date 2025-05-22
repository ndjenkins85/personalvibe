# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/4.4.0.py

"""
patch_docs_chunk_d.py  –  Milestone 2.1.0 / Chunk D
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Refresh *user-facing* documentation (README + docs/INSTALL.md +
docs/using_in_other_projects.md) so Personalvibe reads like an
independent library – no more Storymaker / Flask references.

Run this script **once** from anywhere inside the repo:

    poetry run python patch_docs_chunk_d.py

It will
1. locate the repository root via personalvibe.vibe_utils,
2. overwrite the three markdown files with the new canonical text,
3. create docs/ONBOARDING.md (additional newcomer hints), and
4. print a short diff-hint summary.

No other files are touched.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from personalvibe import vibe_utils


# ────────────────────────────────────────────────────────────────────────────
# helpers
# ────────────────────────────────────────────────────────────────────────────
def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def main() -> None:
    repo = vibe_utils.get_base_path()

    # ╭──────────────────────────────────────────────────────────────────╮
    # │                1. Top-level README.md (PyPI view)               │
    # ╰──────────────────────────────────────────────────────────────────╯
    readme = """
    # Personalvibe

    *Brainstorm → YAML → Prompt → Code → Test*
    Personalvibe turns AI tinkering into a **repeatable pipeline**
    you can embed in *any* project.

    ```text
    pip install personalvibe        # 🚀  get the CLI
    pv run --config 1.0.0.yaml      # 🤖  generate / execute prompts
    ```

    ---
    ## Why “vibe coding” ?
    Traditional scaffolding tools expect you to know the end-state.
    But early-stage ideas are fuzzy, iterations rapid.
    Personalvibe embraces this *uncertainty*:

    • prompts live beside your source code (version controlled)
    • every run writes human-readable logs in `./logs`
    • unit tests guard each sprint so automation stays trustworthy

    ---
    ## Quick start (2 mins)

    1. `pip install personalvibe`
    2. `pv run --config examples/hello_world.yaml --prompt_only`
       → renders a prompt, saves it under `data/<project>/prompt_inputs/`
    3. fill in your OpenAI key, drop the `--prompt_only` flag, re-run.

    ---
    ## CLI overview

    | command        | purpose                                   |
    |----------------|-------------------------------------------|
    | `pv run`       | auto-detect mode from YAML & execute      |
    | `pv milestone` | ask the LLM for a milestone plan          |
    | `pv sprint`    | generate a sprint chunk (≤20 k chars)     |
    | `pv validate`  | re-run lint/tests inside a one-liner gate |
    | `pv parse-stage` | save last assistant *code* block to file|

    Append `--help` to any sub-command for details.

    ---
    ## Development setup (optional)

    ```bash
    poetry install         # installs dev + lint + test groups
    poetry run nox         # black, flake8, mypy, pytest, smoke_dist
    ./tests/personalvibe.sh   # the same quality-gate in one shell
    ```

    ---
    ## License & acknowledgements
    MIT.
    Made with ❤️  and too much coffee by Nick Jenkins.
    Inspired by dozens of open-source LLM projects — thank you!
    """

    # ╭──────────────────────────────────────────────────────────────────╮
    # │             2. docs/INSTALL.md  – end-user installation         │
    # ╰──────────────────────────────────────────────────────────────────╯
    install_md = """
    # Installation – Personalvibe 2.1

    ```bash
    pip install --upgrade personalvibe
    ```

    A console-script **`pv`** appears on your `$PATH` afterwards.

    ```bash
    pv --help
    pv run --config my_config.yaml
    ```

    Runtime artefacts are created in the **current working directory**:

    ```
    .
    ├─ data/<project>/prompt_inputs/
    ├─ data/<project>/prompt_outputs/
    └─ logs/<semver>_base.log
    ```

    Override the workspace root via:

    ```bash
    export PV_DATA_DIR=/absolute/path/to/workspace
    ```
    """

    # ╭──────────────────────────────────────────────────────────────────╮
    # │  3. docs/using_in_other_projects.md – refreshed, shortened      │
    # ╰──────────────────────────────────────────────────────────────────╯
    using_md = """
    # Using Personalvibe in *your* project

    ## 1 – Install

    ```bash
    poetry add personalvibe    # or  pip install personalvibe
    ```

    ## 2 – Create a YAML config

    ```yaml
    # 1.0.0.yaml
    project_name: my_cool_idea
    mode: milestone         # prd | milestone | sprint | validate
    execution_details: ''
    code_context_paths: []  # optional snippets fed into the prompt
    ```

    ## 3 – Run

    ```bash
    pv run --config 1.0.0.yaml --prompt_only   # preview
    pv run --config 1.0.0.yaml                 # full run
    ```

    ## Advanced

    • Persist artefacts in a separate folder:

      `PV_DATA_DIR=.pv_workspace pv sprint --config 1.0.0.yaml`

    • Extract the last assistant code block and run it:

      `pv parse-stage --project_name my_cool_idea --run`

    ---

    *Happy vibecoding!*  — The Personalvibe team
    """

    # ╭──────────────────────────────────────────────────────────────────╮
    # │                 4. New docs/ONBOARDING.md helper                │
    # ╰──────────────────────────────────────────────────────────────────╯
    onboarding = """
    # Developer on-boarding (5 minutes)

    1. **Clone** the repo and `cd` inside.
    2. `poetry install --with dev,tests,lint,docs`
    3. `pre-commit install`  (optional but recommended)
    4. Run the *full* quality-gate locally:

       ```bash
       ./tests/personalvibe.sh
       ```

    5. Create a branch `feature/<something>` and start hacking.

    Troubleshooting tips
    --------------------
    • Missing `pv` after install? → `poetry env info --path` shows the venv,
      ensure its `bin/` is on `$PATH`.

    • OpenAI key unavailable → set `OPENAI_API_KEY` or keep `--prompt_only`.

    • Questions? Open an issue or ping @ndjenkins85 on GitHub.
    """

    # ────────────────────────────────────────────────────────────────────
    # write files
    # ────────────────────────────────────────────────────────────────────
    write(repo / "README.md", readme)
    write(repo / "docs" / "INSTALL.md", install_md)
    write(repo / "docs" / "using_in_other_projects.md", using_md)
    write(repo / "docs" / "ONBOARDING.md", onboarding)

    # ────────────────────────────────────────────────────────────────────
    # user feedback
    # ────────────────────────────────────────────────────────────────────
    print("📝  Documentation patch applied:")
    for rel in (
        "README.md",
        "docs/INSTALL.md",
        "docs/using_in_other_projects.md",
        "docs/ONBOARDING.md",
    ):
        print("  •", rel)


if __name__ == "__main__":
    main()
