# Personalvibe workflow

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

## Design phases

These are the phases I'm using so far:

### Phase 1: Create a strong PRD

Spend a lot of time up front developing a product requirements document.

The one I used for storymaker seems to be a good amount of detail and domains.

It is helpful to add examples of prototype code, **codestyle**.

At this stage, AI can be used more informally and disposably to provide suggestions and help build out aspects of the PRD.

Start with fleshing out all non-technical aspects. And leave scoping of the technical approach to last.

### Phase 2: Create project structure

Ask AI to create the project structure.

You are tasked with designing the technical file and folder structure related to the storymaker project.
