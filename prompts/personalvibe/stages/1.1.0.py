# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/1.1.0.py
#!/usr/bin/env python
"""
apply_sprint1_patch.py  – Sprint 1: Logging Harness & Tests
==========================================================

Run this file **once** from *any* sub-directory of the repo:

    poetry run python apply_sprint1_patch.py

It will …
1. PATCH src/personalvibe/logger.py  (BEGIN-STAMP + “_base” logic)
2. PATCH src/personalvibe/run_pipeline.py  (derive run_id = <semver>_base)
3. PATCH tests/personalvibe.sh  (pipe all stdout/stderr -> logs/{semver}_base.log)
4. ADD   tests/test_logging.py   (pytest safety-net)

Afterwards you can validate with:

    nox -s tests
"""
from __future__ import annotations

import textwrap
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content.lstrip("\n")), encoding="utf-8")
    print(f"✔  Wrote {path.relative_to(REPO)}")


# --------------------------------------------------------------------------- #
# 1. LOGGER PATCH
# --------------------------------------------------------------------------- #
logger_py = """
# Copyright © 2025 by Nick Jenkins.
\"\"\"Opinionated Structured Logging (per-run log file aware).\"\"\"

from __future__ import annotations

import logging
import logging.config
import sys
from datetime import datetime
from pathlib import Path
from typing import Literal

_configured = False


class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\\033[94m",
        "INFO": "\\033[92m",
        "WARNING": "\\033[93m",
        "ERROR": "\\033[91m",
        "CRITICAL": "\\033[95m",
    }
    RESET = "\\033[0m"

    def format(self, record):  # type: ignore[override]
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f\"{color}{record.levelname}{self.RESET}\"
        return super().format(record)


def configure_logging(
    verbosity: Literal[\"verbose\", \"none\", \"errors\"] | str = \"none\",
    *,
    color: bool = True,
    run_id: str | None = None,
    log_dir: str | Path = \"logs\",
) -> None:
    \"\"\"Idempotent logging bootstrap.

    Parameters
    ----------
    verbosity
        \"verbose\" = DEBUG, \"none\" = INFO (default), \"errors\" = ERROR
    run_id
        When supplied, a *file* handler is attached at
        ``<log_dir>/<run_id>.log``. First call for a given run_id will
        create the file and write::

            RUN_ID=<run_id>               # line-1
            BEGIN-STAMP <iso-timestamp>   # line-2  (always for *_base)

        Subsequent processes with the *same* run_id will **append** a fresh
        BEGIN-STAMP line (useful for tee piping).
    \"\"\"
    global _configured
    if _configured:  # pragma: no cover
        return

    # ------------------------ base console handler -------------------------
    levels = {\"verbose\": logging.DEBUG, \"none\": logging.INFO, \"errors\": logging.ERROR}
    level = levels.get(verbosity, logging.INFO)

    fmt = \"%(asctime)s | %(levelname)s | %(name)s | %(message)s\"
    date = \"%Y-%m-%d %H:%M:%S\"
    formatter_cls = ColorFormatter if color else logging.Formatter
    formatter = formatter_cls(fmt=fmt, datefmt=date)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logging.root.setLevel(level)
    logging.root.handlers.clear()
    logging.root.addHandler(console_handler)

    # ----------------------------- file handler ----------------------------
    if run_id:
        log_path = Path(log_dir) / f\"{run_id}.log\"
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Create file with RUN_ID header on first ever write
        if not log_path.exists():
            log_path.write_text(f\"RUN_ID={run_id}\\n\", encoding=\"utf-8\")

        # For *_base logs record a session stamp **every** invocation
        if run_id.endswith(\"_base\"):
            ts = datetime.utcnow().isoformat(timespec=\"seconds\")
            with log_path.open(\"a\", encoding=\"utf-8\") as fh:
                fh.write(f\"BEGIN-STAMP {ts}\\n\")

        file_handler = logging.FileHandler(log_path, mode=\"a\", encoding=\"utf-8\")
        file_handler.setFormatter(logging.Formatter(fmt, date))
        logging.root.addHandler(file_handler)

    _configured = True


def reset_logging() -> None:
    \"\"\"Utility for unit tests – wipes all handlers so we can re-init.\"\"\"
    global _configured
    logging.root.handlers.clear()
    _configured = False
"""

write(Path(REPO, "src/personalvibe/logger.py"), logger_py)

# --------------------------------------------------------------------------- #
# 2. run_pipeline PATCH
# --------------------------------------------------------------------------- #
run_pipeline_py = """
# Copyright © 2025 by Nick Jenkins. All rights reserved
\"\"\"Orchestrates YAML → prompt rendering → vibecoding.\"\"\"

import argparse
import logging
from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, Field, ValidationError

from personalvibe import logger, vibe_utils


class ConfigModel(BaseModel):
    version: str
    project_name: str
    mode: str = Field(..., pattern=\"^(prd|milestone|sprint|validate)$\")
    execution_task: Optional[str] = None
    execution_details: str = \"\"
    code_context_paths: List[str]
    milestone_file_name: str = \"\"
    error_file_name: str = \"\"


def load_config(config_path: str) -> ConfigModel:
    \"\"\"Load & validate YAML config; bubble schema errors.\"\"\"
    with open(config_path, \"r\", encoding=\"utf-8\") as f:
        raw = yaml.safe_load(f)
        raw[\"version\"] = Path(config_path).stem
    try:
        return ConfigModel(**raw)
    except ValidationError as e:
        logging.getLogger(__name__).error(\"Config validation failed:\\n%s\", e)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=\"Run the Personalvibe Workflow.\")
    parser.add_argument(\"--config\", required=True, help=\"Path to YAML config file.\")
    parser.add_argument(
        \"--verbosity\", choices=[\"verbose\", \"none\", \"errors\"], default=\"none\", help=\"Console log level\"
    )
    parser.add_argument(\"--prompt_only\", action=\"store_true\", help=\"If set, only generate the prompt.\")
    args = parser.parse_args()

    # 1️⃣  Parse config first – we need the semver to derive run_id
    config = load_config(args.config)
    run_id = f\"{config.version}_base\"

    # 2️⃣  Bootstrap logging (console + per-semver file)
    logger.configure_logging(args.verbosity, run_id=run_id)
    log = logging.getLogger(__name__)
    log.info(\"P  E  R  S  O  N  A  L  V  I  B  E  – run_id=%s\", run_id)

    # 3️⃣  Render prompt template ------------------------------------------------
    code_context = vibe_utils.get_context(config.code_context_paths)
    replacements = vibe_utils.get_replacements(config, code_context)

    template_map = {\"prd\": \"\", \"milestone\": \"\", \"sprint\": \"\", \"validate\": \"\"}
    template_path = f\"{config.project_name}/prd.md\"
    if not template_path:
        log.error(\"Unsupported mode '%s'.\", config.mode)
        return

    prompt = vibe_utils.render_prompt_template(template_path, replacements=replacements)

    if args.prompt_only:
        base_input_path = Path(\"data\", config.project_name, \"prompt_inputs\")
        base_input_path.mkdir(parents=True, exist_ok=True)
        _ = vibe_utils.save_prompt(prompt, base_input_path)
    else:
        vibe_utils.get_vibed(prompt, project_name=config.project_name, max_completion_tokens=20_000)


if __name__ == \"__main__\":  # pragma: no cover
    main()
"""

write(Path(REPO, "src/personalvibe/run_pipeline.py"), run_pipeline_py)

# --------------------------------------------------------------------------- #
# 3. tests/personalvibe.sh PATCH
# --------------------------------------------------------------------------- #
personalvibe_sh = r"""
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

echo -e "\n🧹  Code quality (black, mypy, flake8)…"
poetry run nox -rs lint

echo -e "\n✅  Running pytest…"
poetry run nox -rs tests
"""

write(Path(REPO, "tests/personalvibe.sh"), personalvibe_sh)

# --------------------------------------------------------------------------- #
# 4. NEW unit test
# --------------------------------------------------------------------------- #
test_logging_py = """
\"\"\"Unit tests for the enhanced logging harness.\"\"\"
from pathlib import Path

from personalvibe import logger


def test_logfile_created(tmp_path: Path) -> None:
    \"\"\"configure_logging() must create <run_id>.log & stamp it.\"\"\"
    run_id = "0.0.1_base"
    logger.reset_logging()
    logger.configure_logging("none", run_id=run_id, log_dir=tmp_path)

    log_file = tmp_path / f"{run_id}.log"
    assert log_file.exists(), "Log file should be created"

    lines = log_file.read_text().splitlines()
    assert lines[0] == f"RUN_ID={run_id}"
    assert lines[1].startswith("BEGIN-STAMP"), "Missing session stamp"
    logger.reset_logging()
"""

write(Path(REPO, "tests/test_logging.py"), test_logging_py)

# --------------------------------------------------------------------------- #
print(
    "\n✅  Sprint 1 patch applied.\n\n"
    "Next steps:\n"
    "  • Run `nox -s tests` to ensure the new pytest passes.\n"
    "  • Use `nox -s vibed -- 1.1.0` in a follow-up sprint once Sprint-2 "
    "enhancements are implemented.\n"
)
