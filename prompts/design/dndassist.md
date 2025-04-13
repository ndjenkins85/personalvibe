# dndassist: AI Companion for Dungeon Masters

## Overview

`dndassist` is an AI-powered assistant for Dungeon Masters (DMs) playing tabletop roleplaying games like Dungeons & Dragons. It helps capture, summarize, and visualize key moments in a campaign by transcribing gameplay audio, tracking characters and events, and generating summaries and scene art.

This project is designed to run alongside live sessions or be used for post-session reflection. It emphasizes real-time or near-real-time interaction while staying out of the way of the DM’s creative flow.

## Key Use Cases

- 🎙️ **Session Transcription**
  Transcribe voice conversations during a game session to text, enabling downstream summarization and context capture.

- 🧾 **Scene Summarization**
  After a key scene or battle, generate a short summary of what happened to share with players or to log for continuity.

- 🧙 **NPC Tracking**
  Automatically recognize when a new NPC is introduced and create a reference entry for them (name, traits, image, role in story).

- 🖼️ **AI-Generated Illustrations**
  Generate images of scenes or characters described during gameplay to enhance immersion.

- 📘 **Campaign Log Creation**
  Build a searchable history of events, characters, and locations to help players stay engaged and avoid continuity gaps.

## Project Goals

- 🧠 **Passive AI Support**
  Provide meaningful assistance without interrupting gameplay — ideally activated by simple triggers or batch processing between scenes.

- 🪄 **Flexible Input Modes**
  Accept both recorded audio and manual text for processing (supporting both live and post-session workflows).

- 🧑‍🤝‍🧑 **Multi-Character Awareness**
  Maintain context about multiple PCs and NPCs over time, updating their states or relationships across scenes.

- 🖼️ **Visual Immersion**
  Enhance storytelling with visuals that match the tone and content of the scene (e.g., dark forest, epic battle, mysterious NPC).

## Technical Scope

- **Core Modules from `personalvibe/`**
  - `audio_input.py`: Record or stream gameplay audio
  - `transcription.py`: Convert audio to text using Whisper
  - `prompt_engine.py`: Render structured summaries and NPC entries
  - `image_gen.py`: Generate scene and character images
  - `memory_store.py`: Track campaign state, NPC registry
  - `tts_output.py` (optional): Narrate summaries or recaps

- **Prompt Templates in `src/dndassist/prompts/`**
  - `battle_summary.md.j2`
  - `npc_profile.md.j2`
  - `scene_description.md.j2`
  - `system.md.j2`: Sets tone, format, and DM assistant behavior

- **Docs Folder in `src/dndassist/docs/`**
  - Product requirements
  - Prompt guidelines
  - Example campaign logs

## Future Add-ons

- 🤖 **Voice Commands for Triggering Actions**
  - E.g., “Log this scene” or “Who was that NPC again?”

- 📅 **Session Calendar & Replay**
  - Organize sessions and summaries by date or chapter

- 🧩 **Player Companion Extension**
  - Optional module for players to view logs, summaries, and NPC images between sessions

## Cursor Guidance

This project is an AI co-pilot for tabletop gaming — not a game master replacement. Assume a human DM is always in control. Focus on:

- Capturing events clearly, especially names, conflicts, outcomes
- Maintaining consistency and character identity across sessions
- Enhancing immersion with vivid, appropriate visual assets
- Being unobtrusive — tools should be called manually or by trigger, not interrupt live gameplay

Write prompts that are:
- Narrative-friendly, in the style of a fantasy chronicle or journal
- Focused on what matters to players (e.g. stakes, emotions, discoveries)
- Able to transform raw speech into structured campaign content
