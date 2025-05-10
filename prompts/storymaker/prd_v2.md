# Storymaker product requirements document

You are tasked with {{ execution_task }} related to the storymaker project.

{{ execution_details }}

{% if generate_diff %}
{% include "personalvibe/generate_diff.md" %}
{% endif %}
{% if generate_python_patch %}
{% include "personalvibe/generate_python_patch.md" %}
{% endif %}
{% if generate_milestone %}
{% include "personalvibe/generate_milestone.md" %}
{% endif %}

<effort>High</effort>
<mode>Thoughtful before action</mode>
<output_size>Maximum allowed, i.e. up to 100,000 tokens</output_size>

You will be provided the following information

* Project background
* Code context
* Code style guidelines
* Example character
* Example story data
* Major AI prompts
* Technical requirements
* Product behaviour requirements
* Chunking plan

## Project background

Storymaker is a hobby project to automate the creation of children's books based on ChatGPT image generation.

It is a python project within the 'personalvibe' megaproject.
The 'personalvibe' megaproject contains helpful utilities, scaffolding, and shared code between other AI based hobby projects.

## Code context

The following is the relevant existing code context, including file names and file contents, for use in your deliberations.

<code_context>
{{ code_context }}
</code_context>

## Code style guidelines

The following is a markdown document containing recommended code style guidelines.
<code_style_guide>
{% include "code_style_guide.md" %}
</code_style_guide>

## Example character

The following is an example of a character

<Example character: Chiki>
{% include "storymaker/chiki.md" %}
</Example character: Chiki>

## Example story data

The following is an example of the data contents of a story

<example_story_data>
{% include "storymaker/story_example.csv" %}
</example_story_data>

## Major AI prompts

The following are some core prompts that perform AI based work.
These are provided as context for the storymaker PRD.

<prompt_examples>

<generate_story_prompt>
{% include "storymaker/generate_story.md" %}
</generate_story_prompt>

<generate_chapter_prompt>
{% include "storymaker/generate_chapter.md" %}
</generate_chapter_prompt>

</prompt_examples>

## Technical requirements

Must create a python project with the following features:

* Pydantic interfaces
* Poetry pyproject.toml
* Robust, modern logging
* Flask backend
* Modern, single page application front end
* Data interface which is clearly separated from code (IO)
* Data storage using local file system under Path("data/storymaker") base folder (to be migrated later)
* Login system to interact with your specific data

## Product behaviour requirements

The website must have the following pages

- Index: Create a custom kids book
- My Books: Lists previously created books
- Characters: Manage your characters
- Studio: Create a new story
- My Account: Manage your login and account details

### Index: Create a custom kids book

- Shows a moving gallery of example books (placeholders)
- Has a large placeholder to highlight a character

### My Books: Lists previously created books

- Shown in gallery card format
- The last element of the gallery has a ' + New ' link
- Gallery card shows the image of the book front cover, and the book title, and created date YYYY-MM-DD
- You can star your favorite books
- Books are sorted by favorited and latest created date
- Clicking on a book opens a panel which allows you to click through each chapter of the story

### Characters: Manage your characters

- The page is divided into an Upload section (left) and an Avatar section (right)
- Upload section
	- Characters can be specified as adult, child, or toy
	- Characters can be named, have a longform description, and image upload functionality
- Avatar section
	- Has a placeholder image for avatar
	- Has a 'Regenerate' button
	- Has an Regenerate textbox with gray text helper '(Optional): Regenerate instructions'
	- Regeneration will kick off an AI image creation process using backend API
	- When image is ready, it will appear
	- Has a button for 'set to account image'

### Studio: Create a new story

- Part 1: Story background
	- Book name
	- Book details
	- Main character (single select)
	- Side characters (multi select)
- Part 2: Review the script
	- After generating the story, users can edit chapter information
	- Chapter information appears in a row, with a medium size thumbnail of the generated image
	- There should be a special border for the front page, and back page, with 10 other rows as per the story prompt
	- Each chapter has it's own 'regenerate' button
	- A button at the bottom is titled 'regenerate all'
	- Another button is labelled 'OK' and closes the window

### My Account: Manage your login and account details

Has a section for login / logout
Has an account image, which defaults to a placeholder, and can be created through the avatar process


{% if milestone_plan %}
## Milestone Plan

The following is the current project milestone plan, so as to work around large language model input/output limits.
<milestone_plan>
{% include milestone_plan %}
</milestone_plan>
{% endif %}
