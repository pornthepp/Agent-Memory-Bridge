# AI Project Memory Guidance

This project uses automatic runtime hooks. The memory files are injected automatically; do not rely on this file to load them.

When a checkpoint hook asks for a memory update:

- Update `.ai/state.md` with current reality, completed work, issues, and the next action.
- Update `.ai/plan.md` at milestone/task level. Do not turn it into a per-edit history log.
- Append to `.ai/decisions.md` only for important accepted project decisions.
- Never manually delete `.ai/.dirty`, `.ai/.checkpoint-retry`, or `.ai/precompact-recovery.md`.
- If actual project files conflict with memory, treat actual project files as reality and reconcile the memory.
- Before finishing a session or pushing, commit `.ai/state.md`, `.ai/plan.md`, and `.ai/decisions.md` together with the code changes they describe. Never leave them uncommitted while code changes go out — the next agent (same tool or different) relies on git to receive the memory update along with the code.
