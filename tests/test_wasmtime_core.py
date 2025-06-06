# Copyright © 2025 by Nick Jenkins. All rights reserved

"""Tests for Wasmtime core integration."""

import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from personalvibe.wasmtime_core import (
    WasmtimeBinaryNotFoundError,
    WasmtimeCore,
    WasmtimeExecutionError,
    execute_python_in_sandbox,
    get_wasmtime_core,
    wasmtime_smoke_test,
)


def test_wasmtime_core_init():
    """Test WasmtimeCore initialization."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        core = WasmtimeCore(tmp_dir)
        assert core.workspace_dir.exists()
        assert core.workspace_dir.name.endswith("personalvibe_wasmtime")


def test_get_platform_identifier():
    """Test platform identifier generation."""
    core = WasmtimeCore()
    platform_id = core.get_platform_identifier()
    assert isinstance(platform_id, str)
    assert "-" in platform_id
    # Should be something like darwin-aarch64, linux-x86_64, etc.


@patch("subprocess.run")
def test_initialize_sandbox_success(mock_run):
    """Test successful sandbox initialization."""
    mock_run.return_value = MagicMock(returncode=0, stdout="Wasmtime version info", stderr="")

    with tempfile.TemporaryDirectory() as tmp_dir:
        core = WasmtimeCore(tmp_dir)

        # Mock the binary detection to avoid resource loading
        mock_binary = Path(tmp_dir) / "wasmtime"
        mock_binary.touch()
        mock_binary.chmod(0o755)
        core._wasmtime_binary = mock_binary

        result = core.initialize_sandbox("print('hello')")

        assert result["exit_code"] == 0
        assert "stdout" in result
        assert "stderr" in result
        assert result["python_code"] == "print('hello')"


@patch("subprocess.run")
def test_initialize_sandbox_timeout(mock_run):
    """Test sandbox timeout handling."""
    mock_run.side_effect = subprocess.TimeoutExpired("wasmtime", 1)

    with tempfile.TemporaryDirectory() as tmp_dir:
        core = WasmtimeCore(tmp_dir)

        # Mock binary
        mock_binary = Path(tmp_dir) / "wasmtime"
        mock_binary.touch()
        mock_binary.chmod(0o755)
        core._wasmtime_binary = mock_binary

        with pytest.raises(WasmtimeExecutionError, match="timed out"):
            core.initialize_sandbox("print('hello')", timeout=1)


def test_detect_wasmtime_binary_system_fallback(monkeypatch):
    """Test fallback to system wasmtime binary."""

    # Mock importlib.resources to fail
    def mock_files_fail(*args):
        raise FileNotFoundError("Package resource not found")

    monkeypatch.setattr("importlib.resources.files", mock_files_fail)

    # Mock shutil.which to return a fake path
    fake_wasmtime = "/usr/bin/wasmtime"
    monkeypatch.setattr("shutil.which", lambda x: fake_wasmtime if x == "wasmtime" else None)

    with tempfile.TemporaryDirectory() as tmp_dir:
        core = WasmtimeCore(tmp_dir)
        result = core.detect_wasmtime_binary()
        assert str(result) == fake_wasmtime


def test_detect_wasmtime_binary_not_found(monkeypatch):
    """Test exception when wasmtime binary cannot be found."""

    # Mock both package resources and system binary to fail
    def mock_files_fail(*args):
        raise FileNotFoundError("Package resource not found")

    monkeypatch.setattr("importlib.resources.files", mock_files_fail)
    monkeypatch.setattr("shutil.which", lambda x: None)

    with tempfile.TemporaryDirectory() as tmp_dir:
        core = WasmtimeCore(tmp_dir)
        with pytest.raises(WasmtimeBinaryNotFoundError):
            core.detect_wasmtime_binary()


@patch("subprocess.run")
def test_smoke_test_success(mock_run):
    """Test successful smoke test."""
    mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")

    with tempfile.TemporaryDirectory() as tmp_dir:
        core = WasmtimeCore(tmp_dir)

        # Mock binary
        mock_binary = Path(tmp_dir) / "wasmtime"
        mock_binary.touch()
        mock_binary.chmod(0o755)
        core._wasmtime_binary = mock_binary

        assert core.smoke_test() is True


@patch("subprocess.run")
def test_smoke_test_failure(mock_run):
    """Test smoke test failure handling."""
    mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="error")

    with tempfile.TemporaryDirectory() as tmp_dir:
        core = WasmtimeCore(tmp_dir)

        # Mock binary
        mock_binary = Path(tmp_dir) / "wasmtime"
        mock_binary.touch()
        mock_binary.chmod(0o755)
        core._wasmtime_binary = mock_binary

        assert core.smoke_test() is False


def test_cleanup():
    """Test workspace cleanup."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        workspace_parent = Path(tmp_dir)
        core = WasmtimeCore(workspace_parent / "test_workspace")

        # Ensure workspace exists
        assert core.workspace_dir.exists()

        # Add some test data
        test_file = core.workspace_dir / "test.txt"
        test_file.write_text("test")

        core.cleanup()

        # Workspace should be cleaned up
        assert not core.workspace_dir.exists()
        assert core._wasmtime_binary is None
        assert len(core._extracted_binaries) == 0


@patch("personalvibe.wasmtime_core.get_wasmtime_core")
def test_convenience_functions(mock_get_core):
    """Test convenience functions."""
    mock_core = MagicMock()
    mock_core.initialize_sandbox.return_value = {"exit_code": 0}
    mock_core.smoke_test.return_value = True
    mock_get_core.return_value = mock_core

    # Test execute_python_in_sandbox
    result = execute_python_in_sandbox("print('test')")
    assert result["exit_code"] == 0
    mock_core.cleanup.assert_called_once()

    # Reset mock
    mock_core.reset_mock()

    # Test wasmtime_smoke_test
    assert wasmtime_smoke_test() is True
    mock_core.smoke_test.assert_called_once()
    mock_core.cleanup.assert_called_once()


# Only supporting MacOS at this time
# class TestPlatformSpecifics:
#     """Test platform-specific functionality."""

#     def test_platform_normalization(self, monkeypatch):
#         """Test platform identifier normalization."""
#         test_cases = [
#             ("Darwin", "arm64", "darwin-aarch64"),
#             ("Linux", "x86_64", "linux-x86_64"),
#             ("Linux", "amd64", "linux-x86_64"),
#             ("Windows", "AMD64", "windows-x86_64"),
#         ]

#         for system, machine, expected in test_cases:
#             monkeypatch.setattr("platform.system", lambda: system)
#             monkeypatch.setattr("platform.machine", lambda: machine)

#             core = WasmtimeCore()
#             assert core.get_platform_identifier() == expected
