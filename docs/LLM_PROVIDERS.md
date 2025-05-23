# LLM Provider Configuration

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

| Model String                           | Description                                 |
|----------------------------------------|---------------------------------------------|
| `openai/o3`                            | OpenAI's o3 (default)                       |
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
