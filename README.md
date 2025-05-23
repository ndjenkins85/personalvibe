# Personalvibe


## Documentation quick links

* [Installation](docs/INSTALL.md)
* [Developer on-boarding](docs/ONBOARDING.md)
* [Using Personalvibe *in other projects*](docs/using_in_other_projects.md)
* [API reference](docs/reference.rst)
* [Roadmap 3.0.0](docs/roadmap/3.0.0_milestone.md)

---

Personalvibe is my own attempt at bootstrapping and building an AI interface into my code approach.

*Brainstorm → YAML → Prompt → Code → Test*
Personalvibe turns AI tinkering into a **repeatable pipeline**
you can embed in *any* project.

```text
pip install personalvibe        # 🚀  get the CLI
pv run --config 1.0.0.yaml      # 🤖  generate / execute prompts
```

---
## Why “vibe coding” ?
Traditional scaffolding tools expect you to know the end-state.
But early-stage ideas are fuzzy, iterations rapid.
Personalvibe embraces this *uncertainty*:

• prompts live beside your source code (version controlled)
• every run writes human-readable logs in `./logs`
• unit tests guard each sprint so automation stays trustworthy

---
## Quick start (2 mins)

1. `pip install personalvibe`
2. `pv run --config examples/hello_world.yaml --prompt_only`
   → renders a prompt, saves it under `data/<project>/prompt_inputs/`
3. fill in your OpenAI key, drop the `--prompt_only` flag, re-run.

---
## CLI overview

| command        | purpose                                   |
|----------------|-------------------------------------------|
| `pv run`       | auto-detect mode from YAML & execute      |
| `pv milestone` | ask the LLM for a milestone plan          |
| `pv sprint`    | generate a sprint chunk (≤20 k chars)     |
| `pv validate`  | re-run lint/tests inside a one-liner gate |
| `pv parse-stage` | save last assistant *code* block to file|

Append `--help` to any sub-command for details.

---
## Development setup (optional)

```bash
poetry install         # installs dev + lint + test groups
poetry run nox         # black, flake8, mypy, pytest, smoke_dist
./tests/personalvibe.sh   # the same quality-gate in one shell
```

---
## License & acknowledgements
MIT.
Made with ❤️  and too much coffee by Nick Jenkins.
Inspired by dozens of open-source LLM projects — thank you!
