# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Sphinx configuration."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
# -- path hack for local build

import sphinx_rtd_theme  # noqa: F401, E402

from personalvibe import __version__  # noqa: E402

project = "personalvibe"
author = "Nick Jenkins"
copyright = open(Path("..", "LICENSE")).read()
version = __version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "myst_parser",
    "sphinx_rtd_theme",
]
source_suffix = [".rst", ".md"]
html_theme = "sphinx_rtd_theme"
