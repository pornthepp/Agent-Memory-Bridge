# AI Project Memory Guidance

This project uses automatic runtime hooks. The memory files are injected automatically; do not rely on this file to load them.

When a checkpoint hook asks for a memory update:

- Update `.ai/state.md` with current reality, completed work, issues, and the next action.
- Update `.ai/plan.md` at milestone/task level. Do not turn it into a per-edit history log.
- Append to `.ai/decisions.md` only for important accepted project decisions.
- Never manually delete `.ai/.dirty`, `.ai/.checkpoint-retry`, or `.ai/precompact-recovery.md`.
- If actual project files conflict with memory, treat actual project files as reality and reconcile the memory.
- Before finishing a session or pushing, commit `.ai/state.md`, `.ai/plan.md`, and `.ai/decisions.md` together with the code changes they describe. Never leave them uncommitted while code changes go out — the next agent (same tool or different) relies on git to receive the memory update along with the code.

When asked to bootstrap/initialize project memory (fresh install of this template):
- If the project is empty (no code yet): write honest "just starting" defaults into `state.md`/`plan.md` and ask the user for the actual goal before inventing one.
- If the project already has code/history: read the actual source tree, README, and `git log` (if a repo exists) before writing anything. Base `state.md`/`plan.md` only on what you can verify. If the real goal or phase isn't inferable from evidence, ask the user instead of guessing.
- Leave `decisions.md` empty at bootstrap; only add entries for decisions actually made afterward.
