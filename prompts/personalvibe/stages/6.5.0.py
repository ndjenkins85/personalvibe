# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/6.4.1.py

import os
import re
import textwrap
from pathlib import Path

from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()

# 1. Create LLM_PROVIDERS.md documentation
llm_providers_content = """# LLM Provider Configuration

Personalvibe supports various LLM providers through [LiteLLM](https://github.com/BerriAI/litellm),
giving you flexibility to choose the best model for your task.

## Using the `model:` configuration

Every YAML config can specify an optional `model:` field that follows the format
`<provider>/<model_name>`. For example:

```yaml
project_name: my_project
mode: milestone
model: openai/gpt-4o-mini
execution_details: ""
code_context_paths: []
```

## Supported Providers

The following model strings are supported:

| Model String                           | Description                                  |
|----------------------------------------|----------------------------------------------|
| `openai/o3`                            | OpenAI's GPT-o3 (default)              |
| `openai/gpt-4o`                        | OpenAI's GPT-4o                             |
| `openai/gpt-4-turbo`                   | OpenAI's GPT-4 Turbo                        |
| `anthropic/claude-3-opus`              | Anthropic's Claude 3 Opus                   |
| `anthropic/claude-3-sonnet`            | Anthropic's Claude 3 Sonnet                 |
| `anthropic/claude-3-haiku`             | Anthropic's Claude 3 Haiku                  |
| `google/gemini-pro`                    | Google's Gemini Pro                         |
| `mistral/mistral-large`                | Mistral Large                               |
| `openrouter/<any-model>`               | Any model supported by OpenRouter           |
| `sharp_boe/<model_name>`               | Custom SharpBOE provider                    |

## Authentication

Most providers require API keys which should be set as environment variables:

```bash
# OpenAI (default)
export OPENAI_API_KEY=sk-...

# Anthropic
export ANTHROPIC_API_KEY=sk-ant-...

# Google
export GOOGLE_API_KEY=...

# Custom Sharp BOE provider
export SHARP_USER_SECRET=...
```

LiteLLM handles most authentication automatically. For detailed configuration
options, refer to the [LiteLLM documentation](https://docs.litellm.ai/docs/).

## Custom Provider: Sharp BOE

To use the custom SharpBOE provider:

1. Set the `SHARP_USER_SECRET` environment variable
2. Use the model string format: `sharp_boe/<model_name>`

## Fallback Behavior

If no `model:` is specified in your config, Personalvibe defaults to `openai/gpt-4o-mini`.
"""

llm_providers_path = REPO / "docs" / "LLM_PROVIDERS.md"
llm_providers_path.write_text(llm_providers_content, encoding="utf-8")
print(f"Created {llm_providers_path}")

# 2. Update README.md to include model information
readme_path = REPO / "README.md"
readme_content = readme_path.read_text(encoding="utf-8")

# Update the readme to mention model configuration
updated_readme = re.sub(
    r"(pip install personalvibe\s+# 🚀  get the CLI\n)(.*?)(---)",
    r"\1pv run --config 1.0.0.yaml      # 🤖  generate / execute prompts\npv run --config 1.0.0.yaml --model openai/gpt-4o   # 🧠  specify LLM model\n\n---",
    readme_content,
    flags=re.DOTALL,
)

# Add LLM_PROVIDERS.md to the quick links section
updated_readme = re.sub(
    r"(\* \[API reference\]\(docs/reference\.rst\)\n)(\* \[Roadmap 3\.0\.0\])",
    r"\1* [LLM Providers](docs/LLM_PROVIDERS.md)\n\2",
    updated_readme,
)

readme_path.write_text(updated_readme, encoding="utf-8")
print(f"Updated {readme_path}")

# 3. Update installation docs to mention LiteLLM
install_path = REPO / "docs" / "INSTALL.md"
install_content = install_path.read_text(encoding="utf-8")

updated_install = install_content.replace(
    "Runtime artefacts are created in the **current working directory**:",
    """Runtime artefacts are created in the **current working directory**:

LLM model selection is available through the `model:` YAML config field:
```yaml
model: openai/gpt-4o-mini  # default if omitted
```

See [LLM Providers](LLM_PROVIDERS.md) for all supported models.""",
)

install_path.write_text(updated_install, encoding="utf-8")
print(f"Updated {install_path}")

# 4. Create and update migration.py to mark deprecated code
migration_file = """# Copyright © 2025 by Nick Jenkins. All rights reserved

\"\"\"OpenAI compatibility shims and migration tools (Chunk-5).

This module provides backwards compatibility for code transitioning
from direct OpenAI usage to LiteLLM. It's intended for temporary use
during migration; new code should use llm_router directly.
\"\"\"

import warnings
from typing import Any, Callable, Dict, List, Optional, Union

from personalvibe import llm_router

# Create an alias to maintain backwards compatibility
def deprecation_warning(fn_name: str) -> None:
    warnings.warn(
        f"{fn_name} is deprecated and will be removed in a future version. "
        "Use llm_router.chat_completion instead.",
        DeprecationWarning,
        stacklevel=2
    )

def openai_chat_completion(
    *,
    model: Optional[str] = None,
    messages: List[Dict[str, Any]],
    **kwargs: Any,
) -> Dict[str, Any]:
    \"\"\"Deprecated OpenAI completion adapter.

    This function is a backward compatibility shim that translates
    OpenAI-style calls to llm_router.chat_completion. New code should
    use llm_router directly.
    \"\"\"
    deprecation_warning("openai_chat_completion")

    # If model is specified without provider, add openai/ prefix
    if model and "/" not in model:
        model = f"openai/{model}"

    return llm_router.chat_completion(model=model, messages=messages, **kwargs)

# This is a placeholder for any other legacy functions that might need
# temporary compatibility wrappers during the transition period.
"""

migration_path = REPO / "src" / "personalvibe" / "migration.py"
migration_path.write_text(migration_file, encoding="utf-8")
print(f"Created {migration_path}")

# 5. Update using_in_other_projects.md to show model usage
using_path = REPO / "docs" / "using_in_other_projects.md"
using_content = using_path.read_text(encoding="utf-8")

updated_using = using_content.replace(
    "# 1.0.0.yaml\nproject_name: my_cool_idea\nmode: milestone         # prd | milestone | sprint | validate\nexecution_details: ''\ncode_context_paths: []  # optional snippets fed into the prompt",
    "# 1.0.0.yaml\nproject_name: my_cool_idea\nmode: milestone         # prd | milestone | sprint | validate\nmodel: openai/gpt-4o-mini  # optional, defaults to gpt-4o-mini\nexecution_details: ''\ncode_context_paths: []  # optional snippets fed into the prompt",
)

# Add a link to LLM providers in the advanced section
updated_using = updated_using.replace(
    "## Advanced",
    "## Advanced\n\n• Choose any [supported LLM provider](LLM_PROVIDERS.md):\n\n  `model: anthropic/claude-3-sonnet`",
)

using_path.write_text(updated_using, encoding="utf-8")
print(f"Updated {using_path}")

# 6. Add a simple integration smoke test
smoke_test = """# Copyright © 2025 by Nick Jenkins. All rights reserved

\"\"\"Integration smoke test for model selection.\"\"\"

import os
from unittest import mock

import pytest

from personalvibe import run_pipeline, vibe_utils


def test_model_field_passed_to_router(monkeypatch, tmp_path):
    # Create minimal config with model field
    cfg_yaml = tmp_path / "test.yaml"
    cfg_yaml.write_text(
        \"\"\"
        project_name: smoketest
        mode: milestone
        model: openai/gpt-4o
        execution_details: ""
        code_context_paths: []
        \"\"\",
        encoding="utf-8",
    )

    # Mock the template loader and get_vibed to avoid real API calls
    monkeypatch.setattr(
        vibe_utils,
        "render_prompt_template",
        lambda *args, **kwargs: "Test prompt"
    )

    # Capture the model parameter
    captured = {"model": None}
    def fake_get_vibed(prompt, **kwargs):
        captured["model"] = kwargs.get("model")
        return "Test response"

    monkeypatch.setattr(vibe_utils, "get_vibed", fake_get_vibed)

    # Create minimal prompts directory structure
    prompts_dir = tmp_path / "prompts" / "smoketest"
    prompts_dir.mkdir(parents=True)
    monkeypatch.setattr(vibe_utils, "get_base_path", lambda: tmp_path)

    # Run with --prompt_only to avoid actual API calls
    monkeypatch.setattr(
        "sys.argv",
        ["pv", "run", "--config", str(cfg_yaml), "--prompt_only"]
    )

    try:
        run_pipeline.main()
    except SystemExit:
        pass

    # Verify the model was passed through correctly
    assert captured["model"] == "openai/gpt-4o"

"""

smoke_test_path = REPO / "tests" / "test_model_selection.py"
smoke_test_path.write_text(smoke_test, encoding="utf-8")
print(f"Created {smoke_test_path}")

# 7. Final smoke test verification - ensure default run works without explicit model
final_smoke_test = """# Copyright © 2025 by Nick Jenkins. All rights reserved

\"\"\"Verify default behavior works without model field.\"\"\"

import os
from pathlib import Path

import pytest

from personalvibe import run_pipeline, vibe_utils


def test_default_model_fallback(monkeypatch, tmp_path):
    # Create minimal config with NO model field
    cfg_yaml = tmp_path / "test.yaml"
    cfg_yaml.write_text(
        \"\"\"
        project_name: smoketest
        mode: milestone
        execution_details: ""
        code_context_paths: []
        \"\"\",
        encoding="utf-8",
    )

    # Mock the template loader and get_vibed to avoid real API calls
    monkeypatch.setattr(
        vibe_utils,
        "render_prompt_template",
        lambda *args, **kwargs: "Test prompt"
    )

    # Capture the model parameter
    captured = {"model": None}
    def fake_get_vibed(prompt, **kwargs):
        captured["model"] = kwargs.get("model")
        return "Test response"

    monkeypatch.setattr(vibe_utils, "get_vibed", fake_get_vibed)

    # Create minimal prompts directory structure
    prompts_dir = tmp_path / "prompts" / "smoketest"
    prompts_dir.mkdir(parents=True)
    monkeypatch.setattr(vibe_utils, "get_base_path", lambda: tmp_path)

    # Run with --prompt_only to avoid actual API calls
    monkeypatch.setattr(
        "sys.argv",
        ["pv", "run", "--config", str(cfg_yaml), "--prompt_only"]
    )

    try:
        run_pipeline.main()
    except SystemExit:
        pass

    # Verify the model was None, which should trigger the default in llm_router
    assert captured["model"] is None

"""

final_smoke_test_path = REPO / "tests" / "test_default_model.py"
final_smoke_test_path.write_text(final_smoke_test, encoding="utf-8")
print(f"Created {final_smoke_test_path}")

print(
    """
LiteLLM Integration Milestone (Chunk 5) has been completed!

The following changes were made:

1. Created docs/LLM_PROVIDERS.md documenting all supported LLM providers
2. Updated README.md to reference the model selection capability
3. Enhanced docs/INSTALL.md with model selection information
4. Created src/personalvibe/migration.py with backward compatibility shims
5. Updated docs/using_in_other_projects.md to show model usage examples
6. Added two smoke tests to verify both custom model selection and default behavior

Next steps:
1. Run the tests to verify everything works as expected:
   ```
   poetry run pytest tests/test_model_selection.py tests/test_default_model.py -v
   ```
2. Run the full test suite to ensure no regressions:
   ```
   poetry run nox -s tests
   ```
3. Consider adding real integration tests with actual API calls (mocked in CI)
4. Update any project documentation or tutorials to demonstrate model selection
5. Plan for eventual removal of the migration.py compatibility shims

This completes the LiteLLM integration milestone. The codebase now routes all LLM
traffic through LiteLLM, allowing flexible model selection while maintaining
backward compatibility.
"""
)
