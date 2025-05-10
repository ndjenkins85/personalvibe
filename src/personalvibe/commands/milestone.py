# Copyright © 2025 by Nick Jenkins. All rights reserved

# Copyright © 2025 Nick Jenkins
from pathlib import Path
from typing import Dict, List

from personalvibe import vibe_utils


def draft_milestone(
    prd_path: str,
    project_name: str,
    execution_task: str,
    execution_details: str,
    code_context_paths: List[str],
    extra_vars: Dict[str, str] | None = None,
    model: str = "o3",
) -> str:
    """
    Renders the PRD-milestone prompt, calls the LLM once, saves I/O, and
    returns the raw response (caller can parse or display).

    extra_vars lets you push in ad-hoc template vars without changing
    the function signature every time.
    """
    prd_template = Path(prd_path).read_text()

    code_context = vibe_utils.get_context(code_context_paths)

    replacements = {
        "execution_task": execution_task,
        "execution_details": execution_details,
        "code_context": code_context,
        "project_name": project_name,
    }
    if extra_vars:
        replacements.update(extra_vars)

    # We re-use your existing template renderer on a string:
    prompt = vibe_utils.render_prompt_template(
        template_path=prd_path,  # path relative to prompts/
        replacements=replacements,
        templates_base=vibe_utils.get_base_path() / "prompts",
    )

    # One-shot LLM call & persistence
    response = vibe_utils.get_vibed(
        prompt=prompt,
        contexts=[],
        project_name=project_name,
        model=model,
    )

    return response  # get_vibed already persists I/O; returning is convenience
