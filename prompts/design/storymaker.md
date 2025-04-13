# storymaker: AI Engine for Personalized Children’s Books

## Overview

`storymaker` is a modular AI-powered framework for generating personalized children’s books. It allows parents, educators, or creators to quickly generate toddler-appropriate stories based on custom inputs — such as the child’s name, favorite toy, story theme, or real-world location. The system combines structured prompting, image generation, and narrative templates to output emotionally resonant stories that feel personal, magical, and familiar.

This project is designed for extensibility and supports both batch workflows (e.g., create a storybook set for printing) and real-time interaction (e.g., generate a story on-demand with voice input or app-based selections).

## Motivating Use Case: Chiki

As an example implementation, Chiki is a lovable plush duck and the star of a giftable storytelling bundle. The Chiki experience includes:
- A custom plush toy
- Two fully illustrated books set in the child’s own city (e.g. Brooklyn, SF, Tokyo)
- Familiar scenes (e.g. subways, playgrounds, pizza shops)

Chiki stories help toddlers build emotional connection to their world — turning daily places into imaginative adventures. `storymaker` powers the backend: generating location-specific stories, toddler-safe illustrations, and consistent character experiences.

## Project Goals

- 🧒 **Hyper-Personalized Storytelling**
  Let users generate stories based on custom toy characters, child names, locations, or themes (bedtime, friendship, bravery, etc.)

- 🖋️ **Narrative Prompting Framework**
  Use flexible Jinja2 prompts to generate structured stories with a clear arc: introduction → adventure → resolution

- 🗺️ **Real-World Location Integration**
  Ground stories in real cities or neighborhoods by embedding landmarks, local foods, transport, etc.

- 🧸 **Consistent Character Support**
  Support both default mascots (like Chiki) and user-uploaded toys or avatars for story personalization

- 🖼️ **Illustration Generation**
  Use AI image models to produce child-safe, consistent illustrations — either generic or specific to a toy/photo

- 📘 **Book Output Pipeline**
  Assemble generated text and images into printable/exportable formats (e.g. PDF, EPUB)

## Technical Scope

- Prompt templates for:
  - Story text generation (structured, toddler-friendly)
  - Scene-to-image illustration descriptions
  - Character consistency prompts (for known avatars like Chiki)

- Core modules in `personalvibe/`:
  - `prompt_engine.py` for rendering templates
  - `image_gen.py` for AI image creation
  - `tts_output.py` (optional) for narrated stories
  - `memory_store.py` to persist story preferences

- File export pipeline (e.g. ReportLab or WeasyPrint) to combine text + image into book format

## Cursor Guidance

Use this file to guide all development inside `src/storymaker/`.

The system should always prioritize:
- Age-appropriate language (target: toddlers aged 2–5)
- Personalization (name, toy, place)
- Familiarity and emotional tone (gentle, joyful, curious)

Chiki is an example of a specific implementation. `storymaker` should remain general-purpose — capable of supporting any plush character or location the user specifies.

When designing prompts, default to:
- Friendly tone
- Simple sentence structure
- Scenes that build emotional connection (e.g. getting lost, making a friend, exploring a park)
