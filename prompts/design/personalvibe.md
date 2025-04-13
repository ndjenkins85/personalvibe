# personalvibe: Core Framework for Vibe Coding Projects

## Overview

`personalvibe` is a shared library that powers multiple AI-assisted, prompt-driven applications. It provides reusable tools and patterns for handling audio, prompt templating, image generation, memory management, and more. This framework enables "vibe coding" — a workflow where prompts, context, and AI logic are first-class citizens of software development.

All projects that live in `src/` consume the modules in `personalvibe`. Each project is structured independently, with its own prompts, task logic, and documentation — but relies on this shared foundation to speed up development and unify core capabilities.

## Project Goals

- 🔁 **Reusable Core**: Build once, use everywhere. Each project should only define what makes it unique.
- 🧱 **Composable Prompt Logic**: Enable a modular Jinja2-based prompt engine that allows combining templates, system prompts, and dynamic inputs.
- 🎙️ **Voice-First by Design**: Support workflows based on recorded or live audio input, then transcribed into text for LLM processing.
- 🎨 **Multimodal Ready**: Easily integrate image generation, audio synthesis, and other modalities in a consistent API structure.
- 🧠 **Stateful Agents & Memory**: Track user sessions, character states, or conversational context across turns or interactions.
- 🚀 **Real-Time + Batch Modes**: Support both immediate, conversational workflows (e.g. improv practice) and background task pipelines (e.g. children’s book creation).

## High-Level Architecture

- `audio_input.py`: Record and save audio from a mic, or stream in chunks.
- `transcription.py`: Transcribe audio files using OpenAI Whisper or other models.
- `prompt_engine.py`: Load and render Jinja2 prompt templates from file paths.
- `image_gen.py`: Wrapper to generate images using OpenAI DALL·E, Midjourney, or other models.
- `agent_core.py`: Define and manage agents with memory, secret goals, and reactive dialogue.
- `memory_store.py`: Handle state persistence via local JSON, SQLite, or vector DBs.
- `tts_output.py`: Convert generated text into realistic voice responses using ElevenLabs, PlayHT, or OpenAI TTS.

## Usage Pattern Across Projects

Each project in `src/` includes:

- A `main.py` file as the primary entrypoint
- A `prompts/` directory containing runtime prompt templates
- A `docs/` folder to capture design and requirement decisions
- Dependencies on `personalvibe` for all AI-heavy infrastructure

Example:
- `src/story_creator/` uses `transcription`, `prompt_engine`, and `image_gen` to turn user ideas and toy images into illustrated children's books.
- `src/dnd_assist/` uses `audio_input`, `agent_core`, and `image_gen` to support live D&D play with NPC tracking and scene illustrations.

## Cursor Guidance

Use this document to understand the shared context across all projects using `personalvibe`. If helping with a task like writing a prompt, building an agent, or handling audio, prefer using `personalvibe` modules first.

When generating new features, assume modularity — if it’s useful across more than one app, consider implementing it in `personalvibe`.
