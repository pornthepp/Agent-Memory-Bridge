# Project State

## Current Phase
v1.1 change-detection hardening, now under its real name.

## Current Status
- Project renamed to **Agent Memory Bridge** (was "AI Project Memory Universal").
- Git repo exists, remote `origin` = `github.com/pornthepp/Agent-Memory-Bridge.git`,
  pushed to `main` up through commit `a8670c8` before this rename.
- Automatic memory loading is configured for Codex and Claude Code.
- Change tracking (incl. Bash-tool writes), checkpoint enforcement, validation, and
  compact recovery are all configured and self-hosted by this repo's own hooks.
- Guidance tells agents to commit `.ai/*.md` together with code (not hook-enforced).

## In Progress
Renaming: `README.md` title updated to "Agent Memory Bridge"; `.ai/decisions.md` got
D-004 recording the rename. Not yet committed/pushed.

## Current Issues
- Bash write-pattern detection (`scripts/track_changes.py`) is regex-based, not a real
  shell parser. Known gaps documented in README.md "ข้อจำกัด v1.1".
- Committing `.ai/*.md` with code is a documented convention only, not hook-enforced.
- Rename is README/decisions-only so far — `.ai/plan.md` milestone text and any other
  old-name references have not been swept yet (see Next Action).

## Last Completed
Pushed `a8670c8` (AI-driven memory bootstrap prompts feature) to `origin/main`
successfully. Then renamed the project to Agent Memory Bridge per user's choice:
`README.md` title/subtitle updated, `decisions.md` D-004 added explaining why.

## Next Action
Commit the rename (`README.md`, `.ai/decisions.md`, this checkpoint) and push. Consider
whether `.ai/plan.md`'s old milestone line ("Install AI Project Memory Universal v1.1")
should stay as historical record or get a note — leaning toward leaving it, it describes
what was installed, not the project's current name.
