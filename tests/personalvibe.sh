#!/usr/bin/env bash
# tests/personalvibe.sh
#
# One script to rule them all: lint, type-check & pytest,
# **while appending all output** to logs/{semver}_base.log.

set -euo pipefail

# ------------------------------------------------------------------- #
# Detect semver (either exported or from current git branch)
# ------------------------------------------------------------------- #
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")"
if [[ "$BRANCH" =~ ^vibed\/(.+)$ ]]; then
  SEMVER="${BASH_REMATCH[1]}"
else
  SEMVER="${SEMVER:-dev}"
fi

LOG_DIR="logs"
LOG_FILE="${LOG_DIR}/${SEMVER}_base.log"
mkdir -p "${LOG_DIR}"
touch "${LOG_FILE}"

# Duplicate *everything* to the semver log (append mode)
exec > >(tee -a "${LOG_FILE}") 2>&1

echo "🔍  Installing project (if not already)…"
poetry install --sync --no-interaction --no-root

# We dont worry about this for now, maybe later when we get more pedantic
# echo -e "\n🧹  Code quality (black, mypy, flake8)…"
# poetry run nox -rs lint

echo -e "\n✅  Running pytest…"
poetry run nox -rs tests
