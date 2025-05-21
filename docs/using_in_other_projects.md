# Using **Personalvibe** in *other* projects

This guide walks you through installing the published wheel, running the
CLI, and – for front-end tinkerers – the first steps towards a later
Single-Page-App (SPA) integration.

---

## Quick start (Python workflow)

# 1) Install from PyPI (recommended)
pip install personalvibe

# 2) Scaffold a data workspace somewhere **outside** the source checkout
export PV_DATA_DIR=$(pwd)/.pv_workspace     # optional, defaults to CWD

# 3) Run the milestone analysis of YOUR yaml config
pv milestone --config path/to/1.0.0.yaml --verbosity verbose

What happened?

1. The `pv` console-script parsed your YAML and resolved a *workspace*
   at `$PV_DATA_DIR` (or current directory).
2. Logs are streamed to `logs/<semver>_base.log`.
3. All prompt inputs/outputs are persisted under
   `data/<project>/prompt_*`.

---

## Environment variables

| Variable      | Purpose                                     | Default        |
|---------------|---------------------------------------------|----------------|
| `PV_DATA_DIR` | Override the workspace root directory       | `Path.cwd()`   |
| `OPENAI_API_KEY` | Passed straight through to the *OpenAI* SDK | *(required)* |

---

## Transparency reporting (example flow)

Below is an end-to-end snippet you can paste into your project’s CI:

set -e
poetry add --group dev personalvibe
pv milestone --config prompts/myproj/configs/2.0.0.yaml
pv sprint    --config prompts/myproj/configs/2.0.0.yaml --verbosity verbose
pv validate  --config prompts/myproj/configs/2.0.0.yaml

The trio ensures every step appends to the same `logs/2.0.0_base.log`,
making **audit trails** trivial.

---

## SPA placeholder 🍿

Personalvibe’s back-end is framework-agnostic, but future sprints will
expose a small JSON API.  If you already use a front-end stack, keep the
following directory layout ready:

my-project/
└─ web/
   ├─ package.json   # will list @personalvibe/sdk once published
   └─ src/
        App.tsx

Initial NPM bootstrap (React example):

cd web
npm create vite@latest  .
npm install
npm run dev

**No SDK is required yet** – this is merely a sandbox for upcoming
experiments.

---

Happy vibecoding!  — *The Personalvibe team*
