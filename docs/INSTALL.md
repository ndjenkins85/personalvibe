# Installation – Personalvibe 2.1

```bash
pip install --upgrade personalvibe
```

A console-script **`pv`** appears on your `$PATH` afterwards.

```bash
pv --help
pv run --config my_config.yaml
```

Runtime artefacts are created in the **current working directory**:

```
.
├─ data/<project>/prompt_inputs/
├─ data/<project>/prompt_outputs/
└─ logs/<semver>_base.log
```

Override the workspace root via:

```bash
export PV_DATA_DIR=/absolute/path/to/workspace
```
