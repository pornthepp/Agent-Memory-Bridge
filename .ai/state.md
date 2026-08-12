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
Researched Antigravity hook support (WebSearch + WebFetch on antigravity.google/docs and
independent blog posts) — confirmed no SessionStart/PreCompact hook exists there, and
confirmed Antigravity does natively auto-load `AGENTS.md`. Fixed `AGENTS.md`'s opening
line, which previously told agents to NOT rely on it to load memory (correct for
Codex/Claude Code, actively wrong for Antigravity, which has nothing else to fall back
on). Logged as D-006. Full Antigravity `hooks.json` integration explicitly deferred.

## Next Action
Commit + push this checkpoint (`AGENTS.md` fallback fix, `.ai/decisions.md` D-006,
this state/plan sync). Nothing else pending.
