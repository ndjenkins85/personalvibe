# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Tests for the generic retry_engine (Chunk A)."""

from __future__ import annotations

import builtins
from types import SimpleNamespace

import pytest

from personalvibe.retry_engine import RetryError, run_with_retries


def test_success_first_try():
    calls = {"n": 0}

    def _ok():
        calls["n"] += 1
        return True

    assert run_with_retries(_ok, max_retries=3) is True
    assert calls["n"] == 1  # short-circuited


def test_eventual_success(monkeypatch):
    seq = iter([False, False, True])
    calls = {"n": 0}

    def _sometimes():
        calls["n"] += 1
        return next(seq)

    assert run_with_retries(_sometimes, max_retries=5) is True
    assert calls["n"] == 3


def test_permanent_failure_triggers_rollback(monkeypatch):
    # --- stub out _rollback_branch so we don't touch git --------------
    recorded = SimpleNamespace(called=False)

    def _fake_rollback(branch):
        recorded.called = branch

    monkeypatch.setattr("personalvibe.retry_engine._rollback_branch", _fake_rollback)

    def _always_false():
        return False

    with pytest.raises(RetryError):
        run_with_retries(_always_false, max_retries=2, branch_name="vibed/0.0.1")

    assert recorded.called == "vibed/0.0.1"
