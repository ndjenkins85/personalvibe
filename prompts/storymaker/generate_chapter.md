# Storymaker: Generate chapter

Your task is to generate a single chapter of a children's story.

You will be given the following information:

* Output format
* Background info
* Whole story information
* Specific chapter to generate
* Story character

## Output format

* Draw the scene photorealistically if you can, otherwise cartoonish as backup
* If a caption is specified, draw the caption using white text with black outline at the bottom center of the image
* Pay attention to physics based issues in images such as missing arms and legs, seating positions, and mirrors if relevant

## Background information

You will be creatively generating a compelling story for toddlers which use only a short story prompt and details about the toddler's favorite toy.

The audience is very young children.

You will only be responsible for generating one specific chapter of the story.

Do not create scenes that imply extreme closeness between the toddler and the other characters, do not create anything that could imply risk from a safety and community guidelines perspective.

Aim to keep things warm, innocent, and loving. Hugs are very okay!

Use plain English suitable for toddler.

## Whole story information

The following is a CSV of all chapters that comprise the story.
This is provided for two reasons, to give you information of the specific chapter, as well as the context of the overall story arc

<whole_story>
{whole_story}
</whole_story>

## Specific chapter to generate

You will generate the scene labelled as the following chapter:

<generate_chapter>
{generate_chapter}
</generate_chapter>

## Story character information

The following is information about the central character of the story.

<story_character_information>
{story_character_information}
</story_character_information>
