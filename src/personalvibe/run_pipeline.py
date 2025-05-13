# Copyright © 2025 by Nick Jenkins. All rights reserved
"""Orchestrates YAML → prompt rendering → vibecoding."""

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
    mode: str = Field(..., pattern="^(prd|milestone|sprint|validate)$")
    execution_task: Optional[str] = None
    execution_details: str = ""
    code_context_paths: List[str]
    milestone_file_name: str = ""
    error_file_name: str = ""


def load_config(config_path: str) -> ConfigModel:
    """Load & validate YAML config; bubble schema errors."""
    with open(config_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
        raw["version"] = Path(config_path).stem
    try:
        return ConfigModel(**raw)
    except ValidationError as e:
        logging.getLogger(__name__).error("Config validation failed:\n%s", e)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Personalvibe Workflow.")
    parser.add_argument("--config", required=True, help="Path to YAML config file.")
    parser.add_argument("--verbosity", choices=["verbose", "none", "errors"], default="none", help="Console log level")
    parser.add_argument("--prompt_only", action="store_true", help="If set, only generate the prompt.")
    parser.add_argument("--max_retries", type=int, default=5, help="Maximum attempts for sprint validation")
    args = parser.parse_args()

    # 1️⃣  Parse config first – we need the semver to derive run_id
    config = load_config(args.config)
    run_id = f"{config.version}_base"

    # 2️⃣  Bootstrap logging (console + per-semver file)
    logger.configure_logging(args.verbosity, run_id=run_id)
    log = logging.getLogger(__name__)
    log.info("P  E  R  S  O  N  A  L  V  I  B  E  – run_id=%s", run_id)

    # 3️⃣  Render prompt template ------------------------------------------------
    code_context = vibe_utils.get_context(config.code_context_paths)
    replacements = vibe_utils.get_replacements(config, code_context)

    template_map = {"prd": "", "milestone": "", "sprint": "", "validate": ""}
    template_path = f"{config.project_name}/prd.md"
    if not template_path:
        log.error("Unsupported mode '%s'.", config.mode)
        return

    prompt = vibe_utils.render_prompt_template(template_path, replacements=replacements)

    if args.prompt_only:
        base_input_path = Path("data", config.project_name, "prompt_inputs")
        base_input_path.mkdir(parents=True, exist_ok=True)
        _ = vibe_utils.save_prompt(prompt, base_input_path)
    else:
        vibe_utils.get_vibed(prompt, project_name=config.project_name, max_completion_tokens=20_000)


if __name__ == "__main__":  # pragma: no cover
    main()
