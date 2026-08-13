# Project State

## Current Phase
v1.1 change-detection hardening, now under its real name.

## Current Status
- Project renamed to **Agent Memory Bridge**, committed (`fe0db00`) and pushed to
  `origin/main` at `github.com/pornthepp/Agent-Memory-Bridge.git`.
- Automatic memory loading is configured for Codex and Claude Code.
- Change tracking (incl. Bash-tool writes), checkpoint enforcement, validation, and
  compact recovery are all configured and self-hosted by this repo's own hooks.
- Guidance tells agents to commit `.ai/*.md` together with code (not hook-enforced).

## In Progress
None — see Next Action for the one pending step (commit + push this checkpoint).

## Latest addition
Manual checkpoint path shipped: `.ai/CHECKPOINT.md` (step-by-step runbook — plain
markdown, works with ANY agent that can read a file, not just Claude Code/Codex) plus
`.claude/commands/checkpoint.md` (`/checkpoint` shortcut, Claude Code only). README
documents the one-line prompt for agents without a slash-command shortcut. User asked
about opencode/Codex/Gemini CLI/Antigravity specifically — answered: the runbook itself
is universal, but per-tool slash-command shortcuts (Gemini CLI's own format, etc.)
haven't been researched/built yet — explicitly left open, not fabricated.

## Current Issues
- Bash write-pattern detection is heuristic, not a real shell parser. Exotic constructs
  (subshells, variable expansion, backticks) in non-git commands are still out of scope.
  `git merge`/`pull`/`rebase` aren't in `SAFE_GIT_SUBCOMMANDS`, still scanned plainly.
- Committing `.ai/*.md` with code is a documented convention only, not hook-enforced.
- **Antigravity (Gemini) has no `SessionStart`/`PreCompact`-equivalent hook** — confirmed
  via web research (D-006). Only `PreToolUse`/`PostToolUse`/`PreInvocation`/
  `PostInvocation`/`Stop` exist. Full `.agents/hooks.json` support deferred by user
  choice ("ยังก่อนดีกว่า"). Fallback shipped instead: `AGENTS.md` (which Antigravity
  auto-loads natively) now tells non-hook agents to read `.ai/*.md` themselves first.

## Last Completed
Added `.ai/CHECKPOINT.md` (manual checkpoint runbook, universal across agents) and
`.claude/commands/checkpoint.md` (`/checkpoint` shortcut, Claude Code only). README
documents the manual-trigger prompt and the slash command. Trimmed `plan.md`'s
milestone list (was approaching its 3500-char cap) to make room.

## Next Action
Commit + push this checkpoint (`.ai/CHECKPOINT.md`, `.claude/commands/checkpoint.md`,
`README.md`, this state/plan sync). Nothing else pending.
