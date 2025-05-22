# Developer on-boarding (5 minutes)

1. **Clone** the repo and `cd` inside.
2. `poetry install --with dev,tests,lint,docs`
3. `pre-commit install`  (optional but recommended)
4. Run the *full* quality-gate locally:

   ```bash
   ./tests/personalvibe.sh
   ```

5. Create a branch `feature/<something>` and start hacking.

Troubleshooting tips
--------------------
• Missing `pv` after install? → `poetry env info --path` shows the venv,
  ensure its `bin/` is on `$PATH`.

• OpenAI key unavailable → set `OPENAI_API_KEY` or keep `--prompt_only`.

• Questions? Open an issue or ping @ndjenkins85 on GitHub.
