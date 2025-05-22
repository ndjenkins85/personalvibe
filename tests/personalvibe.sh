#!/usr/bin/env bash
# tests/personalvibe.sh  —  consolidated quality-gate (Chunk C)
#
# Purpose:
#   • install *runtime* deps (`--no-root`) so wheel-building works
#   • delegate to **nox** for the actual quality-gate
#   • append *all* stdout/stderr to    logs/<semver>_base.log
#
# Sessions executed:
#   nox -rs lint tests smoke_dist
#
# Behaviour:
#   • `set -euo pipefail` → any failure exits non-zero (CI-friendly)
#   • first positional arg overrides the <semver> used for the log file
#   • keeps backward-compat banners so existing tests don’t break
set -euo pipefail

### ---------- derive SEMVER for log routing ---------------------------------
if [[ $# -ge 1 && -n "$1" ]]; then
  SEMVER="$1"; shift
else
  BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")"
  if [[ "$BRANCH" =~ ^vibed\/([^/]+)$ ]]; then
    SEMVER="${BASH_REMATCH[1]}"
  else
    SEMVER="${SEMVER:-dev}"
  fi
fi

LOG_DIR="logs"
LOG_FILE="${LOG_DIR}/${SEMVER}_base.log"
mkdir -p "${LOG_DIR}"
touch "${LOG_FILE}"

# Duplicate *everything* to the semver log (append mode)
exec > >(tee -a "${LOG_FILE}") 2>&1

echo "🔍  Installing project dependencies (poetry)…"
poetry install --sync --no-interaction --no-root

echo -e "\n🧹  Running quality-gate via nox (lint + tests + smoke_dist)…"
poetry run nox -rs lint tests smoke_dist "$@"

echo -e "\n✅  personalvibe.sh finished ok."
