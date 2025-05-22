# Using Personalvibe in *your* project

## 1 – Install

```bash
poetry add personalvibe    # or  pip install personalvibe
```

## 2 – Create a YAML config

```yaml
# 1.0.0.yaml
project_name: my_cool_idea
mode: milestone         # prd | milestone | sprint | validate
execution_details: ''
code_context_paths: []  # optional snippets fed into the prompt
```

## 3 – Run

```bash
pv run --config 1.0.0.yaml --prompt_only   # preview
pv run --config 1.0.0.yaml                 # full run
```

## Advanced

• Persist artefacts in a separate folder:

  `PV_DATA_DIR=.pv_workspace pv sprint --config 1.0.0.yaml`

• Extract the last assistant code block and run it:

  `pv parse-stage --project_name my_cool_idea --run`

---

*Happy vibecoding!*  — The Personalvibe team
