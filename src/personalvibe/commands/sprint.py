# Copyright © 2025 by Nick Jenkins. All rights reserved

from pathlib import Path
from typing import Dict, Iterable, List

from personalvibe import vibe_utils


def execute_sprint(
    prd_path: str,
    project_name: str,
    milestone_plan: str,
    sprint_name: str,
    execution_details: str,
    code_context_paths: List[str],
    max_iterations: int = 3,
    extra_vars: Dict[str, str] | None = None,
    model: str = "o3",
) -> Iterable[str]:
    """
    Interactive sprint executor. Yields every assistant response so the
    caller can inspect success/failure and decide to break early.

    It loops up to `max_iterations` times, passing previous assistant
    output back in as context when needed.
    """
    # 1) Static bits
    prd_template = Path(prd_path).read_text()
    code_context = vibe_utils.get_context(code_context_paths)

    # 2) Iterative loop
    assistant_history: list[str] = []
    for i in range(max_iterations):
        replacements = {
            "milestone_plan": milestone_plan,
            "sprint_name": sprint_name,
            "execution_details": execution_details,
            "code_context": code_context,
            "prev_attempt": assistant_history[-1] if assistant_history else "",
            "iteration": i + 1,
            "project_name": project_name,
        }
        if extra_vars:
            replacements.update(extra_vars)

        prompt = vibe_utils.render_prompt_template(
            prd_path,
            replacements=replacements,
            templates_base=vibe_utils.get_base_path() / "prompts",
        )

        response = vibe_utils.get_vibed(
            prompt=prompt,
            contexts=[],
            project_name=project_name,
            model=model,
        )

        assistant_history.append(response)
        yield response  # let caller evaluate success/failure

        # crude success check: caller sets a flag in the response
        if "SPRINT_SUCCESS" in response:
            break
