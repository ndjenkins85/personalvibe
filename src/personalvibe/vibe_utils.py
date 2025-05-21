# Copyright © 2025 by Nick Jenkins. All rights reserved
import hashlib
import html
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List, Union

import dotenv
import requests
import tiktoken
from jinja2 import Environment, FileSystemLoader, select_autoescape
from openai import OpenAI

dotenv.load_dotenv()
client = OpenAI()

log = logging.getLogger(__name__)


def get_prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def find_existing_hash(root_dir: str, hash_str: str) -> Union[str, None]:
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if hash_str in filename:
                return Path(dirpath) / filename
    return None


def save_prompt(prompt: str, root_dir: Path, input_hash: str = "") -> Path:
    """Persist *one* prompt to disk and return its Path.

    Behaviour
    ----------
    • Uses SHA-256(prompt)[:10] to create a stable short-hash.
    • If a file containing that hash already exists, nothing is written
      and the *existing* Path is returned.
    • New files are named   <timestamp>[_<input_hash>]_ <hash>.md
    • Every file is terminated with an extra line::

          ### END PROMPT

      to make `grep -A999 '^### END PROMPT$'` trivially reliable.
    """
    # Timestamp + hash bits
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    hash_str = get_prompt_hash(prompt)[:10]

    if existing := find_existing_hash(root_dir, hash_str):
        log.info("Duplicate prompt detected. Existing file: %s", existing)
        return existing

    # Compose filename
    if input_hash:
        filename = f"{timestamp}_{input_hash}_{hash_str}.md"
    else:
        filename = f"{timestamp}_{hash_str}.md"
    filepath = Path(root_dir) / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Write prompt + END-marker
    filepath.write_text(
        f"""{prompt}
### END PROMPT
""",
        encoding="utf-8",
    )
    log.info("Prompt saved to: %s", filepath)
    return filepath


def get_vibed(
    prompt: str, contexts: List[Path] = None, project_name=str, model: str = "o3", max_completion_tokens=100_000
) -> str:
    """Wrapper for O3 vibecoding to manage history and file interface"""
    if not contexts:
        contexts = []

    base_input_path = Path("data", project_name, "prompt_inputs")
    if not base_input_path.exists():
        log.info(f"Creating {base_input_path}")
        base_input_path.mkdir(parents=True)
    prompt_file = save_prompt(prompt, base_input_path)
    input_hash = prompt_file.stem.split("_")[-1]

    messages = []
    for context in contexts:
        if "prompt_inputs" in context.parts:
            c = {"role": "user", "content": [{"type": "text", "text": context.read_text()}]}
        elif "prompt_outputs" in context.parts:
            c = {"role": "assistant", "content": [{"type": "text", "text": context.read_text()}]}
        messages.append(c)

    c = {"role": "user", "content": [{"type": "text", "text": prompt}]}
    messages.append(c)

    message_chars = len(str(messages))
    message_tokens = num_tokens(str(messages), model=model)
    log.info(f"Prompt input size - Tokens: {message_tokens}, Chars: {message_chars}")

    response = client.chat.completions.create(
        model=model, messages=messages, max_completion_tokens=max_completion_tokens
    )
    response = response.choices[0].message.content

    message_chars = len(str(response))
    message_tokens = num_tokens(str(response), model=model)
    log.info(f"Response output size - Tokens: {message_tokens}, Chars: {message_chars}")

    base_output_path = Path("data", project_name, "prompt_outputs")
    if not base_output_path.exists():
        log.info(f"Creating {base_output_path}")
        base_output_path.mkdir(parents=True)
    _ = save_prompt(response, base_output_path, input_hash=input_hash)
    return response


def get_context(filenames: List[str], extension: str = ".txt") -> str:
    """Pulls in many file contexts, resolving wildcards only in lines inside the files."""
    big_string = ""
    base_path = get_base_path()

    for name in filenames:
        file_path = base_path / name

        if not file_path.exists():
            print(f"Warning: {file_path} does not exist. {os.getcwd()}")
            continue

        lines = file_path.read_text(encoding="utf-8").splitlines()
        unique_lines = sorted(set(lines))
        file_path.write_text("\n".join(unique_lines) + "\n", encoding="utf-8")

        for line in unique_lines:
            if not line.strip():
                continue  # Skip empty lines

            line_path = base_path / line
            if any(char in line for char in "*?[]"):  # Wildcard detected
                matches = sorted(base_path.glob(line))
                if not matches:
                    log.warning(f"No matches found for wildcard pattern: {line}")
                for match in matches:
                    if match.is_file():
                        big_string += _process_file(match)
            else:
                if not line_path.exists():
                    message = f"Warning: {line_path} does not exist. {os.getcwd()}"
                    log.error(message)
                    raise ValueError(message)
                big_string += _process_file(line_path)

    return big_string


def _process_file(file_path: Path) -> str:
    """Helper to read and return file content with appropriate markdown code fences."""
    rel_path = file_path.relative_to(get_base_path())
    extension = file_path.suffix.lower()

    # Map file extensions to markdown languages
    extension_to_lang = {
        ".py": "python",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".js": "javascript",
        ".jsx": "javascript",
        ".json": "json",
        ".html": "html",
        ".md": "",  # Markdown files don’t need code fences, show raw content
        ".toml": "toml",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".txt": "",  # Plain text, no code highlighting
        ".sh": "bash",
        ".cfg": "",
        ".ini": "",
    }

    language = extension_to_lang.get(extension, "")  # Default to no highlighting if unknown

    content = file_path.read_text(encoding="utf-8")
    content = html.unescape(content)

    if extension == ".md":
        # For markdown files, don't wrap in code fences
        return f"\n#### Start of {rel_path}\n{content}\n#### End of {rel_path}\n"
    else:
        return f"\n#### Start of {rel_path}\n" f"```{language}\n" f"{content}\n" f"```\n" f"#### End of {rel_path}\n"


def get_base_path(base: str = "personalvibe") -> Path:
    """Returns the base folder directory for the entire github project."""
    new_parts = []
    for part in Path(os.getcwd()).parts:
        new_parts.append(part)
        if part == base:
            break
    return Path(*new_parts)


def num_tokens(text: str, model: str = "o3") -> int:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))


def render_prompt_template(template_path: str, replacements: dict) -> str:
    """
    Renders a prompt template using Jinja2.

    Args:
        template_path (str): Path to the Jinja2 template file, relative to templates_base.
        replacements (dict): Variables to inject into the template.

    Returns:
        str: Rendered prompt as a string.
    """
    prompt_base = Path(get_base_path(), "prompts")
    env = Environment(
        loader=FileSystemLoader(prompt_base),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template(template_path)
    return template.render(**replacements)


def _get_error_text(config) -> str:
    error_path = Path(get_base_path(), "prompts", config.project_name, "errors", config.error_file_name)
    # NOTE TO LLM: improve the handling here as per my usual codestyle
    return error_path.read_text()


def _get_milestone_text(config) -> str:
    stages_path = Path(get_base_path(), "prompts", config.project_name, "stages")
    milestone_ver, _, _ = config.version.split(".")
    current_major = int(milestone_ver)

    milestone_files = sorted(
        [p for p in stages_path.glob("*.0.0.md") if p.is_file() and int(p.stem.split(".")[0]) <= current_major],
        key=lambda x: int(x.stem.split(".")[0]),
    )

    if not milestone_files:
        raise ValueError(f"No valid milestone files found in {stages_path} for major <= {current_major}")
    data = """The following are all milestones related to this project.
    The latest milestone text proposes next work needed, this is what sprints focus on:
    """
    data += "\n\n".join(p.read_text() for p in milestone_files)
    return data


def get_replacements(config, code_context: str) -> dict:
    """
    Build the Jinja replacement map once.

    * Milestone mode injects a standard execution task by default
      unless the YAML overrides it.
    """
    log.info(f"Running config version: {config.version}")
    log.info(f"Running mode = {config.mode}")
    milestone_ver, sprint_ver, bugfix_ver = config.version.split(".")
    if config.mode == "prd":
        exec_task = config.execution_task
        instructions = ""
    elif config.mode == "milestone":
        exec_task = "conduct milestone analysis according to guidelines"
        instructions = Path(get_base_path(), "prompts", config.project_name, "commands", "milestone.md").read_text()
    elif config.mode == "sprint":
        exec_task = f"perform the sprint number marked {sprint_ver}"
        instructions = (
            Path(get_base_path(), "prompts", config.project_name, "commands", "sprint.md").read_text()
            + "\n"
            + _get_milestone_text(config)
        )
    elif config.mode == "validate":
        exec_task = f"validate the following logs following the generation of sprint {sprint_ver}"
        instructions = (
            Path(get_base_path(), "prompts", config.project_name, "commands", "validate.md").read_text()
            + "\n"
            + _get_milestone_text(config)
            + "\n"
            + _get_error_text(config)
        )

    return {
        "execution_task": exec_task,
        "execution_details": config.execution_details,
        "instructions": instructions,
        "code_context": code_context,
    }
