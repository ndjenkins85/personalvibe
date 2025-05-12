# Copyright © 2025 by Nick Jenkins. All rights reserved

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
    """Load and validate YAML config, logging any schema errors."""
    log = logging.getLogger(__name__)
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)
        raw_config["version"] = Path(config_path).stem
    try:
        return ConfigModel(**raw_config)
    except ValidationError as e:
        log.error("Config validation failed:\n%s", e)
        raise


def main():
    parser = argparse.ArgumentParser(description="Run the Personalvibe Workflow.")
    parser.add_argument("--config", required=True, help="Path to YAML config file.")
    parser.add_argument("--verbosity", choices=["verbose", "none", "errors"], default="none")
    parser.add_argument("--prompt_only", action="store_true", help="If set, only generate the prompt.")
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # 1️⃣  Centralised logging – one call, early.
    #     Accepts 'verbose' | 'none' | 'errors'
    # ------------------------------------------------------------------
    logger.configure_logging(args.verbosity)

    log = logging.getLogger(__name__)
    log.info("P  E  R  S  O  N  A  L  V  I  B  E")

    config = load_config(args.config)

    code_context = vibe_utils.get_context(config.code_context_paths)

    replacements = vibe_utils.get_replacements(config, code_context)

    template_map = {"prd": "", "milestone": "", "sprint": "", "validate": ""}

    template_path = f"{config.project_name}/prd.md"
    if not template_path:
        log.error(f"Unsupported mode '{config.mode}'. Must be one of {list(template_map.keys())}.")
        return

    prompt = vibe_utils.render_prompt_template(template_path, replacements=replacements)
    if args.prompt_only:
        base_input_path = Path("data", config.project_name, "prompt_inputs")
        if not base_input_path.exists():
            log.info(f"Creating {base_input_path}")
            base_input_path.mkdir(parents=True)
        _ = vibe_utils.save_prompt(prompt, base_input_path)
    else:
        vibe_utils.get_vibed(prompt, project_name=config.project_name, max_completion_tokens=20_000)


if __name__ == "__main__":
    main()
