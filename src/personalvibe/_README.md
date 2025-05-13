# personalvibe

Shared utilities reused by multiple hobby projects (importable as `personalvibe`).


## Prompt persistence & hashing

Every prompt (input *and* LLM output) is written to
`data/<project>/prompt_[in|out]puts` with a filename that embeds:

1. A timestamp – human searchable
2. An optional upstream *input* hash (so output files can be paired)
3. The first 10 chars of **SHA-256(prompt)** – collision-safe ID

The helper `personalvibe.vibe_utils.save_prompt()` de-duplicates using the
hash so re-runs never flood the directory; it simply returns the existing
`Path` when a match is found.  Each file is suffixed with

```text
### END PROMPT
```

which makes shell/grep extraction of individual prompts trivial.
