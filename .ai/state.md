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
Bash write-detection was "fixed" 4 times this session for the same bug family (see
Current Issues). Round 4 pushed as `4b2ccf3` and its OWN commit message immediately
retriggered `.dirty` — confirmed the git-metadata-skip idea was needed, not just a
smarter heredoc scan. This round adds two independent layers instead of one more
single-point patch; not yet pushed, not re-run against the scratch-folder clone (only
unit- and stdin-tested).

## Current Issues
- Bash write-pattern detection is heuristic, not a real shell parser. Exotic constructs
  (subshells, variable expansion, backticks) in *non-git* commands are still out of
  scope. README "ข้อจำกัด v1.1" not yet updated for rounds 3-4.
- Committing `.ai/*.md` with code is a documented convention only, not hook-enforced.
- 4 real failures of the same bug family this session, each from the *previous* fix's
  blind spot: (1) `->` arrow read as redirect; (2) bare `>` in prose read the same way
  after (1)'s patch → root-caused via `shlex` tokenizing (D-005); (3) `strip_heredocs()`
  (a quote-*unaware* regex scan) misfired because it doesn't know `<<'EOF'` appearing
  *inside* a quoted `-m` string isn't a real heredoc → truncated the command and left a
  stray `>` token; (4) **this round**: rewrote `strip_heredocs()` to track quote state
  char-by-char (so `<<` only starts a heredoc when unquoted — matches real shell
  grammar) AND stopped truncating when no terminator is found. Additionally added
  `SAFE_GIT_SUBCOMMANDS` — `git status/log/diff/show/branch/tag/remote/config/blame/
  reflog/fetch/add/commit/push` are skipped for write-scanning entirely, since none of
  them rewrite project-file content as a side effect. This is deliberate defense in
  depth: all 4 failures happened inside `git commit -m ...`, so even if some future text
  pattern defeats the quote-aware scan, this class of command is never scanned at all.

## Last Completed
Rewrote `strip_heredocs()` to be quote-aware (single-pass, tracks `'`/`"` state,
recognizes `<<` only when unquoted, no longer truncates on missing terminator). Added
`SAFE_GIT_SUBCOMMANDS` skip. Verified 21/21 cases: all 4 real failures from this session
(reconstructed from the exact commit text where possible) plus redirects, cp/mv/tee/
touch/sed -i, ambiguous commands, heredocs with real redirects, and mixed git+real-write
chains. Not yet committed.

## Next Action
Commit + push (plain `-m` this time, though it shouldn't matter anymore since `git
commit` is now skipped entirely regardless of its message). Verify `.ai/.dirty` stays
clear after that commit before calling this settled. Then update README "ข้อจำกัด v1.1".
