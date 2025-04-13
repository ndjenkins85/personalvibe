# Personal vibe

This repo is my personal practice at 'vibe coding' style.

I have several ideas which involve generative AI elements, and this repo will act as a shared framework to build them out.

As a python programmer, I'll primarily use flask for backend.

* [Installation](#installation)
  * [Dependency and virtual environment management, library development and build with poetry](#dependency-and-virtual-environment-management-library-development-and-build-with-poetry)
  * [Code quality, testing, and generating documentation with Nox](#code-quality-testing-and-generating-documentation-with-nox)
  * [Code formatting with Pre-commit](#code-formatting-with-pre-commit)
* [Running the webserver](#running-the-webserver)
* [Contributors](#contributors)

## Installation

The following are the setup instructions for installing the codebase locally to continue development.
Follow each step here and ensure tests are working.

### Python

This project uses Python 3.12

### Dependency and virtual environment management, library development and build with poetry

Ensure you have and installation of Poetry `2.1.1` or above, along with poetry-version-plugin.

Also add the following extras:

```bash
poetry self add poetry-plugin-shell
poetry self add poetry-plugin-export
```

Set preference for in-project virtual environment
```bash
poetry config virtualenvs.in-project true
```

Make sure you deactivate any existing virtual environments (i.e. conda).

```bash
poetry install
```

You may need to point poetry to the correct python interpreter using the following command.
In another terminal and in conda, run `which python`.
```bash
poetry env use /path/to/python3
```

Library can be built using

```bash
poetry build
```

### Code quality, testing, and generating documentation with Nox

Nox is a python task automation tool similar to Tox, Makefiles or scripts.

The following command can be used to run mypy, lint, and tests.
It is recommended to run these before pushing code, as this is run with Github Actions.
Some checks such as black are run more frequently with [pre-commit](#installing-pre-commit).

```bash
poetry run nox
```

Local Sphinx documentation can be generated with the following command.
Documentation publishing using Github Actions to Github pages is enabled by default.

```bash
poetry run nox -s docs
```

All other task automations commands can be optionally run locally with below command.

```bash
poetry run nox -s black safety pytype typeguard coverage xdoctest autoflake
```

### Code formatting with Pre-commit

On first time use of the repository, pre-commit will need to be installed locally.
You can use the following command to install and run pre-commit over all files.
See .pre-commit-config.yaml for checks in use.
Intention is to have lightweight checks that automatically make code changes.

``` bash
pre-commit run --all-files
```

## Running the webserver

### Local webserver

After following above instructions to use poetry environment, view website locally with following command:

``` bash
python run.py
...
 * Serving Flask app 'personalvibe' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Visit [localhost](http://127.0.0.1:5000) on browser.

## Contributors

* [Nick Jenkins](https://www.ndjenkins.com) - Data Scientist, API & Web dev, Team lead, Writer

See [CONTRIBUTING.md](CONTRIBUTING.md) in Github repo for specific instructions on contributing to project.

Usage rights governed by [LICENSE](LICENSE)  in Github repo or page footer.
