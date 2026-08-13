# Manual Checkpoint Runbook

Use this when the user explicitly asks to save/checkpoint project memory right now —
"save", "checkpoint", "บันทึกความจำ", "บันทึกงาน" — without waiting for a Stop hook.

This exists for agents/runtimes with no Stop-hook equivalent (e.g. Google Antigravity —
see `.ai/decisions.md` D-006), and for mid-session checkpoints on any agent when the
user doesn't want to wait until the turn ends.

## Steps (do them in order)

1. **See what actually changed.** Run `git status` (or `git diff`) if this is a git
   repo. If it isn't, review the files you edited this session directly.
2. **Update `.ai/state.md`** — all six sections, based on the ACTUAL current state, not
   what you plan to do next:
   `## Current Phase`, `## Current Status`, `## In Progress`, `## Current Issues`,
   `## Last Completed`, `## Next Action`.
3. **Update `.ai/plan.md`** at milestone/task level only — don't log every small edit as
   permanent history. Sections: `## Goal`, `## Current Phase`, `## Completed Milestones`,
   `## Current Tasks`, `## Next Milestone`.
4. **Update `.ai/decisions.md`** ONLY if an important project decision was actually made
   since the last checkpoint. Most checkpoints don't need this — skip it by default.
5. **Validate:**
   ```
   python scripts/validate_memory.py
   ```
   Must print `MEMORY VALIDATION PASSED`. If it fails, fix the file(s) named in the
   error and re-run — don't skip this step.
6. **If this is a git repo:** stage and commit `.ai/state.md`/`.ai/plan.md`/
   `.ai/decisions.md` together with any related code changes (see the
   git-commit-with-memory rule in `AGENTS.md`/`CLAUDE.md`). Ask the user before pushing,
   per normal git safety rules — don't push without asking.
7. **Tell the user what was saved**, in plain language — don't just say "done."

## What NOT to do

- Don't invent progress that didn't happen to make the checkpoint look better.
- Don't delete `.ai/.dirty`, `.ai/.checkpoint-retry`, or `.ai/precompact-recovery.md`
  manually to fake a clean state — let the real Stop hook (if one exists) manage those.
- Don't skip step 5 (validation) even if you're confident the files are correct.
