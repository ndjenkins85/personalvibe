#!/usr/bin/env bash
# tests/personalvibe.sh
#
# One script to rule them all: lint, type-check & run pytest in the
# *same* environment every time this sprint automation is triggered.

set -euo pipefail

echo "🔍  Installing project (if not already)…"
poetry install --sync --no-interaction --no-root

echo -e "\n🧹  Code quality (black, mypy, flake8)…"
poetry run nox -rs lint

echo -e "\n✅  Running pytest…"
poetry run nox -rs tests
