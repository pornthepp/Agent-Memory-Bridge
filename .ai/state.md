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
None — regex-based Bash detection was replaced with a tokenizer-based approach after a
second false positive recurred (see Current Issues). Fresh-clone test (scratch folder,
`calculator.py`, all 4 hooks) from earlier this session still stands; not re-run after
this rewrite but the underlying function was unit-tested directly (16 cases, see Last
Completed).

## Current Issues
- Bash write-pattern detection is still heuristic, not a real shell parser — now
  tokenizes with `shlex.split()` instead of regex-scanning raw text, which eliminates
  "quoted text looks like shell syntax" false positives. Exotic constructs (subshells,
  variable expansion, backticks) are still out of scope. README "ข้อจำกัด v1.1" not yet
  updated to match.
- Committing `.ai/*.md` with code is a documented convention only, not hook-enforced.
- ROOT-CAUSED (D-005): the `->`-arrow regex patch (`a3859fd`) broke again almost
  immediately on a different commit message with a bare `>` in prose ("before > in the
  lookbehind" → misread as redirect to file "in"). Root cause: regex scanned the whole
  raw string, so quoted-argument text was indistinguishable from real shell syntax.
  Rewrote around `shlex.split()` — quoted text becomes one token, so `>`/`>>` inside
  quotes can never be misread. See D-005 in decisions.md.

## Last Completed
Rewrote Bash write-detection: `bash_write_targets()` tokenizes with `shlex`, splits on
`&&`/`||`/`;`/`|`, exact-token match on `>`/`>>`, per-subcommand cp/mv/tee/touch/sed -i,
ambiguous-write flag for git apply/checkout --/patch/rsync -a/npm|pip install.
Unit-tested 16/16 (both real failing commit messages + real redirects + all other
patterns) and end-to-end via stdin JSON. Not yet committed.

## Next Action
Commit + push. Update README "ข้อจำกัด v1.1" to describe the tokenizer, not the old
regex list.
