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
Replaced manual `.ai/*.md` editing in the install flow with an AI-driven bootstrap:
- `README.md` "ติดตั้งใน Project ใหม่": step 2 is now a copy-paste prompt for the agent
  instead of "edit these files yourself." Two variants — Case A (empty project: agent
  writes honest "just starting" defaults, asks user for the real goal) and Case B
  (existing project: agent reads source tree/README/git log first, no guessing).
  `decisions.md` explicitly left empty at bootstrap.
- `CLAUDE.md`/`AGENTS.md`: added matching "When asked to bootstrap/initialize project
  memory" rule so both Claude Code and Codex follow the same no-fabrication behavior.
- Prior changes still current: Bash write-detection in `track_changes.py`/`settings.json`
  (validated), git-handoff-with-commit guidance, and pre-push cleanup
  (`__pycache__` removed, `settings.local.json` gitignored).

## Next Action
Nothing pending from the agent side. This repo still has no `.git` — user will `git
init`/commit/push themselves. If asked again later, re-verify with `git status` first.
