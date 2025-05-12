# Copyright © 2025 by Nick Jenkins. All rights reserved

import pytest


# Single authoritative place to declare project-wide markers.  Older
# code used the removed `pytest.register_mark`.  The hook below works
# on every modern Pytest (≥7).
def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "advanced: marks tests that hit heavier integration paths " "(deselect with '-m \"not advanced\"').",
    )
