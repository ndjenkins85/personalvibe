# Copyright © 2025 by Nick Jenkins. All rights reserved

import base64
from pathlib import Path

import dotenv
import pandas as pd
import requests
from IPython.display import Image, display
from openai import OpenAI
from tqdm import tqdm

from src.personalvibe import utils

dotenv.load_dotenv()
client = OpenAI()

project_name = "Chikis Brooklyn bus adventure"
specific_story_prompt = """Join Chiki on a fun Brooklyn adventure!
Chiki asks his family to go on a bus (with a dream cloud)
They wait patiently at the bus stop
They board the bus, find a seat,
and enjoy the views as they pass by famous Brooklyn sights
They are friendly with other passengers who are enjoying the bus
They press the button for the stop
They get out at the museum and wave goodbye to the bus driver
"""
story_character_information = Path("prompts/storymaker/chiki.md").read_text()
story_character_image_path_str = "data/chiki.jpg"

ITERATIONS = 2

# Prepare story prompt
replacements = {
    "specific_story_prompt": specific_story_prompt,
    "story_character_information": story_character_information,
}

base_path = Path("data", utils.to_safe_name(project_name))
base_path.mkdir(exist_ok=True)

prompt_raw = Path("prompts/storymaker/generate_story.md").read_text()
prompt = prompt_raw.format(**replacements)
Path(base_path, "01_story_prompt.md").write_text(prompt)

story_character_image_path = Path(story_character_image_path_str)
story_character_image = base64.b64encode(story_character_image_path.read_bytes()).decode("utf-8")

# Prompting work

pbar = tqdm(total=11, desc="Processing")

# Request story
response = client.chat.completions.create(
    model="o3",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpg;base64,{story_character_image}"}},
            ],
        }
    ],
    # max_tokens=1000
)

response = response.choices[0].message.content

story_path = Path(base_path, "02_story.csv")
story_path.write_text(response)
whole_story = pd.read_csv(story_path)
pbar.update(1)

for ind, row in whole_story.iterrows():
    chapter = ind + 1

    prompt_raw = Path("prompts/storymaker/generate_chapter.md").read_text()
    replacements = {
        "generate_chapter": chapter,
        "story_character_information": story_character_information,
        "whole_story": whole_story,
    }
    prompt = prompt_raw.format(**replacements)
    Path(base_path, "03_chapter_prompt.md").write_text(prompt)

    result = client.images.edit(
        model="gpt-image-1", image=[open(story_character_image_path, "rb")], prompt=prompt, n=ITERATIONS
    )

    for i, image_data in enumerate(result.data):
        image_bytes = base64.b64decode(image_data.b64_json)
        output_path = Path(base_path, f"chapter_{chapter}_option_{i}.png")
        output_path.write_bytes(image_bytes)

    pbar.update(1)
