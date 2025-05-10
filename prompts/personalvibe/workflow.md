# Personalvibe product requirements document

You are tasked with {{ execution_task }} related to the personalvibe project.

{{ execution_details }}

I am still thinking through approaches to performing vibe coding.
I have been able to generate a MVP / scaffold of a good application.
While I started with cursor, I ended up rolling-my-own approach.
Ultimately it is what works best for you to have control of your project, code generation, and feedback loop.

## Constraints

I have been enourmously impressed with ChatGPT o3 as a vibecoding assistant.
It has key limitations of 200k context tokens and 100k output tokens.
No matter how much I prompt or parameterize for increased output tokens, o3 always seems to generate <20k characters.

The 200k is total budget for project inputs, outputs, and some further buffer for thinking.
I recommend capping out at 150k project input tokens, then you need to consider trimming context.

**API**: The o3 API has been an esssential tool for vibe coding automation.
Despite it costing quite a bit of money (~$10 a day), it has been worth it in terms of learning, enjoyment, and efficiency.
I consider this approach an investment, as well as a temporary high-price.

**Web**: I also have the OpenAI ChatGPT plus subscription, which is great for informal/disposable discussions.
These are best for early non-technical discussions, one-off bug hunts, and side-channel questions, that do not need the full project context.

## Broader considerations of the personalvibe project

{% include "design/personalvibe.md" %}

## Design phases

These are the phases I'm using so far:

### Phase 1: Draft PRD

Spend a lot of time up front developing and improving the product requirements document.
The one I used for storymaker seems to be a good amount of detail and domains.

It is helpful to add examples of prototype code, **codestyle**.

At this stage, AI can be used more informally and disposably to provide suggestions and help build out aspects of the PRD.

Start with fleshing out all non-technical aspects - technical approaches follow.

The PRD can be iterated, but it's best to invest heavily in this area up front.
This way we can avoid any surprises which may challenge the design.

The following is the pseudocode needed to create this interaction:


### Phase 2: Draft milestone

In this step, we ask the AI for a plain text description of the next logical project milestone.

Typically this is where we start using the API, to work with greater context windows.
This would include the prd, **codefiles**, codestyles.

The project milestone should be constrained to the following:
* A maximum of five logical sprints (chunks of work)
* Each sprint should be no more than 20k output tokens worth of work
* Sprints should be organized logically with respect to interfaces
* Each sprint must be testable


```python
def draft_milestone(
	prd_path: str,
	project_name: str,
	execution_task: str = "",
	execution_details: str = "",
	code_context_paths: List[str],
)
```

### Phase 3: Execute sprint

In this step, we ask the AI to develop code materials to execute a discrete sprint of work.

We use the API in this stage, due to the context required, and to help with automation.

We request that the model outputs executable python code to do the following kinds of activities:

- touch and mkdir for new files if needed
- Write code to new files, or patch existing files if needed
- Write or update the code testing procedures
- Restart the services, execute tests, smoketests, and collate logs into a central source
- AI performs an assessment as to whether the update was successful, or needs to be iterated based on errors in log or expectations
- Raises a pull request when code is ready to merge

```python
def execute_sprint(
	prd_path: str,
	project_name: str,
	milestone_plan: str,
	sprint_name: str,
	execution_details: str = "",
	code_context_paths: List[str],
)
```

## Code context

The following is the relevant existing code context, including file names and file contents, for use in your deliberations.

<code_context>
{{ code_context }}
</code_context>
