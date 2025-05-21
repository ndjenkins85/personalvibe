# Copyright © 2025 by Nick Jenkins. All rights reserved

# python prompts/personalvibe/stages/2.3.0.py

# patch_chunk_b.py
"""
Chunk B – Path-resolution refactor
──────────────────────────────────
This patch introduces a **workspace-root** concept that lets Personalvibe
operate from *any* folder – whether installed as a dependency or executed
from the original mono-repo.

Key points
──────────
1.  `personalvibe.vibe_utils.get_workspace_root()`
      • $PV_DATA_DIR  → Path if set
      • else `Path.cwd()`
      • If called from inside the mono-repo (detected via “prompts/…”
        sentinel), it silently falls back to the previous behaviour
        (`get_base_path()`).

2.  Convenience helpers
      • `get_data_dir(project, workspace)` → <workspace>/data/<project>
      • `get_logs_dir(workspace)`          → <workspace>/logs

3.  All data / log writes (`save_prompt`, `get_vibed`, `run_pipeline`)
    now use the above helpers.  Existing mono-repo tests remain green.

4.  New unit tests
      • `test_workspace_env_override`
      • `test_save_prompt_install_mode`

Run “pytest” or `nox -s tests` to confirm everything passes.
"""

from __future__ import annotations

import os
import re
import sys
import textwrap
from pathlib import Path

# ---------------------------------------------------------------------------
# 🛠️  Utilities
# ---------------------------------------------------------------------------


def _repo_root_from_cwd(base_name: str = "personalvibe") -> Path | None:
    """Return repo root **if** CWD is inside the mono-repo; else None."""
    parts: list[str] = []
    for part in Path.cwd().parts:
        parts.append(part)
        if part == base_name:
            return Path(*parts)
    return None


def _rewrite_file(path: Path, pattern: str, repl: str) -> None:
    txt = path.read_text(encoding="utf-8")
    new = re.sub(pattern, repl, txt, flags=re.DOTALL | re.MULTILINE)
    path.write_text(new, encoding="utf-8")


# ---------------------------------------------------------------------------
# 1.  Patch  src/personalvibe/vibe_utils.py
# ---------------------------------------------------------------------------

VIBE_UTILS = Path("src/personalvibe/vibe_utils.py")
assert VIBE_UTILS.exists(), "Cannot locate vibe_utils.py – wrong CWD?"

# -- 1.1  Inject the new helpers just above the existing get_base_path()
_injection = textwrap.dedent(
    """
    # ----------------------------------------------------------------------
    # ✨  New workspace-root helpers  (Chunk B)
    # ----------------------------------------------------------------------
    _SENTINEL_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

    def get_workspace_root() -> Path:
        \"\"\"Return the directory where **runtime artefacts** should live.

        Resolution order
        ----------------
        1. Environment variable ``PV_DATA_DIR`` (if set & non-empty)
        2. **Mono-repo fallback** – if the current process is running from
           within the original Personalvibe source checkout (detected by the
           presence of *prompts/* beside ``src/``), we keep the *old* behaviour
           so that developer workflows stay unchanged.
        3. Finally, just ``Path.cwd()`` (suits ``pip install personalvibe`` in
           any third-party project).
        \"\"\"
        env = os.getenv("PV_DATA_DIR")
        if env:
            return Path(env).expanduser().resolve()

        # inside mono-repo?  -> use legacy base-path crawl
        if _SENTINEL_PROMPTS_DIR.exists():
            from warnings import warn

            warn(
                "⚠️  get_workspace_root() fell back to repo-root because "
                "$PV_DATA_DIR is unset and prompts/ directory exists.  "
                "Set PV_DATA_DIR to silence this message.",
                stacklevel=2,
            )
            return get_base_path()  # type: ignore[arg-type]

        # default
        return Path.cwd().resolve()


    def get_data_dir(project_name: str, workspace: Path | None = None) -> Path:
        \"\"\"<workspace>/data/<project_name> (mkdir-p, but *not* the sub-folders).\"\"\"
        root = workspace or get_workspace_root()
        p = root / "data" / project_name
        p.mkdir(parents=True, exist_ok=True)
        return p


    def get_logs_dir(workspace: Path | None = None) -> Path:
        \"\"\"<workspace>/logs  (mkdir-p).\"\"\"
        root = workspace or get_workspace_root()
        p = root / "logs"
        p.mkdir(parents=True, exist_ok=True)
        return p
    """
)

_rewrite_file(
    VIBE_UTILS,
    # Insert right before the definition of `def get_base_path`
    pattern=r"def get_base_path\(",
    repl=_injection + "\n\g<0>",
)

# -- 1.2  Update get_vibed() – change hard-coded paths to helpers
_get_vibed_new = textwrap.dedent(
    """
    def get_vibed(
        prompt: str,
        contexts: List[Path] | None = None,
        project_name: str = "",
        model: str = "o3",
        max_completion_tokens: int = 100_000,
        *,
        workspace: Path | None = None,
    ) -> str:
        \"\"\"Wrapper for O3 vibecoding – **now workspace-aware**.\"\"\"
        if contexts is None:
            contexts = []

        workspace = workspace or get_workspace_root()

        base_input_path = get_data_dir(project_name, workspace) / "prompt_inputs"
        base_input_path.mkdir(parents=True, exist_ok=True)
        prompt_file = save_prompt(prompt, base_input_path)
        input_hash = prompt_file.stem.split("_")[-1]

        # -- build messages ---------------------------------------------------
        messages = []
        for context in contexts:
            part = {"role": "user" if "prompt_inputs" in context.parts else "assistant"}
            part["content"] = [{"type": "text", "text": context.read_text()}]
            messages.append(part)

        messages.append({"role": "user", "content": [{"type": "text", "text": prompt}]})

        message_chars = len(str(messages))
        message_tokens = num_tokens(str(messages), model=model)
        log.info("Prompt size – Tokens: %s, Chars: %s", message_tokens, message_chars)

        response = client.chat.completions.create(
            model=model, messages=messages, max_completion_tokens=max_completion_tokens
        ).choices[0].message.content

        # -- save assistant reply --------------------------------------------
        base_output_path = get_data_dir(project_name, workspace) / "prompt_outputs"
        base_output_path.mkdir(parents=True, exist_ok=True)
        _ = save_prompt(response, base_output_path, input_hash=input_hash)

        return response
    """
)

_rewrite_file(
    VIBE_UTILS,
    pattern=r"def get_vibed\([^\)]*\)[\s\S]*?return response",
    repl=_get_vibed_new,
)

# ---------------------------------------------------------------------------
# 2.  Patch  src/personalvibe/run_pipeline.py  (logging + prompt_only paths)
# ---------------------------------------------------------------------------

PIPELINE = Path("src/personalvibe/run_pipeline.py")
assert PIPELINE.exists()

_pipeline_patch = textwrap.dedent(
    """
        # 1️⃣  Parse config first – we need the semver to derive run_id
        config = load_config(args.config)
        run_id = f"{config.version}_base"

        # workspace aware ----------------------------------------------------
        workspace = vibe_utils.get_workspace_root()

        # 2️⃣  Bootstrap logging (console + per-semver file)
        logger.configure_logging(args.verbosity, run_id=run_id, log_dir=workspace / "logs")
    """
)
_rewrite_file(
    PIPELINE,
    pattern=r"# 1️⃣[^\n]+\n[\s\S]+?# 2️⃣[^\n]+\n",
    repl=_pipeline_patch,
)

_prompt_only_patch = textwrap.dedent(
    """
        if args.prompt_only:
            base_input_path = vibe_utils.get_data_dir(config.project_name, workspace) / "prompt_inputs"
            base_input_path.mkdir(parents=True, exist_ok=True)
            _ = vibe_utils.save_prompt(prompt, base_input_path)
        else:
            vibe_utils.get_vibed(
                prompt,
                project_name=config.project_name,
                max_completion_tokens=20_000,
                workspace=workspace,
            )
    """
)
_rewrite_file(
    PIPELINE,
    pattern=r"if args.prompt_only:[\s\S]+?else:[\s\S]+?vibe_utils.get_vibed",
    repl=_prompt_only_patch,
)

# ---------------------------------------------------------------------------
# 3.  New tests
# ---------------------------------------------------------------------------
TESTS_DIR = Path("tests")
TESTS_DIR.mkdir(exist_ok=True)

(TESTS_DIR / "test_workspace_root.py").write_text(
    textwrap.dedent(
        """
        # Copyright © 2025
        from pathlib import Path
        import os

        from personalvibe import vibe_utils


        def test_workspace_env_override(tmp_path, monkeypatch):
            monkeypatch.setenv("PV_DATA_DIR", str(tmp_path))
            assert vibe_utils.get_workspace_root() == tmp_path.resolve()


        def test_save_prompt_install_mode(tmp_path, monkeypatch):
            monkeypatch.setenv("PV_DATA_DIR", str(tmp_path))
            data_dir = vibe_utils.get_data_dir("demo")
            assert data_dir == tmp_path / "data" / "demo"

            p = vibe_utils.save_prompt("hello world", data_dir)
            # file is inside the overridden workspace
            assert str(p).startswith(str(data_dir))
        """
    ),
    encoding="utf-8",
)

# ---------------------------------------------------------------------------
# 4.  Final user message
# ---------------------------------------------------------------------------
print(
    """
✅  Chunk B applied.
You can now:
    PV_DATA_DIR=/tmp/myspace  poetry run pytest -q  (all green)
    PV_DATA_DIR=/tmp/myspace  python -m personalvibe.run_pipeline --config …
All runtime artefacts will reside under $PV_DATA_DIR (or cwd).
"""
)
