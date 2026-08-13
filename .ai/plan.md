# Project Plan

## Goal
Build/maintain a shared project-memory hook system (Codex + Claude Code) that keeps
`.ai/state.md`, `.ai/plan.md`, `.ai/decisions.md` accurate via runtime hooks, not by
depending on the agent remembering to update them.

## Current Phase
v1.1 change-detection hardening.

## Completed Milestones
- [x] Installed template, renamed to **Agent Memory Bridge**, pushed to
      `github.com/pornthepp/Agent-Memory-Bridge` (main, up to date) (2026-08-12)
- [x] Bash-write detection: regex (D-003) → rewritten as `shlex` tokenizer (D-005) after
      2 confirmed real bugs (`->` arrow, bare `>` read as redirect); added quote-aware
      heredoc stripping + `SAFE_GIT_SUBCOMMANDS` skip-scan (2026-08-12)
- [x] Fixed a Windows-only crash: `session_start.py` died on non-ASCII memory-file text
      (`cp1252` stdout) — pushed `a3859fd` (2026-08-12)
- [x] AI-driven bootstrap prompts (empty vs existing project) + git-commit-with-memory
      convention documented in README/CLAUDE.md/AGENTS.md (2026-08-12)
- [x] Corrected session record (rounds "3-4 broke again" rested on a flawed `.dirty`
      test); synced README limitations section to match real code (2026-08-12)
- [x] Researched Antigravity hooks (confirmed: no SessionStart/PreCompact equivalent);
      shipped `AGENTS.md` fallback for non-hook agents (D-006) (2026-08-12)
- [x] Added manual checkpoint path: `.ai/CHECKPOINT.md` runbook + `/checkpoint` Claude
      Code slash command, for agents/moments with no Stop hook (2026-08-12)

## Current Tasks
- [ ] Decide whether the git-commit-with-memory rule should stay convention-only or
      become hook-enforced
- [ ] Clean up scratch test folder (user said they'd do it later)
- [ ] Consider adding `merge`/`pull`/`rebase` to Bash write-detection (known gap, not urgent)
- [ ] Build real `.agents/hooks.json` for Antigravity (PostToolUse/Stop only —
      SessionStart/PreCompact have nothing to map to) — deferred by user choice

## Next Milestone
Core detection work is settled. Antigravity has a documented manual fallback; full
hooks.json integration is deliberately deferred, not yet scheduled.
