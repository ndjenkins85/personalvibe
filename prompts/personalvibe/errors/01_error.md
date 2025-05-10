I'm trying to get my patchdiff working in noxfile

--------------------

(personalvibe-py3.12) bash-3.2$ git apply --check data/storymaker_prompts/diffs/newdiff.patch
error: unrecognized input
(personalvibe-py3.12) bash-3.2$

--------------------

(personalvibe-py3.12) bash-3.2$ nox -s sprint -- data/storymaker_prompts/diffs/newdiff.patch  3.1.2
nox > Running session sprint-3.12
nox > Creating virtual environment (virtualenv) using python3.12 in .nox/sprint-3-12
nox > git worktree add .worktrees/vibed_3_1_2 -b vibed/3.1.2
nox > Session sprint-3.12 aborted: Patch dry-run failed (full trace in /Users/nicholasjenkins/Documents/personalvibe/logs/vibed_3_1_2.log).
(personalvibe-py3.12) bash-3.2$

--------------------

Preparing worktree (new branch 'vibed/3.1.2')
HEAD is now at c061fae add patch utils

--- PATCH-DRY-RUN ERROR ---
patch failed
