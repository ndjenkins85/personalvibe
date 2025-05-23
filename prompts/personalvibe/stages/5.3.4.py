# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/5.3.4.py

#!/usr/bin/env python
"""
patch_chunk_5.py  –  Personalvibe “Documentation Directory & Release Prep”

Idempotent script that:
1. Bumps project version → 3.0.0-alpha0 (pyproject.toml + __init__.py)
2. Adds hub-style TOC to README.md (once)
3. Creates roadmap file docs/roadmap/3.0.0_milestone.md
4. Extends docs/index.rst to reference roadmap
5. Ensures docs/conf.py can `import personalvibe` when built from repo
6. Creates / updates top-level CHANGELOG.md
"""

from __future__ import annotations

import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()
print(f"[chunk-5]  repo root  → {REPO}")


# -----------------------------------------------------------------------------
# helpers
def _replace_version(path: Path, pattern: str, new_version: str) -> None:
    txt = path.read_text(encoding="utf-8")
    if new_version in txt:
        return
    new, n = re.subn(pattern, rf'\g<1>"{new_version}"', txt, count=1, flags=re.M)
    if n == 0:  # pragma: no cover
        print(f"[WARN] pattern not found in {path}")
        return
    path.write_text(new, encoding="utf-8")
    print(f"  • bumped version in {path.relative_to(REPO)}")


def _ensure_line_in_file(path: Path, marker: str, payload: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
        print(f"  • created {path.relative_to(REPO)}")
        return
    txt = path.read_text(encoding="utf-8")
    if marker in txt:
        return
    path.write_text(txt.rstrip() + "\n\n" + payload, encoding="utf-8")
    print(f"  • appended payload to {path.relative_to(REPO)}")


# -----------------------------------------------------------------------------
# 1) bump versions ------------------------------------------------------------
NEW_VERSION = "3.0.0-alpha0"
_replace_version(
    REPO / "pyproject.toml",
    r'(?m)^(version\s*=\s*)"[^"]+"',
    NEW_VERSION,
)
_replace_version(
    REPO / "src" / "personalvibe" / "__init__.py",
    r'(?m)^(__version__\s*=\s*)".+"',
    NEW_VERSION,
)

# -----------------------------------------------------------------------------
# 2) README hub TOC -----------------------------------------------------------
readme = REPO / "README.md"
hub_header = "## Documentation quick links"
if readme.exists():
    txt = readme.read_text(encoding="utf-8")
    if hub_header not in txt:
        toc = f"""{hub_header}

* [Installation](docs/INSTALL.md)
* [Developer on-boarding](docs/ONBOARDING.md)
* [Using Personalvibe *in other projects*](docs/using_in_other_projects.md)
* [API reference](docs/reference.rst)
* [Roadmap 3.0.0](docs/roadmap/3.0.0_milestone.md)

---
"""
        # insert after top-level title (# Personalvibe)
        new = re.sub(r"(# Personalvibe\s*)", r"\1\n" + toc + "\n", txt, count=1, flags=re.I)
        readme.write_text(new, encoding="utf-8")
        print("  • injected hub-style TOC into README.md")

# -----------------------------------------------------------------------------
# 3) roadmap doc --------------------------------------------------------------
roadmap_dir = REPO / "docs" / "roadmap"
roadmap_dir.mkdir(parents=True, exist_ok=True)
roadmap_file = roadmap_dir / "3.0.0_milestone.md"
if not roadmap_file.exists():
    roadmap_contents = f"""# Personalvibe 3.0.0 Milestone

Date: {datetime.utcnow().date().isoformat()}

This document summarises the five work chunks that constitute the
3.0.0 release.

| Chunk | Title                                    | Status |
|-------|------------------------------------------|--------|
| 1     | Lint-Zero & Code-Cull                    | ✅ done |
| 2     | Implicit Project Detection               | ✅ done |
| 3     | New-Milestone & Prepare-Sprint Commands  | ✅ done |
| 4     | IO & UX Hardening                        | ✅ done |
| 5     | Documentation Directory & Release Prep   | **this patch** |

Highlights
----------

* Flake8 clean slate, dead code removed – devs work noise-free.
* `detect_project_name()` removes the most tedious CLI arg.
* `pv new-milestone` & `pv prepare-sprint` scaffold YAMLs in one shot.
* YAML sanitiser + `--open` flag protect users from invisible data issues.
* Docs now point newcomers straight to install, onboarding & reference.
"""
    roadmap_file.write_text(roadmap_contents, encoding="utf-8")
    print(f"  • created roadmap page {roadmap_file.relative_to(REPO)}")

# -----------------------------------------------------------------------------
# 4) docs/index.rst  – add roadmap to hidden toctree --------------------------
index_rst = REPO / "docs" / "index.rst"
if index_rst.exists():
    rst_txt = index_rst.read_text(encoding="utf-8")
    roadmap_entry = "   roadmap/3.0.0_milestone"
    if roadmap_entry not in rst_txt:
        rst_new = rst_txt.replace(":maxdepth: 1", ":maxdepth: 1\n\n" + roadmap_entry)
        index_rst.write_text(rst_new, encoding="utf-8")
        print("  • roadmap added to docs/index.rst toctree")

# -----------------------------------------------------------------------------
# 5) docs/conf.py  – ensure src import path included --------------------------
conf_py = REPO / "docs" / "conf.py"
if conf_py.exists():
    conf_txt = conf_py.read_text(encoding="utf-8")
    sentinel = "# -- path hack for local build"
    if sentinel not in conf_txt:
        insertion = """
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
# -- path hack for local build
"""
        conf_txt = conf_txt.replace("from pathlib import Path", "from pathlib import Path" + insertion)
        conf_py.write_text(conf_txt, encoding="utf-8")
        print("  • injected src/ path append into docs/conf.py")

# -----------------------------------------------------------------------------
# 6) CHANGELOG.md -------------------------------------------------------------
changelog = REPO / "CHANGELOG.md"
entry_title = f"## 3.0.0-alpha0 – {datetime.utcnow().date().isoformat()}"
ch_body = f"""
{entry_title}

* Documentation hub added to README
* New `docs/roadmap/3.0.0_milestone.md`
* Sphinx config tweaks so `make html` works from source checkout
* Project version bumped to `3.0.0-alpha0`
"""
if changelog.exists():
    if entry_title not in changelog.read_text(encoding="utf-8"):
        _ensure_line_in_file(changelog, entry_title, ch_body.strip())
else:
    changelog.write_text("# Changelog\n\n" + ch_body.strip(), encoding="utf-8")
    print("  • created CHANGELOG.md")

# -----------------------------------------------------------------------------
print(
    """
✅  Chunk-5 patch applied.

Next steps
----------
1. Run  `poetry run nox -s docs`  to build HTML docs – they should now include
   the roadmap and load Personalvibe modules without import errors.
2. Run  `tests/personalvibe.sh`  to ensure the full quality-gate still passes.
3. If all green, merge & tag `v3.0.0-alpha0`; a release-candidate wheel will
   be published by CI, and docs hosted via GitHub Pages auto-update.

"""
)
