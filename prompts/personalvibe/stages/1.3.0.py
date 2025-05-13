# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/1.3.0.py
#!/usr/bin/env python
"""
patch_prompt_persistence.py  – Sprint-3 “Prompt persistence hardening”

Run via:  poetry run python patch_prompt_persistence.py
--------------------------------------------------------------------
• Refactors personalvibe.vibe_utils.save_prompt  ➜  returns Path,
  always terminates file with “### END PROMPT”.
• Hardens duplicate-hash behaviour & updates get_vibed accordingly.
• Adds unit-tests for duplicate detection + END-marker.
• Appends hashing strategy docs to _README.md.

The script is *idempotent*: safe to re-run; it patches files only once.
"""
from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path
from textwrap import dedent

from personalvibe import vibe_utils
from personalvibe.vibe_utils import get_base_path

REPO = get_base_path()
SRC = REPO / "src" / "personalvibe"
TESTS = REPO / "tests"

# ──────────────────────────────────────────────────────────────────────────
# 1. Patch vibe_utils.py
# ──────────────────────────────────────────────────────────────────────────
vu_path = SRC / "vibe_utils.py"
vu_code = vu_path.read_text(encoding="utf-8")

# ---- 1.1 Replace `save_prompt` ------------------------------------------------
new_save_prompt = dedent(
    '''
    def save_prompt(prompt: str, root_dir: Path, input_hash: str = "") -> Path:
        """Persist *one* prompt to disk and return its Path.

        Behaviour
        ----------
        • Uses SHA-256(prompt)[:10] to create a stable short-hash.
        • If a file containing that hash already exists, nothing is written
          and the *existing* Path is returned.
        • New files are named   <timestamp>[_<input_hash>]_ <hash>.md
        • Every file is terminated with an extra line::

              ### END PROMPT

          to make `grep -A999 '^### END PROMPT$'` trivially reliable.
        """
        # Timestamp + hash bits
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        hash_str = get_prompt_hash(prompt)[:10]

        if existing := find_existing_hash(root_dir, hash_str):
            log.info("Duplicate prompt detected. Existing file: %s", existing)
            return existing

        # Compose filename
        if input_hash:
            filename = f"{timestamp}_{input_hash}_{hash_str}.md"
        else:
            filename = f"{timestamp}_{hash_str}.md"
        filepath = Path(root_dir) / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        # Write prompt + END-marker
        filepath.write_text(f"{prompt}\n### END PROMPT\n", encoding="utf-8")
        log.info("Prompt saved to: %s", filepath)
        return filepath
    '''
).strip("\n")

pattern_save = re.compile(
    r"def save_prompt\([^\n]*\n(?:[^\n]*\n)+?^\s*def get_vibed",
    flags=re.MULTILINE,
)
# Ensure we still have the original text
if not pattern_save.search(vu_code):
    print("‼️  Could not locate original save_prompt() definition – aborting.", file=sys.stderr)
    sys.exit(1)

vu_code = pattern_save.sub(new_save_prompt + "\n\ndef get_vibed", vu_code, count=1)

# ---- 1.2  Update first call-site in get_vibed -------------------------------
vu_code = re.sub(
    r"input_hash\s*=\s*save_prompt\(\s*prompt\s*,\s*base_input_path\s*\)",
    ("prompt_file = save_prompt(prompt, base_input_path)\n" "    input_hash = prompt_file.stem.split('_')[-1]"),
    vu_code,
)

# ---- 1.3  Return type update for find_existing_hash --------------------------
vu_code = re.sub(
    r"def find_existing_hash\([^\n]+\):",
    "def find_existing_hash(root_dir: str | Path, hash_str: str) -> Path | None:",
    vu_code,
)
vu_code = re.sub(
    r"return os\.path\.join\(dirpath, filename\)",
    "return Path(dirpath) / filename",
    vu_code,
)

vu_path.write_text(vu_code, encoding="utf-8")
print(f"✅ Patched {vu_path.relative_to(REPO)}")

# ──────────────────────────────────────────────────────────────────────────
# 2. Add duplicate-hash unit-test
# ──────────────────────────────────────────────────────────────────────────
test_code = dedent(
    """
    # Copyright © 2025 by Nick Jenkins. All rights reserved
    \"\"\"Tests for hardened prompt persistence (save_prompt).\"\"\"

    from pathlib import Path

    from personalvibe.vibe_utils import save_prompt, get_prompt_hash

    def test_save_prompt_duplicate(tmp_path: Path):
        prompt = "Hello duplicate world!"
        root = tmp_path / "prompts"
        p1 = save_prompt(prompt, root)
        assert p1.exists()
        # Second save should *not* create a new file
        p2 = save_prompt(prompt, root)
        assert p1 == p2, "Duplicate hash should return same file"
        # Directory should contain exactly one file
        files = list(root.rglob("*.md"))
        assert len(files) == 1
        # Ensure END-marker present
        content = p1.read_text(encoding="utf-8").splitlines()
        assert content[-1] == "### END PROMPT"
    """
).lstrip()

dup_test_path = TESTS / "test_save_prompt_duplicate.py"
if not dup_test_path.exists():
    dup_test_path.write_text(test_code, encoding="utf-8")
    print(f"✅ Added {dup_test_path.relative_to(REPO)}")
else:
    print("ℹ️  duplicate test already exists – skipped.")

# ──────────────────────────────────────────────────────────────────────────
# 3. Append README hashing strategy
# ──────────────────────────────────────────────────────────────────────────
readme_path = SRC / "_README.md"
append_text = dedent(
    """
    ## Prompt persistence & hashing

    Every prompt (input *and* LLM output) is written to
    `data/<project>/prompt_[in|out]puts` with a filename that embeds:

    1. A timestamp – human searchable
    2. An optional upstream *input* hash (so output files can be paired)
    3. The first 10 chars of **SHA-256(prompt)** – collision-safe ID

    The helper `personalvibe.vibe_utils.save_prompt()` de-duplicates using the
    hash so re-runs never flood the directory; it simply returns the existing
    `Path` when a match is found.  Each file is suffixed with

    ```text
    ### END PROMPT
    ```

    which makes shell/grep extraction of individual prompts trivial.
    """
).strip("\n")

if "## Prompt persistence & hashing" not in readme_path.read_text(encoding="utf-8"):
    with readme_path.open("a", encoding="utf-8") as fh:
        fh.write("\n\n" + append_text + "\n")
    print(f"✅ Appended hashing docs to {readme_path.relative_to(REPO)}")
else:
    print("ℹ️  README already documents hashing – skipped.")

# ──────────────────────────────────────────────────────────────────────────
# 4. Done – guidance
# ──────────────────────────────────────────────────────────────────────────
print(
    "\n🌟  Sprint-3 patch complete.\n"
    "   • Run `nox -s tests` to execute the new duplicate-hash test.\n"
    "   • All prompt files will now end with '### END PROMPT'.\n"
)
