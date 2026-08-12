# Project State

## Current Phase
v1.1 change-detection hardening (this project IS the memory-hook tool).

## Current Status
- AI Project Memory Core is installed and self-hosting (this repo uses its own hooks).
- Automatic memory loading is configured for Codex and Claude Code.
- Change tracking, checkpoint enforcement, validation, and compact recovery are configured.
- Bash tool writes are now detected (previously only Write/Edit/NotebookEdit/apply_patch were).
- Guidance now tells agents to commit `.ai/*.md` together with code (no hook enforces this yet).

## In Progress
None — repo just cleaned up in prep for the user's own `git init`/commit/push.

## Current Issues
- Bash write-pattern detection (`scripts/track_changes.py`) is regex-based, not a real
  shell parser. Known gaps documented in README.md "ข้อจำกัด v1.1".
- Committing `.ai/*.md` with code is a documented convention only (CLAUDE.md/AGENTS.md/
  README.md), not hook-enforced yet.
- This directory is still NOT a git repo (`git status` → "not a git repository"). No
  `.git` exists. User said they will `git init`/commit/push themselves.

## Last Completed
Pre-push cleanup, at user's request:
- Deleted `scripts/__pycache__/` (regenerable bytecode cache, already gitignored).
- Added `.claude/settings.local.json` to `.gitignore` (session-local permission list —
  kept the file for local use, just excluded it from git so it never gets pushed).
- Confirmed no other stray/irrelevant files exist in the project tree.
- Prior changes still current: Bash write-detection in `track_changes.py`/`settings.json`
  (validated), and git-handoff guidance added to CLAUDE.md/AGENTS.md/README.md.

## Next Action
Nothing pending from the agent side. Waiting on user to `git init` and commit/push. If
asked again later, re-verify with `git status` before assuming repo state.
