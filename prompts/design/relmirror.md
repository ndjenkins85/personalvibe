# relmirror: Relationship Reflection & Coaching Assistant

## Overview

`relmirror` is a voice-based AI assistant designed to help individuals or couples reflect on their relationships. It allows users to speak freely about a disagreement, recurring dynamic, or emotional concern, and receive structured insights, reframed perspectives, or gentle reflections to support communication, understanding, and connection.

The system is intended to be emotionally intelligent, private, and non-judgmental — serving as a mirror that reflects values, patterns, and priorities back to the user. It is not therapy or a mediator, but a tool for thoughtful self-reflection and awareness.

## Key Use Cases

- 💬 **Voice Journaling or Conversation Capture**
  A person or couple records a conversation or monologue describing a recent challenge or emotional experience.

- ✍️ **Reflective Summary Generation**
  The system transcribes the input, identifies emotional themes and relational dynamics, and outputs a structured reflection.

- 🪞 **Mirroring Emotional Priorities**
  The assistant tries to echo each person’s needs, pain points, or intentions in a kind, respectful voice — encouraging empathy.

- 🔄 **Profile Building Over Time**
  Optionally, the system can build and evolve a lightweight profile of each person’s values, sensitivities, and recurring needs to ground future reflections.

## Project Goals

- 🧠 **Compassionate Contextual Understanding**
  Generate emotionally intelligent summaries grounded in what matters most to each speaker.

- 🔒 **Privacy-Preserving by Design**
  Ensure user voice data and transcripts are treated with strict confidentiality. Optionally, support local-only or end-to-end encrypted storage.

- 🗣️ **Natural Voice Input & Output**
  Enable frictionless use through speech-to-text and optional voice synthesis of the reflection response.

- 🧭 **Non-Prescriptive Guidance**
  Offer gentle framing and re-phrasing without making direct judgments or offering fixed advice.

## Technical Scope

- **Core Modules from `personalvibe/`**
  - `audio_input.py`: Record or upload dialogue
  - `transcription.py`: Transcribe to clean text using Whisper
  - `prompt_engine.py`: Generate reflections, summary, and mirror responses
  - `memory_store.py`: Track profile fragments and conversation history
  - `tts_output.py`: Read reflections aloud in a calming tone

- **Prompt Templates in `src/relmirror/prompts/`**
  - `relationship_reflection.md.j2`: Core prompt for summarizing a conversation or journal entry
  - `profile_update.md.j2`: Used to extract/upkeep emotional profile data
  - `mirror_response.md.j2`: Generates a response phrased as a compassionate “mirror” voice
  - `system.md.j2`: Ensures emotional tone and grounding

- **Docs Folder in `src/relmirror/docs/`**
  - Product requirements
  - Prompt guidelines and tone calibration
  - Example use cases and response scenarios

## Optional Features

- 📊 **Tone Tracker or Pattern Insights**
  Detect emotional tone or recurring cycles over time to help users recognize patterns in how they feel or speak.

- 📆 **Conversation Timelining**
  Let users replay the evolution of a theme or dynamic across multiple sessions.

- 🔄 **Alternate Voice Styles**
  Offer personalization of the reflection voice (soothing, neutral, curious, etc.)

## Cursor Guidance

This project is a **mirror, not a fixer**. Reflections should be emotionally sensitive, safe, and constructive. Use language that builds bridges, not sides.

When writing prompts or generating outputs:
- Summarize what matters most to each speaker
- Echo emotional content without judgment
- Use phrasing that encourages self-awareness and calm re-engagement
- Avoid direct advice, criticism, or simplification of complex emotions

Examples of strong outputs include:
> “You seem to really value feeling heard, especially when things get overwhelming.”
> “It sounds like both of you are trying to protect something important — even if you’re expressing it differently.”

Prioritize warmth, respect, and clarity. Assume privacy and care are central to the product.
