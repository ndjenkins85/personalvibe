# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/2.4.0.py

#!/usr/bin/env python
"""
Sprint 4️⃣ Chunk D – Packaging & Smoke-test
=========================================
This patch:

1. bumps Personalvibe to **v2.0.0** in *pyproject.toml*,
2. adds a new **nox** session  `smoke_dist`
   • builds the wheel
   • installs it into an isolated temp-venv
   • executes `pv --help` to prove the console-script works,
3. adds lightweight installation docs  *docs/INSTALL.md*.

Run it once from **any** folder inside the repo:

    poetry run python patches/4d_packaging.py
    nox -s smoke_dist
"""
from __future__ import annotations

import re
import textwrap
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()

# --------------------------------------------------------------------------- #
# 1. pyproject.toml – bump version to 2.0.0
# --------------------------------------------------------------------------- #
pyproject = REPO / "pyproject.toml"
content = pyproject.read_text(encoding="utf-8")
# first occurrence only, keeps changelog history if present later
updated = re.sub(r'version\s*=\s*"[0-9]+\.[0-9]+\.[0-9]+"', 'version = "2.0.0"', content, count=1)
pyproject.write_text(updated, encoding="utf-8")

# --------------------------------------------------------------------------- #
# 2. noxfile.py – append smoke_dist session if absent
# --------------------------------------------------------------------------- #
noxfile = REPO / "noxfile.py"
nox_src = noxfile.read_text(encoding="utf-8")

if "def smoke_dist(" not in nox_src:
    smoke_session = textwrap.dedent(
        """
        @session(python=["3.12"], reuse_venv=False)
        def smoke_dist(session: Session) -> None:  # noqa: D401
            \"\"\"Build wheel, install into **fresh** temp venv, run `pv --help`.\"\"\"
            _print_step("🏗️  Building wheel …")
            session.run("poetry", "build", "-f", "wheel", external=True)

            dist_dir = Path("dist")
            wheels = sorted(dist_dir.glob("personalvibe-*.whl"))
            if not wheels:
                session.error("Wheel not found in ./dist – build failed?")
            wheel = max(wheels, key=lambda p: p.stat().st_mtime)
            _print_step(f"Wheel built: {wheel.name}")

            import tempfile, os, subprocess, sys

            venv_dir = Path(tempfile.mkdtemp(prefix="pv_smoke_"))
            _print_step(f"🧪  Creating temp venv at {venv_dir}")
            session.run("python", "-m", "venv", str(venv_dir), external=True)

            bin_dir = venv_dir / ("Scripts" if os.name == "nt" else "bin")
            pip = bin_dir / ("pip.exe" if os.name == "nt" else "pip")
            pv_exe = bin_dir / ("pv.exe" if os.name == "nt" else "pv")

            _print_step("📦  Installing wheel into temp venv …")
            session.run(str(pip), "install", str(wheel), external=True)

            _print_step("🚀  Running `pv --help` smoke test …")
            session.run(str(pv_exe), "--help", external=True)

            _print_step("✅  smoke_dist completed successfully")
        """
    ).lstrip()
    noxfile.write_text(
        f"{nox_src.rstrip()}\n\n# --- PERSONALVIBE CHUNK D PATCH START\n{smoke_session}\n# --- PERSONALVIBE CHUNK D PATCH END\n",
        encoding="utf-8",
    )

# --------------------------------------------------------------------------- #
# 3. docs/INSTALL.md – basic installation primer
# --------------------------------------------------------------------------- #
install_md = REPO / "docs" / "INSTALL.md"
install_md.parent.mkdir(parents=True, exist_ok=True)
if not install_md.exists():
    install_md.write_text(
        textwrap.dedent(
            """
            # Installation – Personalvibe 2.x

            # Grab the latest stable release
            pip install --upgrade personalvibe

            A console-script `pv` will be available afterwards:

            pv --help
            pv milestone --config path/to/1.0.0.yaml

            Runtime artefacts are created in the **current working directory**.
            Override via:

            export PV_DATA_DIR=/absolute/path/to/workspace
            """
        ).lstrip(),
        encoding="utf-8",
    )

# --------------------------------------------------------------------------- #
# 4. Guidance
# --------------------------------------------------------------------------- #
print(
    textwrap.dedent(
        """
        ✅  Chunk D applied successfully.

        • pyproject.toml bumped to 2.0.0
        • nox session `smoke_dist` added
        • docs/INSTALL.md created

        Next steps:
            nox -s smoke_dist        # wheel build & CLI smoke-test
            git add pyproject.toml noxfile.py docs/INSTALL.md
            git commit -m "feat(pkg): v2.0.0 packaging + smoke_dist session"
        """
    )
)
