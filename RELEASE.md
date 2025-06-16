# Release guide

This is a *living* checklist to cut an **Independence Day** style
release.  Nothing here enforces policy – it is a reminder that the
human-in-the-loop must still sanity-check artefacts.

1. `git switch master && git pull`
2. Ensure CI is green on *all* branches slated for merge.
3. Run the full quality-gate locally:

    ./tests/personalvibe.sh 2.1.0

4. Bump changelog / docs if needed.
5. Tag & push:

    git tag v2.1.0 && git push origin v2.1.0

6. GitHub Actions will build & upload the wheel.
7. Verify **PyPI** and **docs** artefacts.
8. Tweet the release, grab ☕.
