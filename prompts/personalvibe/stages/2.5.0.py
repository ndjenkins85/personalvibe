# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/2.5.0.py

#!/usr/bin/env python
"""
Chunk E – Documentation & examples

Creates the end-user on-boarding guide *docs/using_in_other_projects.md*
(with SPA placeholder) and appends a short CLI notice to
src/personalvibe/_README.md if missing.

The script is idempotent; re-runs will not duplicate content.
"""

from __future__ import annotations

import sys
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()


# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------
def _ensure_section(file: Path, header: str, body: str) -> None:
    """
    Append a Markdown section only if *header* is not present already.
    """
    text = file.read_text(encoding="utf-8") if file.exists() else ""
    if header in text:
        print(f"✓ {header.strip()} already present in {file.relative_to(REPO)}")
        return

    with file.open("a", encoding="utf-8") as fh:
        if not text.endswith("\n"):
            fh.write("\n")
        fh.write(f"{header}\n{body}\n")
        print(f"★ Added {header.strip()} to {file.relative_to(REPO)}")


# ---------------------------------------------------------------------
# 1) Main on-boarding guide
# ---------------------------------------------------------------------
docs_dir = REPO / "docs"
docs_dir.mkdir(exist_ok=True)
guide_path = docs_dir / "using_in_other_projects.md"

GUIDE_TXT = """\
# Using **Personalvibe** in *other* projects

This guide walks you through installing the published wheel, running the
CLI, and – for front-end tinkerers – the first steps towards a later
Single-Page-App (SPA) integration.

---

## Quick start (Python workflow)

# 1) Install from PyPI (recommended)
pip install personalvibe

# 2) Scaffold a data workspace somewhere **outside** the source checkout
export PV_DATA_DIR=$(pwd)/.pv_workspace     # optional, defaults to CWD

# 3) Run the milestone analysis of YOUR yaml config
pv milestone --config path/to/1.0.0.yaml --verbosity verbose

What happened?

1. The `pv` console-script parsed your YAML and resolved a *workspace*
   at `$PV_DATA_DIR` (or current directory).
2. Logs are streamed to `logs/<semver>_base.log`.
3. All prompt inputs/outputs are persisted under
   `data/<project>/prompt_*`.

---

## Environment variables

| Variable      | Purpose                                     | Default        |
|---------------|---------------------------------------------|----------------|
| `PV_DATA_DIR` | Override the workspace root directory       | `Path.cwd()`   |
| `OPENAI_API_KEY` | Passed straight through to the *OpenAI* SDK | *(required)* |

---

## Transparency reporting (example flow)

Below is an end-to-end snippet you can paste into your project’s CI:

set -e
poetry add --group dev personalvibe
pv milestone --config prompts/myproj/configs/2.0.0.yaml
pv sprint    --config prompts/myproj/configs/2.0.0.yaml --verbosity verbose
pv validate  --config prompts/myproj/configs/2.0.0.yaml

The trio ensures every step appends to the same `logs/2.0.0_base.log`,
making **audit trails** trivial.

---

## SPA placeholder 🍿

Personalvibe’s back-end is framework-agnostic, but future sprints will
expose a small JSON API.  If you already use a front-end stack, keep the
following directory layout ready:

my-project/
└─ web/
   ├─ package.json   # will list @personalvibe/sdk once published
   └─ src/
        App.tsx

Initial NPM bootstrap (React example):

cd web
npm create vite@latest  .
npm install
npm run dev

**No SDK is required yet** – this is merely a sandbox for upcoming
experiments.

---

Happy vibecoding!  — *The Personalvibe team*
"""

# Always overwrite – the file is owned entirely by this script
guide_path.write_text(GUIDE_TXT, encoding="utf-8")
print(f"📝  Wrote on-boarding guide → {guide_path.relative_to(REPO)}")

# ---------------------------------------------------------------------
# 2) Append short CLI note to the internal README (if absent)
# ---------------------------------------------------------------------
readme_internal = REPO / "src" / "personalvibe" / "_README.md"
CLI_HEADER = "## CLI usage"
CLI_BODY = """\
After installation a *console-script* named `pv` is available:

pv --help                         # global help
pv milestone --config 1.0.0.yaml  # run milestone analysis
pv sprint    --config 1.0.0.yaml  # execute a sprint
pv validate  --config 1.0.0.yaml  # lint/tests against the log file
"""

_ensure_section(readme_internal, CLI_HEADER, CLI_BODY)

# ---------------------------------------------------------------------
# 3) Developer output
# ---------------------------------------------------------------------
print(
    "\n✅  Chunk E complete.  Build the docs with:\n"
    "   nox -s docs\n"
    "or open docs/using_in_other_projects.md in your editor.\n"
)

if __name__ == "__main__":  # pragma: no cover
    pass  # All actions executed at import time
