# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Personalvibe Command-Line Interface (Chunk A).

After `poetry install`, a console-script named ``pv`` is available:

    pv milestone --config path/to/1.2.3.yaml --verbosity verbose
    pv sprint    --config cfg.yaml --prompt_only
    pv validate  --config cfg.yaml

Internally this is just a *thin* wrapper that forwards options to
:pyfunc:`personalvibe.run_pipeline.main`.
"""

from __future__ import annotations

import argparse
import sys
from typing import List


# Deferred import so we can monkey-patch ``sys.argv`` before the module’s
# global-level argparse in run_pipeline is evaluated.
def _forward_to_run_pipeline(argv: List[str]) -> None:
    sys.argv = ["personalvibe.run_pipeline"] + argv  # pretend we’re the module
    from personalvibe import run_pipeline  # local import

    run_pipeline.main()


def cli_main() -> None:  # entry-point impl
    parser = argparse.ArgumentParser(prog="pv", description="Personalvibe CLI")
    sub = parser.add_subparsers(
        dest="mode", required=True, metavar="<mode>", help="Operation mode (yaml's 'mode' key should match)."
    )

    def _add_common(p):
        p.add_argument("--config", required=True, help="Path to YAML config file.")
        p.add_argument("--verbosity", choices=["verbose", "none", "errors"], default="none")
        p.add_argument("--prompt_only", action="store_true")
        p.add_argument("--max_retries", type=int, default=5)

    for _mode in ("prd", "milestone", "sprint", "validate"):
        _add_common(sub.add_parser(_mode, help=f"{_mode} flow"))

    args = parser.parse_args()
    forwarded = [
        "--config",
        args.config,
        "--verbosity",
        args.verbosity,
    ]
    if args.prompt_only:
        forwarded.append("--prompt_only")
    if args.max_retries != 5:
        forwarded += ["--max_retries", str(args.max_retries)]

    _forward_to_run_pipeline(forwarded)


# The entry-point declared in pyproject.toml
def app() -> None:  # noqa: D401
    """Poetry console-script shim."""
    cli_main()


if __name__ == "__main__":  # pragma: no cover
    cli_main()
