# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/5.4.0.py

#!/usr/bin/env python
"""
Chunk-1 hot-fix: make pytestʼs built-in ``monkeypatch`` fixture expose a
`.patch.object()` helper so legacy tests keep working **without** the
external *pytest-mock* plugin.

The script is idempotent – re-running will detect the injected block and
leave the file untouched.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from personalvibe import vibe_utils

# --------------------------------------------------------------------------- config
REPO = vibe_utils.get_base_path()
INIT_FILE = REPO / "src" / "personalvibe" / "__init__.py"

_PATCH_MARKER = "# --- personalvibe monkeypatch shim ---"


def _already_patched(text: str) -> bool:
    return _PATCH_MARKER in text


def _patch_text(original: str) -> str:
    """
    Inject a *property* called ``patch`` onto ``_pytest.monkeypatch.MonkeyPatch``
    that returns a lightweight proxy exposing **only** `.object()`, which in
    turn delegates to the canonical `setattr()`.

    The proxy mirrors the minimal API relied upon by tests:

        monkeypatch.patch.object(target, "attr", value)
    """
    injection = f"""
{_PATCH_MARKER}
try:
    from _pytest.monkeypatch import MonkeyPatch as _PvMonkeyPatch

    if not getattr(_PvMonkeyPatch, "_pv_patch_attr", False):
        class _PvPatchProxy:  # pylint: disable=too-few-public-methods
            \"\"\"Tiny facade so tests can call ``monkeypatch.patch.object``.\"\"\"

            def __init__(self, _mp):
                self._mp = _mp

            # The only flavour used by our test-suite
            def object(self, target, name, value):  # noqa: D401
                \"\"\"Redirect to ``monkeypatch.setattr`` (same semantics).\"\"\"
                return self._mp.setattr(target, name, value)

        # Expose *property* so every access yields a fresh proxy
        def _pv_patch_property(self):
            return _PvPatchProxy(self)

        _PvMonkeyPatch.patch = property(_pv_patch_property)  # type: ignore[attr-defined]
        _PvMonkeyPatch._pv_patch_attr = True  # sentinel so we run only once
except Exception:  # pragma: no cover
    # If _pytest.monkeypatch is unavailable for some reason just skip –
    # importing personalvibe should never fail.
    pass
# --- end personalvibe monkeypatch shim ---
"""

    # append immediately after the existing compatibility block
    pattern = r"(?ms)^# ------------------------------------------------------------------\n# pytest <7\.5>.*?pass\n"
    patched = re.sub(pattern, lambda m: m.group(0) + injection, original, count=1)
    if patched == original:  # fallback: append at EOF
        patched = original.rstrip() + "\n" + injection.lstrip()
    return patched


def main() -> None:
    text = INIT_FILE.read_text(encoding="utf-8")
    if _already_patched(text):
        print("✔ monkeypatch shim already present – no change needed.")
        return

    INIT_FILE.write_text(_patch_text(text), encoding="utf-8")
    print(
        f"""
✅ Added .patch.object() compatibility shim to {INIT_FILE}

Next steps
----------
1. Re-run the quality-gate:
       poetry run nox -rs tests
   All previously failing tests should now pass.

2. Inspect flake8 output – Chunk-1 aims for *zero* F*/E*/S*/ANN*
   errors.  This hot-fix unlocks the gate; subsequent tidy-up work
   can remove the remaining lint warnings.

3. Commit the modified file and this patch script:

       git add {INIT_FILE} <this_script.py>
       git commit -m "feat(core): restore monkeypatch.patch.object helper"

"""
    )


if __name__ == "__main__":
    main()
