# Copyright © 2025 by Nick Jenkins. All rights reserved
"""
Wasmtime Core Integration for Automated Testing.

Key features
------------
* Cross-platform Wasmtime binary detection and loading
* Minimal sandbox initialisation for Python-WASI environments
* Binary vendoring system for OS/CPU–specific Wasmtime builds
* Essential error handling for missing or incompatible binaries
"""

from __future__ import annotations

import importlib.resources
import logging
import os
import platform
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Union

__all__ = [
    "WasmtimeError",
    "WasmtimeBinaryNotFoundError",
    "WasmtimeExecutionError",
    "WasmtimeCore",
    "get_wasmtime_core",
    "execute_python_in_sandbox",
    "wasmtime_smoke_test",
]

_log: logging.Logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------#
# Exceptions
# ---------------------------------------------------------------------------#
class WasmtimeError(Exception):
    """Base exception for Wasmtime-related errors."""


class WasmtimeBinaryNotFoundError(WasmtimeError):
    """Raised when the Wasmtime binary cannot be found or extracted."""


class WasmtimeExecutionError(WasmtimeError):
    """Raised when Wasmtime execution fails."""


# ---------------------------------------------------------------------------#
# Core wrapper
# ---------------------------------------------------------------------------#
class WasmtimeCore:
    """
    Core Wasmtime integration for automated testing sandbox environments.

    Responsibilities
    ----------------
    * Platform-specific binary detection and extraction
    * Minimal sandbox initialisation
    * Python-WASI execution with timeout and error handling
    """

    def __init__(self: "WasmtimeCore", workspace_dir: Optional[Union[str, Path]] = None) -> None:
        """
        Parameters
        ----------
        workspace_dir:
            Directory used for temporary files and extraction.  Defaults to the
            system temp directory.
        """
        self.workspace_dir: Path = Path(workspace_dir or tempfile.gettempdir()) / "personalvibe_wasmtime"
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

        self._wasmtime_binary: Optional[Path] = None
        self._extracted_binaries: Dict[str, Path] = {}

    # ------------------------------------------------------------------#
    # Helpers
    # ------------------------------------------------------------------#
    def get_platform_identifier(self: "WasmtimeCore") -> str:
        """
        Returns
        -------
        str
            Platform string such as ``darwin-aarch64`` or ``linux-x86_64``.
        """
        system: str = platform.system().lower()
        machine: str = platform.machine().lower()

        # Normalise architecture names
        if machine in {"aarch64", "arm64"}:
            machine = "aarch64"
        elif machine in {"x86_64", "amd64"}:
            machine = "x86_64"
        elif machine.startswith("arm"):
            machine = "arm"

        return f"{system}-{machine}"

    # ------------------------------------------------------------------#
    # Binary discovery / extraction
    # ------------------------------------------------------------------#
    def detect_wasmtime_binary(self: "WasmtimeCore") -> Path:
        """
        Locate or extract the Wasmtime binary appropriate for this platform.

        Returns
        -------
        pathlib.Path
            Absolute path to an executable Wasmtime binary.

        Raises
        ------
        WasmtimeBinaryNotFoundError
            If the binary cannot be found or extracted.
        """
        # Cached?
        if self._wasmtime_binary and self._wasmtime_binary.exists():
            return self._wasmtime_binary

        platform_id: str = self.get_platform_identifier()
        binary_name: str = f"wasmtime-{platform_id}-min"

        # Already extracted in this run?
        cached_path: Optional[Path] = self._extracted_binaries.get(platform_id)
        if cached_path and cached_path.exists():
            self._wasmtime_binary = cached_path
            return cached_path

        # Try bundled resource first
        try:
            pkg_file = importlib.resources.files("personalvibe._bin").joinpath(binary_name)
            binary_data = pkg_file.read_bytes()

            extracted_path = self.workspace_dir / f"wasmtime-{platform_id}"
            extracted_path.write_bytes(binary_data)
            extracted_path.chmod(stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

            self._extracted_binaries[platform_id] = extracted_path
            self._wasmtime_binary = extracted_path
            _log.info("Extracted Wasmtime binary for %s to %s", platform_id, extracted_path)
            return extracted_path

        except Exception as exc:  # noqa: BLE001
            _log.debug("Bundled binary not available: %s", exc, exc_info=True)

        # Fallback: system PATH
        system_wasmtime: Optional[str] = shutil.which("wasmtime")
        if system_wasmtime:
            _log.info("Using system Wasmtime binary: %s", system_wasmtime)
            self._wasmtime_binary = Path(system_wasmtime)
            return self._wasmtime_binary

        raise WasmtimeBinaryNotFoundError(
            f"Wasmtime binary for platform '{platform_id}' not found in resources " "and not present on PATH."
        )

    # ------------------------------------------------------------------#
    # Sandbox execution
    # ------------------------------------------------------------------#
    def initialize_sandbox(
        self: "WasmtimeCore",
        python_code: str,
        timeout: int = 30,
    ) -> Dict[str, Any]:
        """
        Execute arbitrary Python source inside a minimal Wasmtime sandbox.

        Notes
        -----
        This demo implementation runs ``wasmtime --version`` because a full
        Python-in-WASI runtime is beyond scope here.  Replace ``cmd`` with an
        appropriate invocation once available.

        Parameters
        ----------
        python_code:
            Source code to (eventually) run inside the sandbox.
        timeout:
            Maximum seconds to allow the subprocess to run.

        Returns
        -------
        dict
            Keys: ``exit_code``, ``stdout``, ``stderr``, ``python_code``,
            ``workspace``.

        Raises
        ------
        WasmtimeExecutionError
            On subprocess failure or timeout.
        """
        wasmtime_binary = self.detect_wasmtime_binary()

        exec_workspace: Path = self.workspace_dir / f"exec_{os.getpid()}"
        exec_workspace.mkdir(exist_ok=True)

        try:
            (exec_workspace / "script.py").write_text(python_code, encoding="utf-8")

            cmd: list[str] = [str(wasmtime_binary), "--version"]
            _log.debug("Executing Wasmtime command: %s", " ".join(cmd))

            completed = subprocess.run(
                cmd,
                cwd=exec_workspace,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )

            result: Dict[str, Any] = {
                "exit_code": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "python_code": python_code,
                "workspace": str(exec_workspace),
            }

            if completed.returncode != 0:
                _log.warning("Wasmtime exited with %d; stderr:\n%s", completed.returncode, completed.stderr)
            else:
                _log.info("Wasmtime execution succeeded.")

            return result

        except subprocess.TimeoutExpired as exc:
            raise WasmtimeExecutionError(f"Wasmtime execution timed out after {timeout} s") from exc
        except Exception as exc:  # noqa: BLE001
            raise WasmtimeExecutionError(f"Wasmtime execution failed: {exc}") from exc
        finally:
            try:
                shutil.rmtree(exec_workspace)
            except Exception as exc:  # noqa: BLE001
                _log.warning("Failed to clean up workspace %s: %s", exec_workspace, exc)

    # ------------------------------------------------------------------#
    # Utilities
    # ------------------------------------------------------------------#
    def smoke_test(self: "WasmtimeCore") -> bool:
        """
        Quick binary sanity check.

        Returns
        -------
        bool
            ``True`` if the binary appears to work, else ``False``.
        """
        try:
            return self.initialize_sandbox("print('hello')")["exit_code"] == 0
        except WasmtimeError:
            return False

    def cleanup(self: "WasmtimeCore") -> None:
        """Remove any extracted binaries and temporary workspaces."""
        try:
            if self.workspace_dir.exists():
                shutil.rmtree(self.workspace_dir)
        finally:
            self._extracted_binaries.clear()
            self._wasmtime_binary = None


# ---------------------------------------------------------------------------#
# Convenience helpers
# ---------------------------------------------------------------------------#
def get_wasmtime_core(workspace_dir: Optional[Union[str, Path]] = None) -> WasmtimeCore:
    """Return a fresh :class:`WasmtimeCore` instance."""
    return WasmtimeCore(workspace_dir)


def execute_python_in_sandbox(python_code: str, timeout: int = 30) -> Dict[str, Any]:
    """
    Convenience wrapper around :py:meth:`WasmtimeCore.initialize_sandbox`.
    """
    core = get_wasmtime_core()
    try:
        return core.initialize_sandbox(python_code, timeout)
    finally:
        core.cleanup()


def wasmtime_smoke_test() -> bool:
    """
    Convenience wrapper around :py:meth:`WasmtimeCore.smoke_test`.
    """
    core = get_wasmtime_core()
    try:
        return core.smoke_test()
    finally:
        core.cleanup()
