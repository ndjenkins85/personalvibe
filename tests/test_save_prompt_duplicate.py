# Copyright © 2025 by Nick Jenkins. All rights reserved
"""Tests for hardened prompt persistence (save_prompt)."""

from pathlib import Path

from personalvibe.vibe_utils import get_prompt_hash, save_prompt


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
