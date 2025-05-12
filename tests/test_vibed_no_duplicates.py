# Copyright © 2025 by Nick Jenkins. All rights reserved

import builtins
from contextlib import contextmanager

import pytest

import noxfile


class DummySession:
    """Mimics minimal `nox.sessions.Session` behaviour."""

    def __init__(self, posargs):
        self.posargs = posargs
        self.runs = []

    # nox`Session.run` signature is flexible – we ignore **kwargs
    def run(self, *cmd, **_):
        self.runs.append(cmd)

    def run_always(self, *cmd, **_):
        self.run(*cmd)

    def error(self, msg):
        raise RuntimeError(msg)


@contextmanager
def _noop_log_to(_):
    """Stub that bypasses `tee`, making stdout capturable."""
    yield


def test_vibed_prints_single_branch_banner(monkeypatch, capsys):
    # --- isolate side-effects -------------------------------------------------
    monkeypatch.setattr(noxfile, "_log_to", _noop_log_to, raising=True)

    session = DummySession(["0.0.2"])
    noxfile.vibed(session)

    captured = capsys.readouterr().out
    assert captured.count("Creating branch vibed/0.0.2") == 1, captured
