# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/3.3.0.py

"""
personalvibe/chunk4_dist_smoke_patch.py
======================================

Patch “Chunk 4 – Distribution smoke”.

What it does
------------
1. Ensures Markdown templates **ship inside the wheel**
   • adds them to `pyproject.toml [tool.poetry] include`
   • guarantees `personalvibe.data` is a *proper* package
     (creates `src/personalvibe/data/__init__.py`)

2. Extends the existing **nox smoke_dist** session so that the
   built-wheel is exercised end-to-end:

      pv --help
      pv run         --config <tmp>/1.0.0.yaml --prompt_only
      pv parse-stage --project_name sampleproj

   – a minimal prompts/ folder and dummy assistant output are generated
     on-the-fly so the commands succeed without OpenAI access.

Run this patch via:

    poetry run python personalvibe/chunk4_dist_smoke_patch.py
"""

from __future__ import annotations

import re
import textwrap
from pathlib import Path


# --------------------------------------------------------------------------- helpers
def repo_root() -> Path:
    # Cheapest way – we are executed from repo; the noxfile lives at top level
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Could not locate repo root (pyproject.toml)")


ROOT = repo_root()


def touch(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(text, encoding="utf-8")


# --------------------------------------------------------------------------- 1️⃣  package data
data_init = ROOT / "src" / "personalvibe" / "data" / "__init__.py"
touch(
    data_init,
    text="# Auto-created by Chunk 4 – marks `personalvibe.data` as a real package.\n",
)

print(f"✓ ensured package file {data_init.relative_to(ROOT)}")

# ------------------- pyproject.toml  (include markdown templates) -------------
pytoml = ROOT / "pyproject.toml"
toml_src = pytoml.read_text(encoding="utf-8")
include_glob = "src/personalvibe/data/*.md"
if include_glob not in toml_src:
    # insert into the existing [tool.poetry] table´s include list
    new_src = re.sub(
        r"(\ninclude\s*=\s*\[)([^\]]*)\]",
        rf"\1\2\n    \"{include_glob}\",\n]",
        toml_src,
        count=1,
    )
    pytoml.write_text(new_src, encoding="utf-8")
    print(f"✓ added '{include_glob}' to pyproject.toml include list")
else:
    print("✓ pyproject.toml already includes template markdowns")

# --------------------------------------------------------------------------- 2️⃣  smoke_dist patch
nox_file = ROOT / "noxfile.py"
nox_src = nox_file.read_text(encoding="utf-8")

if "PERSONALVIBE CHUNK 4 PATCH START" not in nox_src:
    patch = textwrap.dedent(
        '''
        # --- PERSONALVIBE CHUNK 4 PATCH START
        from datetime import datetime
        import tempfile
        from pathlib import Path as _Path

        from nox_poetry import session as _pv_session  # reuse already-installed decorator


        @_pv_session(python=["3.12"], reuse_venv=False)  # type: ignore[misc]
        def smoke_dist(session):  # noqa: D401
            """Extended smoke-test: wheel install + core CLI commands."""
            _print_step = globals()["_print_step"]  # late-bind from module globals

            # 1) build wheel --------------------------------------------------
            _print_step("🏗️  Building wheel …")
            session.run("poetry", "build", "-f", "wheel", external=True)
            dist_dir = _Path("dist")
            wheels = sorted(dist_dir.glob("personalvibe-*.whl"))
            if not wheels:
                session.error("Wheel build failed – no file in ./dist")
            wheel = max(wheels, key=lambda p: p.stat().st_mtime)

            # 2) temp venv ----------------------------------------------------
            venv_dir = _Path(tempfile.mkdtemp(prefix="pv_smoke_"))
            _print_step(f"🧪  Creating temp venv at {venv_dir}")
            session.run("python", "-m", "venv", str(venv_dir), external=True)

            bindir = venv_dir / ("Scripts" if session.platform == "win32" else "bin")
            pip_exe = bindir / ("pip.exe" if session.platform == "win32" else "pip")
            pv_exe = bindir / ("pv.exe" if session.platform == "win32" else "pv")

            # 3) install wheel -------------------------------------------------
            _print_step("📦  Installing wheel …")
            session.run(str(pip_exe), "install", str(wheel), external=True)

            # 4) pv --help -----------------------------------------------------
            _print_step("🚀  Running `pv --help` …")
            session.run(str(pv_exe), "--help", external=True)

            # 5) prepare minimal workspace (prompts + cfg) --------------------
            repo_root = _Path.cwd()  # still the mono-repo root
            prompts_dir = repo_root / "prompts" / "sampleproj"
            prompts_dir.mkdir(parents=True, exist_ok=True)
            (prompts_dir / "prd.md").write_text(
                "# dummy template used by smoke_dist\\nHello {{ execution_task }}.",
                encoding="utf-8",
            )

            cfg_dir = repo_root / "tmp_smoke_cfg"
            cfg_dir.mkdir(exist_ok=True)
            cfg_file = cfg_dir / "1.0.0.yaml"
            cfg_file.write_text(
                textwrap.dedent(\"\"\"\
                project_name: sampleproj
                mode: milestone
                execution_details: ''
                code_context_paths: []
                \"\"\"),
                encoding="utf-8",
            )

            # 6) run pv run --prompt_only --------------------------------------
            _print_step("🎯  pv run --prompt_only …")
            session.run(
                str(pv_exe),
                "run",
                "--config",
                str(cfg_file),
                "--prompt_only",
                "--verbosity",
                "errors",
                external=True,
            )

            # 7) create dummy assistant output so parse-stage succeeds ---------
            outputs_dir = repo_root / "data" / "sampleproj" / "prompt_outputs"
            outputs_dir.mkdir(parents=True, exist_ok=True)
            dummy_path = outputs_dir / f\"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_dummyhash.md\"
            dummy_path.write_text(
                \"\"\"```python
    print('hello world')
    ```\"\"\",
                encoding="utf-8",
            )

            # 8) pv parse-stage -----------------------------------------------
            _print_step("🔎  pv parse-stage …")
            session.run(
                str(pv_exe),
                "parse-stage",
                "--project_name",
                "sampleproj",
                external=True,
            )

            _print_step("✅  smoke_dist finished without errors")
        # --- PERSONALVIBE CHUNK 4 PATCH END
        '''
    )
    nox_file.write_text(nox_src + patch, encoding="utf-8")
    print("✓ patched smoke_dist session (extended commands)")
else:
    print("✓ smoke_dist patch already present – no changes made")

# --------------------------------------------------------------------------- done
print(
    "\n🎉  Chunk 4 patch applied.\nNext step:  `nox -s smoke_dist` should "
    "build the wheel and execute the extended CLI smoke-test without errors."
)
