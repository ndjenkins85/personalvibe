# Storymaker: Generate story

Your task is to generate a short children's story based on a specific story prompt.

You will be given the following information:

* Output format
* Background information
* Specific story prompt
* Story character

## Output format

Your output must conform to the following requirements

* Reply using CSV format, so that your output is parsable by a python pandas without errors
* Do not provide any other justification, commentary or opinion, only the CSV as specified
* The CSV must have the following headers: chapter, title, scene, key_visual, caption
* Create 10 distinct scenes, such that the CSV is 11 lines total including header line
* 'chapter' field must be a numeric value between 1 to 10
* 'title' field must be a string of no more than five words
* 'scene' field describes the entirety of the scene as per a script must be a string of less than 60 words
* 'key_visual' field should describe the scene visually, and must be less than 60 words
* 'caption' is an optional field, with specific text that a character in the scene would say.

## Background information

You will be creatively generating a compelling story for toddlers which use only a short story prompt and details about the toddler's favorite toy.

The audience is very young children.

Your output will be used in later downstream steps to create compelling images in the story telling process.

You will only be responsible for generating the full story arc and 10 specific scenes of the story.

When creating the story, stick strongly to the provided story prompt and story character information

Your scene scripts must be suitable for use in a prompting engine in order to create images.

Secondary characters would be 'mum' and 'dad', and a unnamed toddler.

Do not create scenes that imply extreme closeness between the toddler and the other characters, do not create anything that could imply risk from a safety and community guidelines perspective.

Aim to keep things warm, innocent, and loving. Hugs are very okay!

Use plain English suitable for toddler.

## Specific story prompt

THe following is the specific story prompt which you will focus on to generate the overall story arc and scenes

<specific_story_prompt>
{specific_story_prompt}
</specific_story_prompt>

## Story character information

The following is information about the central character of the story.

<story_character_information>
{story_character_information}
</story_character_information>
