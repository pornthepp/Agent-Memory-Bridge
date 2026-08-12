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
None. Earlier this session, rounds 3-4 of Bash write-detection work were wrongly logged
as "broke again live" — see Current Issues for the correction (testing method was
flawed: `.dirty` isn't cleared by `git commit`, only by the Stop hook).

## Current Issues
- Bash write-pattern detection is heuristic, not a real shell parser. Exotic constructs
  (subshells, variable expansion, backticks) in non-git commands are still out of scope.
  `git merge`/`pull`/`rebase` aren't in `SAFE_GIT_SUBCOMMANDS` and still get scanned with
  the plain pattern list, even though they can rewrite files broadly too.
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
Nothing pending — README "ข้อจำกัด v1.1" and "Project change detection" now describe
the current shlex/heredoc/git-skip implementation, including the honest 2-confirmed-
bugs-plus-proactive-hardening framing. Consider re-running the scratch-folder clone test
at some point given the corrected picture, but not blocking.
