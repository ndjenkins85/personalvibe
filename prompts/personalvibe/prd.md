# Personalvibe product requirements document

* Project background
* Using ChatGPT o3
* Design phases
* Phase 1: Draft PRD
* Phase 2: Draft milestone
* Phase 3: Execute sprint
* Phase 4: Validate sprint
* Q&A
* Code context

## Project background

Personalvibe turns brainstorming into repeatable AI-assisted build pipelines for hobby projects.

It contains a set of documentation, prompts, and code organized into milestones and sprints.

AI services can help us flesh out the project design, major milestones, and the execution of sprint tasks.

By completing many sprint tasks we can gradually build the product.

## Using ChatGPT o3

ChatGPT o3 is an impressive vibecoding assistant.
It has a high intelligence, and ability to create effective code structures.

**API**: The o3 API has been an esssential tool for vibe coding automation.
Despite it costing quite a bit of money (~$10 a full day), it has been worth it in terms of learning, enjoyment, and efficiency.
It can handle 200k context tokens and 100k output tokens.
In practice, o3 always seems to output <20k characters.
The 200k is total budget for project inputs, outputs, and some further buffer for thinking.
I recommend capping out at 150k project input tokens, then you need to consider trimming context.

**Web**: I also have the OpenAI ChatGPT plus subscription, which is great for informal/disposable discussions.
These are best for early non-technical discussions, one-off bug hunts, and side-channel questions, that do not need the full project context.

## Design phases

These are the phases I'm using so far:

### Phase 1: Draft PRD

Drafting PRD is a highly manual writing process where you must lead the strategic project management.

Best to use informal/disposable AI to provide suggestions and help build out aspects of the PRD.

Start with fleshing out all non-technical aspects - technical approaches follow.

It is helpful to add examples of **prototype code**, **codestyle**.

The PRD should be open to being iterated throughout the project, so as to stay adapative with strategy.

### Phase 2: Draft milestone

In this step, we ask the AI for a plain text description of the next logical project milestone.

We can iterate on the design of our milestone until we are ready to turn it into sprints.

Depending on context length requirements, you can use informal/disposable or API interfaces.

Milestone documents benefit from the following context:

- prd: This document
- codestyles: Your preferences for writing and reading code, tech stack, preferences
- codefiles: Specific files to include as filenames + entire file contents
- prototype code: Early example prototype of core tech

Milestones should be constrained to the following:

* A maximum of five logical sprints (chunks of work)
* Each sprint should be no more than 20k output tokens worth of work
* Sprints should be organized logically with respect to interfaces and dependencies
* Each sprint must be testable, include effective tests, and help orchestrate testing within existing frameworks

### Phase 3: Execute sprint

In this step, we hand over to the AI to develop code materials to execute a discrete sprint of work.

We use the API in this stage, due to the context required, and to help with automation of validation.

We request that the model outputs executable python code, which we run in a sandboxed docker environment.

Sprint output can include:

- `touch` and `mkdir` like behaviour for new files if needed
- Write code to new files, or patch existing files if needed
- Write or update the code testing procedures
- Manage the services startup process using docker
- Manage executing tests, smoketests, and the collation of logs into a central info and debugging trace
- No file delete operations are allowed, log to the user in a separate log file

Users would feed results into the validate step

### Phase 4: Validate sprint

In this step, we ask the AI to validare code materials from a sprint.

- Assess logs to reason if the update was successful
- If errors exist, retry sprint prompt with errors
- Raises a pull request when code is ready to merge

The file changes may include changes to how the tests and logging is orchestrated.

“Definition of Done” once (e.g. code passes lint + tests, docker-compose up, PR merged).

## Q&A

The following are answers to some common questions

- The lead decision-maker can be referenced as “product owner”
- Cost governance not an issue at this stage
- We already save output to data/{project}/prompt_input or data/{project}/prompt_output users have the choice of entering that code into prompts/{project}/ for a more permanent home and valid place in context.
- At this stage we are only using data/ local file store, no databases
- Milestone = major, sprint = minor, bugfix iteration = patch
- Multimodal bits we will handle later and in separate projects not core personalvibe
- Logging has been addressed since last review
- Renames should be done by `git mv` operations (executed by user), within file migrations are fine, as they are covered by git version control
- Not worried about context bloat at this stage, plenty of room to grow
- Developing core is a priority for learning and development
- Not worried about external api rate limits

3 · Rationale
These edits translate tacit decisions into explicit, version-controlled artefacts. Freezing the persistence layer and semver rules reduces cognitive overhead for every sprint. Splitting prompt drafts from production avoids accidental context inflation without stifling creativity. A permissive cost-tracking warning keeps finances visible while respecting your “not an issue yet” stance. Lastly, codifying the rename pathway preserves repository hygiene without breaching the no-delete guarantee.
