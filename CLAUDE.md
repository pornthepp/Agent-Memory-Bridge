# AI Project Memory Guidance

Project memory is loaded automatically by Claude Code lifecycle hooks from `.ai/`.

This file provides formatting guidance only; runtime hooks are the enforcement layer.

When a checkpoint hook asks you to update memory:

- Update `.ai/state.md` with the actual current project state, completed work, issues, and `## Next Action`.
- Update `.ai/plan.md` at milestone/task level. Avoid logging every small edit permanently.
- Update `.ai/decisions.md` only when an important project decision is made.
- Do not manually delete `.ai/.dirty`, `.ai/.checkpoint-retry`, or `.ai/precompact-recovery.md`.
- After pre-compact recovery, inspect the actual project before reconciling stale memory.
- Before finishing a session or pushing, commit `.ai/state.md`, `.ai/plan.md`, and `.ai/decisions.md` together with the code changes they describe. Never leave them uncommitted while code changes go out — the next agent (same tool or different) relies on git to receive the memory update along with the code.

When asked to bootstrap/initialize project memory (fresh install of this template):
- If the project is empty (no code yet): write honest "just starting" defaults into `state.md`/`plan.md` and ask the user for the actual goal before inventing one.
- If the project already has code/history: read the actual source tree, README, and `git log` (if a repo exists) before writing anything. Base `state.md`/`plan.md` only on what you can verify. If the real goal or phase isn't inferable from evidence, ask the user instead of guessing.
- Leave `decisions.md` empty at bootstrap; only add entries for decisions actually made afterward.
