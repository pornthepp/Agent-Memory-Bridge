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
Bash write-detection has now been "fixed" 3 times in this session for the same class of
bug (see Current Issues) — flagging that pattern explicitly rather than just claiming
round 3 is the last one. Each fix was verified against every prior real failure, so
regressions are covered, but a 4th unseen edge case can't be ruled out from testing
alone. Not re-run against the scratch-folder clone since the heredoc fix; only unit- and
stdin-tested directly.

## Current Issues
- Bash write-pattern detection is heuristic, not a real shell parser. Exotic constructs
  (subshells, variable expansion, backticks) are still out of scope. README "ข้อจำกัด
  v1.1" not yet updated for the heredoc-stripping change specifically.
- Committing `.ai/*.md` with code is a documented convention only, not hook-enforced.
- 3 real failures of the same bug class this session, each caused by the *previous*
  fix's blind spot: (1) `->` arrow in a commit message read as redirect → fixed by
  lookbehind exclusion; (2) that patch didn't survive a *different* commit message with
  a bare `>` in prose → root-caused by switching to `shlex` tokenizing (D-005); (3) the
  shlex fix's own commit message (built via `$(cat <<'EOF' ... EOF)`, containing literal
  `"` characters) desynced shlex's quote-tracking since shlex doesn't model heredocs →
  fixed by `strip_heredocs()`, which removes heredoc bodies before tokenizing (heredoc
  bodies are never real shell syntax, so this is safe to drop unconditionally).

## Last Completed
Added `strip_heredocs()` to `track_changes.py`, applied before `shlex.split()`. Verified
against all 3 real failures from this session plus 15 other cases (redirects, cp/mv/tee/
touch/sed -i, ambiguous commands, a heredoc with a real redirect on its marker line) —
18/18. Not yet committed.

## Next Action
Commit + push. Given the pattern above, watch the very next commit's own message for a
recurrence before treating this as settled. Also update README "ข้อจำกัด v1.1" for the
heredoc-stripping behavior.
