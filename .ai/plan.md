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
- [x] Renamed project to Agent Memory Bridge (2026-08-12)

## Current Tasks
- [ ] Commit + push the rename (README.md, decisions.md D-004, this checkpoint)
- [ ] Decide whether v2 (git diff / file watcher / repo snapshot) is needed for full
      write-detection accuracy, or current regex-pattern coverage is sufficient
- [ ] Decide whether the git-commit-with-memory rule should stay convention-only or
      become hook-enforced

## Next Milestone
Confirm Bash write-detection holds up in real (non-mock) Claude Code sessions.
