# Cursor Rules: personalvibe-based AI Projects

This project uses **prompt-driven development** in Python, powered by a shared `personalvibe` core and modular applications for various interactive AI experiences. These rules guide Cursor's behavior when assisting with code generation, prompt writing, and system design.

---

## 🧱 Project Overview

This monorepo contains multiple LLM-powered applications, all built around a common framework (`personalvibe`) to handle:

- Audio recording and transcription
- Prompt templating with Jinja2
- OpenAI API interaction
- Image and TTS generation
- Agent memory and reasoning

Each project (e.g. `storymaker`, `dndassist`, `improvisor`, `relmirror`) has its own prompts, docs, and logic. The assistant should always prefer modularity and reusability.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Package Manager:** Poetry (`pyproject.toml`)
- **Web Framework:** Flask (if needed for APIs or interface layers)
- **Data:** pandas (for CSV/JSON parsing, data processing)
- **LLM API:** OpenAI (`openai` library), using environment variables for keys
- **Assets:** All outputs (audio, image, text) are stored **locally**, under appropriate folders (`outputs/audio`, `outputs/images`, etc.)

---

## ✨ Coding Standards

- Follow **PEP 8** and use **4-space indentation**
- Use **snake_case** for functions and variables, **CapWords** for classes
- **Always include docstrings** for functions and classes (PEP 257)
- Add type hints for all function parameters and return values
- Prefer **`pathlib`** for file paths over raw strings or `os.path.join`
- Use context managers for file I/O (`with open(...) as f:`)
- No global state; encapsulate logic in functions or classes

---

## 🧩 Architecture and Design Principles

- Follow **DRY**: factor repeated logic into helper functions
- Keep functions focused and under ~30 lines if possible
- Split larger processes into modular, testable parts
- Use `personalvibe` modules for shared tasks (audio, TTS, prompt rendering, etc.)
- Never hard-code API keys or config paths — use `os.environ` or config files
- Define reusable templates in `prompts/templates/` and load them with `prompt_engine.py`

---

## 🔄 Prompt-Driven Workflow Guidelines

- Cursor-generated code must respect the **structure of user-authored prompts**
- Do not overwrite prompt templates unless explicitly told
- Always follow the format, names, and conventions from the `.md.j2` prompt
- If a prompt has placeholders (e.g. `{{ character_name }}`), write code to populate these without altering the template logic
- Avoid injecting unsolicited features — stick to the user prompt

---

## 🧠 OpenAI API Usage

- Use the `openai` Python SDK for:
  - `ChatCompletion.create()` for text
  - `Image.create()` for illustrations
- API keys must be accessed via `os.getenv("OPENAI_API_KEY")`
- Handle `openai.error` exceptions and retry gracefully
- External config should define model (e.g., `"gpt-4"`), temperature, max tokens
- Never log or print sensitive content like API keys

---

## 🗂️ Local File Management

- Save all outputs under structured `outputs/` folders:
  - `outputs/audio/`
  - `outputs/images/`
  - `outputs/text/`
- Filename format: `taskname_timestamp.extension` (e.g. `npc_2024-04-13T12-00.png`)
- Always log successful saves with the full path
- Use `pathlib.Path` objects throughout

---

## 🔈 Audio and TTS

- Use `personalvibe.audio_input` for mic/audio file recording
- Use `personalvibe.tts_output` to generate audio from LLM responses
- TTS output should be MP3 or WAV, saved locally
- Ensure TTS responses are emotionally appropriate (e.g. soothing tone in `relmirror`)

---

## 🧪 Testing and Logging

- Add minimal test cases or usage examples when generating new logic
- Prefer `print()` for basic debugging, `logging` module for persistent tools
- Use assert statements in helper modules when generating new internal logic

---

## 🤖 Agent Behavior (improvisor, dndassist)

- Use `agent_core.py` to track agent state, goals, and hidden beliefs
- Agents should have:
  - visible dialogue (`say`)
  - internal state (`think`)
  - memory (`remember`)
- Mirror emotional realism and conversational pacing
- Avoid overwriting prior agent history unless prompted

---

## 🧭 Cursor Style Tips

- Be concise in completions
- Generate importable modules, not scripts
- Suggest code that works *with* existing modules
- If a library is missing, include a comment like:
  `# Requires: pip install pillow` (let user add via Poetry)
- Use Markdown or triple backticks in completions when displaying multi-line blocks

---

## ✅ Final Reminders

- Reuse existing helpers from `personalvibe/` whenever possible
- Prioritize modularity and readability
- Never add features or assumptions not present in the prompt
- This is a co-pilot workflow — stay focused, grounded, and maintain project consistency
