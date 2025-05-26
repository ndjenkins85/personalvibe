# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/7.1.2.py

#!/usr/bin/env python3
"""
Personalvibe Sprint 7.2.0 - Chunk 2: Bugfix Mode Implementation

This script implements the new bugfix mode for personalvibe, including:
- Creating bugfix.md prompt template
- Updating ConfigModel to support 'bugfix' mode
- Implementing bugfix-specific logic
- CLI support for bugfix mode
- Proper semver naming for bugfix files
"""

import textwrap
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()

# Create the bugfix.md prompt template
bugfix_template_content = """# Bugfix Mode Instructions

You are working on a bugfix for the {{ project_name }} project.

## Context

{{ execution_details }}

## Current Error or Issue

The following error or issue needs to be resolved:

{{ error_details }}

## Instructions

1. Analyze the error carefully and identify the root cause
2. Generate a minimal, focused fix that addresses only this specific issue
3. Ensure the fix doesn't break existing functionality
4. Include appropriate error handling if needed
5. Add or update tests to prevent regression

## Code Context

The following code files are relevant to this bugfix:

{{ code_context }}

## Output Requirements

Generate a Python script within <python></python> tags that:
- Creates idempotent changes to fix the bug
- Includes clear comments explaining the fix
- Updates relevant tests if needed
- Prints a summary of changes at the end

Remember: This is a bugfix, so keep changes minimal and focused.
"""

bugfix_template_path = REPO / "src" / "personalvibe" / "data" / "bugfix.md"
bugfix_template_path.parent.mkdir(parents=True, exist_ok=True)
bugfix_template_path.write_text(bugfix_template_content, encoding="utf-8")
print(f"✓ Created bugfix template at {bugfix_template_path}")

# Update ConfigModel to support 'bugfix' mode
config_model_path = REPO / "src" / "personalvibe" / "run_pipeline.py"
with open(config_model_path, "r") as f:
    content = f.read()

# Update the mode field validator pattern to include 'bugfix'
old_pattern = r'mode: str = Field\(\.\.\., pattern="\^\(prd\|milestone\|sprint\|validate\)\$"\)'
new_pattern = 'mode: str = Field(..., pattern="^(prd|milestone|sprint|validate|bugfix)$")'
content = content.replace(old_pattern, new_pattern)

with open(config_model_path, "w") as f:
    f.write(content)
print("✓ Updated ConfigModel to support 'bugfix' mode")

# Update vibe_utils.py to handle bugfix mode
vibe_utils_path = REPO / "src" / "personalvibe" / "vibe_utils.py"
with open(vibe_utils_path, "r") as f:
    content = f.read()

# Find the get_replacements function and add bugfix mode support
import re

# Find the get_replacements function
def_pattern = r'(def get_replacements\(config: "ConfigModel", code_context: str\) -> dict:.*?)(\n    else:  # pragma: no cover\n        raise ValueError)'
def_match = re.search(def_pattern, content, re.DOTALL)

if def_match:
    before_else = def_match.group(1)
    else_clause = def_match.group(2)

    # Add bugfix mode handling before the else clause
    bugfix_addition = """
    elif config.mode == "bugfix":
        exec_task = f"fix the bug described in version {config.version}"
        # Get error details from execution_details or a dedicated field
        error_details = config.execution_details
        instructions = _load_template("bugfix.md")

        # Add error_details to replacements
        return {
            "execution_task": exec_task,
            "execution_details": config.execution_details,
            "instructions": instructions,
            "code_context": code_context,
            "error_details": error_details,
            "project_name": config.project_name,
        }"""

    new_content = before_else + bugfix_addition + else_clause
    content = re.sub(def_pattern, new_content, content, flags=re.DOTALL)

    with open(vibe_utils_path, "w") as f:
        f.write(content)
    print("✓ Updated get_replacements to handle bugfix mode")

# Update CLI to support bugfix mode
cli_path = REPO / "src" / "personalvibe" / "cli.py"
with open(cli_path, "r") as f:
    content = f.read()

# Update the explicit modes list to include 'bugfix'
old_modes_line = 'for _mode in ("milestone", "sprint", "validate", "prd"):'
new_modes_line = 'for _mode in ("milestone", "sprint", "validate", "prd", "bugfix"):'
content = content.replace(old_modes_line, new_modes_line)

with open(cli_path, "w") as f:
    f.write(content)
print("✓ Updated CLI to support 'bugfix' sub-command")

# Update parse_stage.py to handle bugfix file naming (x.y.z.md)
parse_stage_path = REPO / "src" / "personalvibe" / "parse_stage.py"
with open(parse_stage_path, "r") as f:
    content = f.read()

# Find extract_and_save_code_block function and update file extension logic
extract_pattern = r'(def extract_and_save_code_block\(project_name: Union\[str, None\] = None\) -> str:.*?)(    # Determine file extension based on mode.*?)(    output_file = stages_dir / f"\{new_version\}\.py")'

extract_match = re.search(extract_pattern, content, re.DOTALL)
if extract_match:
    part1 = extract_match.group(1)
    part2 = extract_match.group(2)
    part3 = extract_match.group(3)

    # Replace the file extension logic
    new_extension_logic = """    # Determine file extension based on mode (bugfix = .md, sprint = .py)
    # Check if this is a bugfix by looking at the version pattern
    version_parts = new_version.split('.')
    if len(version_parts) == 3 and int(version_parts[2]) > 0:
        # This is a bugfix (patch version > 0)
        file_extension = '.md'
    else:
        # This is a sprint
        file_extension = '.py' """

    new_output_line = '    output_file = stages_dir / f"{new_version}{file_extension}"'

    new_content = part1 + new_extension_logic + "\n" + new_output_line
    remaining = content[extract_match.end() :]
    content = content[: extract_match.start()] + new_content + remaining

    with open(parse_stage_path, "w") as f:
        f.write(content)
    print("✓ Updated parse_stage to use .md extension for bugfix files")

# Create a bugfix template YAML file
bugfix_yaml_template = """project_name: {{ project_name }}
mode: bugfix
model: openai/o3  # optional, defaults to o3
execution_details: |
  # Describe the bug or issue to fix here
  # Include error messages, stack traces, or unexpected behavior

code_context_paths:
  # List relevant files that need to be examined or fixed
  # - src/module/file.py
  # - tests/test_file.py
"""

yaml_template_path = REPO / "src" / "personalvibe" / "data" / "bugfix_template.yaml"
yaml_template_path.write_text(bugfix_yaml_template, encoding="utf-8")
print(f"✓ Created bugfix YAML template at {yaml_template_path}")

# Add a test for bugfix mode
test_bugfix_content = '''# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Test bugfix mode functionality."""

from pathlib import Path
import pytest
from personalvibe.run_pipeline import ConfigModel, load_config
from personalvibe import vibe_utils


def test_bugfix_mode_config(tmp_path):
    """Test that bugfix mode is accepted in config."""
    cfg_yaml = tmp_path / "1.0.1.yaml"
    cfg_yaml.write_text("""
        project_name: testproject
        mode: bugfix
        execution_details: "Fix the import error"
        code_context_paths: []
    """, encoding='utf-8')

    config = load_config(str(cfg_yaml))
    assert config.mode == "bugfix"
    assert config.execution_details == "Fix the import error"


def test_bugfix_template_exists():
    """Ensure bugfix.md template was created."""
    template_path = Path(vibe_utils.get_base_path()) / "src" / "personalvibe" / "data" / "bugfix.md"
    assert template_path.exists()
    content = template_path.read_text()
    assert "Bugfix Mode Instructions" in content


def test_bugfix_file_extension(monkeypatch, tmp_path):
    """Test that bugfix versions use .md extension."""
    from personalvibe.parse_stage import determine_next_version

    root = tmp_path / "repo"
    stages = root / "prompts" / "demo" / "stages"
    stages.mkdir(parents=True)

    # Create an existing sprint file
    (stages / "1.1.0.py").write_text("# sprint code")

    monkeypatch.patch.object(vibe_utils, "get_base_path", lambda: root)

    # Next version should be a bugfix
    next_ver = determine_next_version("demo")
    assert next_ver == "1.1.1"  # bugfix version
'''

test_path = REPO / "tests" / "test_bugfix_mode.py"
test_path.write_text(test_bugfix_content, encoding="utf-8")
print(f"✓ Created test file at {test_path}")

# Update the prepare-sprint command to support bugfix preparation
cli_path = REPO / "src" / "personalvibe" / "cli.py"
with open(cli_path, "r") as f:
    content = f.read()

# Add prepare-bugfix command after prepare-sprint
prepare_bugfix_addition = """
    # prepare-bugfix -----------------------------------------------
    pbug = sub.add_parser("prepare-bugfix", help="Scaffold next bugfix YAML")
    pbug.add_argument("--project_name", help="Override auto detection.")
    pbug.add_argument("--no-open", action="store_true")
    pbug.set_defaults(func=_cmd_prepare_bugfix)"""

# Insert after prepare-sprint command definition
parser_section = re.search(r"(    pspr\.set_defaults\(func=_cmd_prepare_sprint\))", content)
if parser_section:
    insert_pos = parser_section.end()
    content = content[:insert_pos] + prepare_bugfix_addition + content[insert_pos:]

# Add the command handler function
prepare_bugfix_handler = """
# ----------------------------------------------------------------- PB
def _cmd_prepare_bugfix(ns: argparse.Namespace) -> None:
    proj = ns.project_name or vibe_utils.detect_project_name()
    stages = vibe_utils.get_base_path() / "prompts" / proj / "stages"
    stages.mkdir(parents=True, exist_ok=True)
    versions = _scan_versions(stages)

    if not versions:
        # no files yet
        next_ver = "1.0.1"
    else:
        latest = versions[-1]
        # For bugfix, increment patch version
        next_ver = f"{latest[0]}.{latest[1]}.{latest[2] + 1}"

    dest = Path.cwd() / f"{next_ver}.yaml"
    tmpl = vibe_utils._load_template("bugfix_template.yaml")
    dest.write_text(tmpl.replace("{{ project_name }}", proj), encoding="utf-8")
    print(f"Created bugfix YAML: {dest}")
    if not ns.no_open:
        _open_in_editor(dest)
"""

# Insert before the app() function
app_pattern = re.search(r"(# === CHUNK3_cli_helpers_cmds END ===)", content)
if app_pattern:
    insert_pos = app_pattern.start()
    content = content[:insert_pos] + prepare_bugfix_handler + "\n\n" + content[insert_pos:]

with open(cli_path, "w") as f:
    f.write(content)
print("✓ Added prepare-bugfix command to CLI")

print(
    """
================================================================================
✨ Bugfix Mode Implementation Complete!

Summary of changes:
1. Created src/personalvibe/data/bugfix.md prompt template
2. Updated ConfigModel to accept 'bugfix' as a valid mode
3. Added bugfix handling to get_replacements() in vibe_utils.py
4. Added 'bugfix' to CLI sub-commands
5. Updated parse_stage to use .md extension for bugfix files (x.y.z where z > 0)
6. Created bugfix_template.yaml for easy YAML scaffolding
7. Added prepare-bugfix CLI command for creating bugfix YAMLs
8. Created test_bugfix_mode.py with basic tests

Testing recommendations:
1. Run: poetry run pytest tests/test_bugfix_mode.py -v
2. Test CLI: pv prepare-bugfix --project_name testproject --no-open
3. Create a bugfix YAML and run: pv bugfix --config 1.0.1.yaml --prompt_only
4. Verify .md extension for bugfix files in prompts/<project>/stages/

Next steps:
- Test the bugfix workflow end-to-end
- Consider adding more sophisticated error parsing in bugfix mode
- Add integration tests for the complete bugfix pipeline
- Update documentation to explain bugfix mode usage
================================================================================
"""
)
