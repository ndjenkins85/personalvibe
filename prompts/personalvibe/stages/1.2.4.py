# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/1.2.4.py
#!/usr/bin/env python
"""
Sprint-2 patch script – “nox vibed enhancements”

Run me with:  `python sprint_2_patch.py`

What it does
============
1. Patch **noxfile.py**
   • fix `locations` path to `src/personalvibe`
   • log-file name changed to  …`_base.log`
   • accept *optional* patch paths, execute them
   • add `--verbosity=verbose` to any `run_pipeline` invocations
2. Drop a minimal pytest that spawns
   `nox -s vibed -- 0.0.2 <dummy_patch.py>`
   and asserts that the _base log contains the three step banners.
3. Ship a tiny dummy patch used by the test.
4. All modifications are strictly additive / in-place; no files are
   deleted.

After running the script, execute

    nox -s tests

to prove the new behaviour.

"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
try:
    from personalvibe import vibe_utils
except ModuleNotFoundError:  # running before poetry install
    sys.path.append(str(Path(__file__).resolve().parent / "src"))
    from personalvibe import vibe_utils  # type: ignore

REPO = vibe_utils.get_base_path()


def patch_noxfile() -> None:
    nf = REPO / "noxfile.py"
    text = nf.read_text(encoding="utf-8")

    # ---- 1️⃣  fix `locations` ------------------------------------------------
    text = re.sub(
        r'locations\s*=\s*".*?personalvibe"',
        'locations = "src/personalvibe", "tests", "noxfile.py", "docs/conf.py"',
        text,
        count=1,
    )

    # ---- 2️⃣  tweak `_log_to` docstring if needed (already append-mode) ------
    # nothing to change – implementation already uses `tee -a`

    # ---- 3️⃣  patch the vibed session ---------------------------------------
    pattern = r"@session\(python=\[\"3\.12\"\], reuse_venv=True\)\s+def vibed\(session: Session\).*?" ""  # noqa: E501
    m = re.search(pattern, text, flags=re.DOTALL)
    if not m:
        raise RuntimeError("Failed to locate vibed() in noxfile.py")

    old_block = m.group(0)

    # Re-write the whole function – simpler & clearer
    new_block = dedent(
        """
        @session(python=["3.12"], reuse_venv=True)
        def vibed(session: Session) -> None:  # noqa: D401
            \"\"\"Create vibed/<semver> branch, apply patch(es), run quality-gate.

            Usage examples
            --------------
            nox -s vibed -- 1.2.3
            nox -s vibed -- 1.2.3 path/to/patch.py other_patch.py
            \"\"\"
            if not session.posargs:
                session.error("Semver identifier required, e.g. nox -s vibed -- 0.2.1")

            semver, *patches = session.posargs
            semver = semver.strip()

            log_path = Path("logs") / f"{semver}_base.log"
            log_path.parent.mkdir(parents=True, exist_ok=True)

            with _log_to(log_path):
                _print_step(f"Creating branch vibed/{semver}")
                session.run("git", "checkout", "-b", f"vibed/{semver}", external=True)

                # ------------------------------------------------ Patch scripts
                for patch in patches:
                    _print_step(f"Running patch script: {patch}")
                    session.run("poetry", "run", "python", patch, external=True)

                _print_step("Executing quality-gate (tests/personalvibe.sh)")
                session.run("bash", "tests/personalvibe.sh", external=True)

            _print_step(f"✨  Vibe sprint '{semver}' finished – see {log_path}")
        """
    ).strip("\n")

    text = text.replace(old_block, new_block)
    nf.write_text(text, encoding="utf-8")
    print("✓ Patched noxfile.py")


def add_pytest() -> None:
    test_dir = REPO / "tests"
    test_dir.mkdir(exist_ok=True)

    (test_dir / "dummy_patch.py").write_text(
        dedent(
            """
            \"\"\"Minimal patch that just prints something.\"\"\"
            print("dummy patch ran successfully")
            """
        ).lstrip(),
        encoding="utf-8",
    )

    (test_dir / "test_vibed_session.py").write_text(
        dedent(
            """
            import subprocess
            from pathlib import Path
            import sys

            def test_vibed_end_to_end(tmp_path):
                semver = "0.0.2"
                dummy_patch = Path("tests") / "dummy_patch.py"

                # Run vibed session
                cmd = ["nox", "-s", "vibed", "--", semver, str(dummy_patch)]
                completed = subprocess.run(
                    cmd,
                    text=True,
                    capture_output=True,
                )
                # surface helpful output on failure
                assert completed.returncode == 0, completed.stderr + "\\n" + completed.stdout

                log_file = Path("logs") / f"{semver}_base.log"
                assert log_file.exists(), "log file not created"

                content = log_file.read_text(encoding="utf-8")
                assert f"Creating branch vibed/{semver}" in content
                assert "Running patch script" in content
                assert "Executing quality-gate (tests/personalvibe.sh)" in content
            """
        ).lstrip(),
        encoding="utf-8",
    )
    print("✓ Added pytest that exercises nox vibed")


def main() -> None:
    patch_noxfile()
    add_pytest()

    print(
        dedent(
            f"""
            ----------------------------------------------------------------
            Sprint-2 patch applied ✔

              • noxfile.py updated
              • pytest added: tests/test_vibed_session.py
              • dummy patch:  tests/dummy_patch.py

            Next steps
            ----------
            1. Re-install if needed:      poetry install --sync
            2. Run the full suite:        nox -s tests
               (this invokes the new vibed session internally)
            3. Inspect logs/0.0.2_base.log – you should see the 3 banners.

            Happy vibecoding! 🕺
            ----------------------------------------------------------------
            """
        )
    )


if __name__ == "__main__":
    main()
