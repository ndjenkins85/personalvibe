# Installation – Personalvibe 2.x

# Grab the latest stable release
pip install --upgrade personalvibe

A console-script `pv` will be available afterwards:

pv --help
pv milestone --config path/to/1.0.0.yaml

Runtime artefacts are created in the **current working directory**.
Override via:

export PV_DATA_DIR=/absolute/path/to/workspace
