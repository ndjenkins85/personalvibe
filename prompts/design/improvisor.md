# improvisor: AI Co-Agents for Improv Comedy Practice

## Overview

`improvisor` is a real-time agent framework for practicing improv comedy scenes with AI-powered characters. It allows a solo performer to interact with one or more large language model (LLM)-driven agents that behave like scene partners: they hold secrets, have emotional intentions, and play roles in dynamic, evolving narratives.

This tool is designed to help beginner and intermediate improvisers rehearse core improv skills — such as “yes, and”, emotional commitment, character consistency, and building scenes collaboratively — in a sandboxed, low-pressure environment.

## Key Use Cases

- 🎭 **Solo Scene Practice**
  One human improviser interacts with 1–3 AI scene partners playing distinct roles in a shared environment.

- 🧠 **Theory of Mind Agents**
  Each AI character has internal goals, memories, and knowledge that may differ from what they say — enabling dramatic irony, hidden agendas, and emotional depth.

- 🧾 **Scene Setup and Prompts**
  Users can specify or generate a setting, character archetypes, and scene stakes to begin a practice session.

- 🔊 **Voice Input & Output**
  The system supports speech-to-text transcription for user input and optional TTS responses for AI dialogue.

## Project Goals

- 🤹‍♀️ **Dynamic Scene Generation**
  Create engaging and spontaneous dialogues that feel grounded in improvisational principles.

- 🧠 **Stateful Agents with Motivations**
  Model each agent with internal state: secret knowledge, goals, emotional triggers, and beliefs about the other characters.

- 🧍‍♂️ **Low-Latency, High-Responsiveness**
  Support real-time interaction with minimal delays to preserve rhythm and timing.

- 🎤 **Multimodal Input & Output**
  Transcribe voice input in real-time and optionally deliver AI responses via speech synthesis.

## Technical Scope

- **Core Modules from `personalvibe/`**
  - `audio_input.py`: Capture mic input during scene
  - `transcription.py`: Convert user speech to text
  - `agent_core.py`: Define and manage agents with memory, secrets, goals
  - `prompt_engine.py`: Compose per-agent dialogue prompts based on scene state
  - `tts_output.py`: Read aloud agent responses (if enabled)
  - `memory_store.py`: Maintain shared scene memory and agent state

- **Prompt Templates in `src/improvisor/prompts/`**
  - `agent_dialogue.md.j2`: Core template for generating an agent’s next line
  - `scene_starter.md.j2`: Generates a new scene setting and character suggestions
  - `internal_state_update.md.j2`: Updates agent goals and beliefs
  - `system.md.j2`: Defines core improv tone and format

- **Docs Folder in `src/improvisor/docs/`**
  - Product requirements
  - Prompt behavior guidelines
  - Sample scenes or training routines

## Optional Features

- 🎲 **Scene Randomizer**
  Generate quick randomized suggestions (location, character types, stakes) for warm-up scenes.

- 📝 **Debrief Mode**
  At the end of a scene, provide analysis or coaching based on pacing, emotional tone, or scene structure.

- 👥 **Group Play**
  Future extension could support multiple human improvisers or streamers interacting with agents collaboratively.

## Cursor Guidance

This project supports improv comedy practice by simulating interactive, emotionally grounded AI agents.

Write prompts that:
- Capture each agent’s **motivation, perspective, and tone**
- Reflect **improv principles** like agreement, escalation, and emotional truth
- Allow agents to make **strong offers**, **react emotionally**, and **heighten the scene**

Agents should have:
- **Visible behavior** (what they say and do)
- **Internal state** (what they believe, want, or fear)
- **Dynamic relationships** with others

Assume the user is improvising live — timing, clarity, and emotional variation matter.
