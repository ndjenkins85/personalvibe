# Copyright © 2025 by Nick Jenkins. All rights reserved
import hashlib
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List

import dotenv
import requests
from openai import OpenAI

dotenv.load_dotenv()
client = OpenAI()
logging.basicConfig(level=logging.INFO)


def get_prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def find_existing_hash(root_dir: str, hash_str: str) -> str | None:
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if hash_str in filename:
                return os.path.join(dirpath, filename)
    return None


def save_prompt(prompt: str, root_dir: Path, input_hash: str = "") -> None:
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    hash_str = get_prompt_hash(prompt)[:10]  # Shorten hash for filename

    # Check for existing hash match
    existing = find_existing_hash(root_dir, hash_str)
    if existing:
        logging.info(f"Duplicate prompt detected. Existing file: {existing}")
        return

    # Save prompt to new file
    if input_hash:
        filename = f"{timestamp}_{input_hash}_{hash_str}.md"
    else:
        filename = f"{timestamp}_{hash_str}.md"
    filepath = Path(root_dir, filename)
    filepath.write_text(prompt)

    logging.info(f"Prompt saved to: {filepath}")


def get_vibed(prompt: str, contexts: List[Path], max_completion_tokens=100_000) -> None:
    """Wrapper for O3 vibecoding to manage history and file interface"""
    base_input_path = Path("data/storymaker/prompt_inputs/")
    input_hash = save_prompt(prompt, base_input_path)

    messages = []
    for context in contexts:
        if "prompt_inputs" in context.parts:
            c = {"role": "user", "content": [{"type": "text", "text": context.read_text()}]}
        elif "prompt_outputs" in context.parts:
            c = {"role": "assistant", "content": [{"type": "text", "text": context.read_text()}]}
        messages.append(c)

    c = {"role": "user", "content": [{"type": "text", "text": prompt}]}
    messages.append(c)
    logging.info(f"Prompt input size: {len(str(messages))}")

    response = client.chat.completions.create(
        model="o3", messages=messages, max_completion_tokens=max_completion_tokens
    )
    response = response.choices[0].message.content

    logging.info(f"Prompt output size: {len(str(response))}")
    base_input_path = Path("data/storymaker/prompt_outputs/")
    _ = save_prompt(response, base_input_path, input_hash=input_hash)


def get_context(filenames: List[str], extension: str = ".txt") -> str:
    """Pulls in many file contexts."""
    big_string = ""

    for name in filenames:
        file_path = Path(name)

        if not file_path.exists():
            print(f"Warning: {file_path} does not exist.")
            continue

        # Read, deduplicate lines, and save back
        lines = file_path.read_text(encoding="utf-8").splitlines()
        unique_lines = sorted(set(lines))  # Optional: sort for consistency
        file_path.write_text("\n".join(unique_lines) + "\n", encoding="utf-8")

        for line in unique_lines:
            # Append to big string
            big_string += f"## {str(line)}\n"
            big_string += Path(line).read_text()

    return big_string
