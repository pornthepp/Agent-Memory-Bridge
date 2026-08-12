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
None. CORRECTION to earlier checkpoints in this session: rounds 3 and 4 of the Bash
write-detection work were NOT each confirmed live regressions the way rounds 1-2 were.
Testing methodology was flawed — checking whether `.ai/.dirty` existed right after a
live `git commit && git push` doesn't prove the commit's text caused a fresh false
trigger, because **`git commit` never clears `.dirty` — only `checkpoint_guard.py`
(the Stop hook) does, after validating state.md/plan.md are fresh.** That hook wasn't
actually invoked between rounds (mid-turn user messages kept the turn open), so `.dirty`
was simply persisting from legitimate `track_changes.py` edits made in the same turn.
Re-tested both the round-3 and round-4 trigger commit messages against their
*contemporary* code in isolation: both came back clean (no false target). So "it broke
again" for rounds 3-4 was likely a misread of a stale flag, not a real recurrence.

## Current Issues
- Bash write-pattern detection is heuristic, not a real shell parser. Exotic constructs
  (subshells, variable expansion, backticks) in non-git commands are still out of scope.
  README "ข้อจำกัด v1.1" not yet updated for the shlex/heredoc/git-skip changes.
- Committing `.ai/*.md` with code is a documented convention only, not hook-enforced.
- Confirmed (via direct, isolated function calls) real bugs: (1) `->` arrow in a commit
  message read as a redirect; (2) after fixing (1), a bare `>` in unrelated prose read
  the same way. Both fixed by moving to `shlex.split()`-based tokenizing (D-005).
- NOT independently confirmed, but kept as reasonable proactive hardening: quote-aware
  heredoc stripping (heredocs are a real shlex blind spot even if not proven to have
  fired live) and skipping write-scans for git metadata subcommands (add/commit/push/
  status/etc. — structurally can't rewrite project files, so scanning them was always
  unnecessary risk for no benefit).

## Last Completed
Corrected the session's own record-keeping: verified via `checkpoint_guard.py` that
`.dirty` clears normally when actually invoked (it did, cleanly). Re-tested the round-3
and round-4 trigger commands in isolation against their contemporary code — both clean,
contradicting the "broke again" claims made mid-session. Current code (shlex tokenizer +
quote-aware heredoc stripping + git-metadata skip) is correct and well-tested (21/21
unit cases) regardless — nothing needs reverting, only the causal narrative needed
fixing.

## Next Action
Update README "ข้อจำกัด v1.1" for the current (shlex/heredoc/git-skip) implementation.
Decide whether to re-run the scratch-folder clone test given the corrected picture.
