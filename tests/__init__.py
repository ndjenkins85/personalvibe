# Copyright © 2025 by Nick Jenkins. All rights reserved

"""
Pytest package initialiser.

Older code called the now-removed `pytest.register_mark("advanced")`.
Project-wide markers are declared in `tests/conftest.py`, so all we
need is the import to make `tests` a package.
"""

import pytest  # noqa: F401
