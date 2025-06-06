# Wasmtime Integration

Personalvibe includes integrated support for running code in isolated WebAssembly sandboxes using Wasmtime.

## Overview

The Wasmtime integration provides:

- Cross-platform binary detection and loading
- Hermetic sandbox environments for code execution
- Python-WASI environment setup
- Automated testing support with timeout and error handling

## Basic Usage

```python
from personalvibe.wasmtime_core import execute_python_in_sandbox, wasmtime_smoke_test

# Execute Python code in sandbox
result = execute_python_in_sandbox("""
print("Hello from sandbox!")
x = 2 + 2
print(f"2 + 2 = {x}")
""")

print(f"Exit code: {result['exit_code']}")
print(f"Output: {result['stdout']}")

# Run smoke test
if wasmtime_smoke_test():
    print("Wasmtime integration working correctly")
```

## Advanced Usage

```python
from personalvibe.wasmtime_core import WasmtimeCore

# Create core instance with custom workspace
core = WasmtimeCore("/tmp/my_sandbox")

try:
    # Execute code with custom timeout
    result = core.initialize_sandbox(
        python_code="import time; time.sleep(1); print('done')",
        timeout=5
    )

    if result["exit_code"] == 0:
        print("Execution successful")
    else:
        print(f"Execution failed: {result['stderr']}")

finally:
    # Always cleanup
    core.cleanup()
```

## Platform Support

The integration automatically detects the platform and loads the appropriate Wasmtime binary:

- macOS (Intel/Apple Silicon)
- Linux (x86_64/ARM64)
- Windows (x86_64)

## Binary Management

Wasmtime binaries are bundled with the package and automatically extracted to a temporary workspace.
If package binaries are not available, the system will fallback to using a globally installed `wasmtime` binary.

## Error Handling

The integration provides specific exception types:

- `WasmtimeBinaryNotFoundError`: When binary cannot be found or extracted
- `WasmtimeExecutionError`: When execution fails or times out

## Testing

Run the test suite to verify integration:

```bash
pytest tests/test_wasmtime_core.py -v
```

## Requirements

- Python 3.9+
- Wasmtime binary (bundled or system-installed)
- Temporary filesystem access for workspace
