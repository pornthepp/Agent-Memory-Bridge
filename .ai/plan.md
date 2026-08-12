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
- [x] Added `strip_heredocs()` (quote-aware) + `SAFE_GIT_SUBCOMMANDS` skip, pushed as
      `77e6a8f` — proactive hardening, not each an independently confirmed live fix
      (2026-08-12)
- [x] Corrected session record: rounds "3-4 broke again" claims rested on a flawed test
      (`.dirty` checked right after `git commit`, which never clears it — only the Stop
      hook does); ran `checkpoint_guard.py` directly and confirmed it clears normally
      (2026-08-12)
- [x] Updated README.md "Project change detection" + "ข้อจำกัด v1.1" to match the real
      shlex/heredoc/git-skip implementation, with the honest 2-confirmed-bugs framing
      (2026-08-12)

## Current Tasks
- [ ] Decide whether the git-commit-with-memory rule should stay convention-only or
      become hook-enforced
- [ ] Clean up scratch test folder (user said they'd do it later)
- [ ] Consider adding `merge`/`pull`/`rebase` handling (not in the safe list, not
      pattern-scanned specially either — noted as a known gap, not urgent)

## Next Milestone
Bash write-detection is settled for now: 2 confirmed regex bugs fixed via shlex, plus
documented proactive hardening. No blocking work left on this thread.
