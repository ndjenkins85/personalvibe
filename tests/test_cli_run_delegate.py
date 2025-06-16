# Copyright © 2025 by Nick Jenkins. All rights reserved

# Copyright © 2025 by Nick Jenkins.
#
# Purpose: ensure `pv run` inspects YAML, routes to the correct
# specialised handler, and honours --raw-argv passthrough.
from __future__ import annotations

import types
from pathlib import Path
from unittest import mock

import personalvibe.cli as cli


def _tmp_cfg(tmp_path: Path, task: str) -> Path:
    cfg = tmp_path / f"{task}.yaml"
    cfg.write_text(
        f"""project_name: demo
task: {task}
user_instructions: ''
project_context_paths: []""",
        encoding="utf-8",
    )
    return cfg


def test_run_delegates_to_mode(monkeypatch, tmp_path):
    called = types.SimpleNamespace(args=None)

    def _fake_main():
        called.args = cli.sys.argv[1:]  # skip prog name

    monkeypatch.patch.object(cli.run_pipeline, "main", _fake_main)

    cfg = _tmp_cfg(tmp_path, "milestone")
    cli.cli_main(["run", "--config", str(cfg)])

    assert called.args is not None, "run_pipeline.main not invoked"
    # Should be same args as explicit 'pv milestone'
    assert "--config" in called.args
    assert str(cfg) in called.args


def test_run_raw_argv_passthrough(monkeypatch, tmp_path):
    captured = {}

    def _fake_main():
        captured["argv"] = cli.sys.argv[1:]

    monkeypatch.patch.object(cli.run_pipeline, "main", _fake_main)

    cfg = _tmp_cfg(tmp_path, "prd")
    cli.cli_main(
        [
            "run",
            "--config",
            str(cfg),
            "--raw-argv",
            "--config sentinel.yaml --verbosity verbose",
        ]
    )

    assert captured["argv"] == [
        "--config",
        "sentinel.yaml",
        "--verbosity",
        "verbose",
    ]
