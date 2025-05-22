# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/4.2.0.py

"""
patch_fix_log_to.py

Applies a surgical hot-patch to **noxfile.py** so that its `_log_to`
context-manager closes the duplicate *TextIOWrapper*s (`new_stdout`,
`new_stderr`).  Without that close the wrappers still hold an open file
descriptor to the pipe which keeps the spawned `tee -a` process alive
forever – pytest then appears to **hang** at
tests/test_log_to_cm.py.

This script:
1. Locates the final “FIXED _log_to IMPLEMENTATION” block.
2. Replaces it with a corrected version that:

   • flushes *and then closes* the wrappers before waiting on `tee`.
   • uses explicit variable names to avoid confusion.

After running the script the test-suite should progress past
`tests/test_log_to_cm.py` without blocking.
"""
from __future__ import annotations

import re
from pathlib import Path

# ----------------------------------------------------------------------
# 1) Locate repo root (works from any cwd)
# ----------------------------------------------------------------------
from personalvibe import vibe_utils

REPO = vibe_utils.get_base_path()  # mono-repo root even when called elsewhere
noxfile_path = REPO / "noxfile.py"

if not noxfile_path.exists():
    raise FileNotFoundError(f"Expected noxfile at {noxfile_path}")

src = noxfile_path.read_text(encoding="utf-8")

# ----------------------------------------------------------------------
# 2) Build replacement _log_to implementation
# ----------------------------------------------------------------------
NEW_IMPL = '''
@contextmanager
def _log_to(path: Path):  # type: ignore[override]
    """
    Duplicate *all* stdout / stderr – including child-process output – to
    ``path`` **in append mode** without dead-locking.

    Key fix:
        Close the per-context TextIOWrapper duplicates **before** waiting
        on the underlying ``tee`` process so that the pipe write-end is
        fully closed (otherwise tee never terminates and pytest hangs).
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

    # Spawn persistent tee (-a so we append)
    tee_proc = subprocess.Popen(
        ["tee", "-a", str(path)],
        stdin=subprocess.PIPE,
        text=False,          # binary FD handing
    )
    if tee_proc.stdin is None:                          # pragma: no cover
        raise RuntimeError("tee failed to provide stdin")

    tee_fd = tee_proc.stdin.fileno()

    # Save original low-level fds
    saved_out_fd = os.dup(1)
    saved_err_fd = os.dup(2)

    # Route fd1/fd2 to tee
    os.dup2(tee_fd, 1)
    os.dup2(tee_fd, 2)

    # High-level Python objects (wrappers around *new* duped fds)
    saved_stdout_obj, saved_stderr_obj = sys.stdout, sys.stderr
    wrapper_stdout = io.TextIOWrapper(os.fdopen(os.dup(1), 'wb'), encoding='utf-8', line_buffering=True)
    wrapper_stderr = io.TextIOWrapper(os.fdopen(os.dup(2), 'wb'), encoding='utf-8', line_buffering=True)
    sys.stdout, sys.stderr = wrapper_stdout, wrapper_stderr

    try:
        yield
    finally:
        # Flush & CLOSE wrappers so no fd points to the pipe afterwards
        try:
            wrapper_stdout.flush()
            wrapper_stderr.flush()
        finally:
            wrapper_stdout.close()
            wrapper_stderr.close()

        # Restore original low-level fds
        os.dup2(saved_out_fd, 1)
        os.dup2(saved_err_fd, 2)
        os.close(saved_out_fd)
        os.close(saved_err_fd)

        # Close tee stdin and wait for it to finish writing
        tee_proc.stdin.close()
        tee_proc.wait()

        # Restore original Python objects
        sys.stdout, sys.stderr = saved_stdout_obj, saved_stderr_obj
'''

# ----------------------------------------------------------------------
# 3) Replace the existing final implementation block
#    (everything from '# --- FIXED _log_to IMPLEMENTATION ---' to
#     '# --- END FIXED _log_to IMPLEMENTATION ---')
# ----------------------------------------------------------------------
pattern = re.compile(
    r"# --- FIXED _log_to IMPLEMENTATION ---.*?# --- END FIXED _log_to IMPLEMENTATION ---",
    re.DOTALL,
)
if not pattern.search(src):
    raise RuntimeError("Unable to find the FIXED _log_to IMPLEMENTATION markers in noxfile.py")

patched = pattern.sub(
    f"# --- FIXED _log_to IMPLEMENTATION ---{NEW_IMPL}\n# --- END FIXED _log_to IMPLEMENTATION ---", src, count=1
)

noxfile_path.write_text(patched, encoding="utf-8")
print(f"✅  Patched _log_to implementation in {noxfile_path}")

print(
    """
Next steps
----------
1. Re-run the test-suite:

   bash tests/personalvibe.sh

   or

   poetry run nox -s tests

2. All tests – especially tests/test_log_to_cm.py – should now complete
   successfully without hanging.
"""
)
