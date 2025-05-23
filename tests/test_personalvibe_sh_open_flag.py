# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Static test ensuring the '--open' enhancement exists in script."""

from pathlib import Path

from personalvibe import vibe_utils


def test_open_flag_present():
    script = vibe_utils.get_base_path() / "tests/personalvibe.sh"
    txt = script.read_text(encoding="utf-8")
    assert "--open" in txt
    assert 'open "${LOG_FILE}"' in txt or 'xdg-open "${LOG_FILE}"' in txt
