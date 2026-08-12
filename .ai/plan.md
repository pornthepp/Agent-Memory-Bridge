# Project Plan

## Goal
Build/maintain a shared project-memory hook system (Codex + Claude Code) that keeps
`.ai/state.md`, `.ai/plan.md`, `.ai/decisions.md` accurate via runtime hooks, not by
depending on the agent remembering to update them.

## Current Phase
v1.1 change-detection hardening.

## Completed Milestones
- [x] Install AI Project Memory Universal v1.1
- [x] Extend PostToolUse change detection to cover Bash-tool file writes (2026-08-12)
- [x] Document git-commit-with-memory convention in CLAUDE.md/AGENTS.md/README.md (2026-08-12)
- [x] Pre-push cleanup: removed `__pycache__`, gitignored `settings.local.json` (2026-08-12)
- [x] Replace manual `.ai/*.md` editing with AI-driven bootstrap prompts (empty-project
      vs existing-project cases) in README.md/CLAUDE.md/AGENTS.md (2026-08-12)
- [x] git init, commit, and push to `origin/main` (2026-08-12) —
      `github.com/pornthepp/Agent-Memory-Bridge`
- [x] Renamed project to Agent Memory Bridge, committed `fe0db00`, pushed (2026-08-12)
- [x] Real end-to-end test: cloned repo to scratch folder, scaffolded calculator.py,
      drove SessionStart/PostToolUse/Stop/PreCompact hooks against it (2026-08-12)
- [x] Found + fixed a severe bug: `session_start.py` crashed on Windows (`cp1252`
      stdout) whenever memory files had non-ASCII text — pushed as `a3859fd` (2026-08-12)
- [x] Rewrote Bash write-detection around `shlex` tokenizing (D-005 supersedes D-003)
      (2026-08-12)
- [x] Round 3: added `strip_heredocs()`, pushed as `4b2ccf3` — then its own commit
      message retriggered `.dirty` (2026-08-12)
- [x] Round 4: made `strip_heredocs()` quote-aware + added `SAFE_GIT_SUBCOMMANDS` skip
      (2 independent layers) — 21/21 test cases pass (2026-08-12)

## Current Tasks
- [ ] Commit + push round 4; confirm `.ai/.dirty` stays clear afterward (verify, don't
      assume — rounds 1 and 3 both broke on their own commit)
- [ ] Update README.md "ข้อจำกัด v1.1" for rounds 3-4
- [ ] Decide whether the git-commit-with-memory rule should stay convention-only or
      become hook-enforced
- [ ] Clean up scratch test folder (user said they'd do it later)

## Next Milestone
Confirm round 4 holds through its own commit; if it does, this specific bug family can
be considered closed (both quote-aware parsing and a structural skip for the recurring
git-commit case are now in place).
