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
Real end-to-end test completed: cloned the pushed repo into a scratch folder
(`%TEMP%/claude/.../scratchpad/amb-test/repo`, not inside this repo), reset its
`.ai/*.md` to fresh-install content, scaffolded `calculator.py`, and drove
`session_start.py` / `track_changes.py` / `checkpoint_guard.py` / `precompact_guard.py`
against that clone with `CLAUDE_PROJECT_DIR` overridden to the clone path (a live second
Claude Code session can't be opened from here, so this simulates the exact env/JSON
Claude Code would send). All 4 hooks behaved correctly. Scratch folder still exists;
user said they'd delete it later.

## Current Issues
- Bash write-pattern detection (`scripts/track_changes.py`) is regex-based, not a real
  shell parser. Known gaps documented in README.md "ข้อจำกัด v1.1".
- Committing `.ai/*.md` with code is a documented convention only, not hook-enforced.
- FIXED: `>`/`>>` regex misread prose arrows (`->`, `=>` in commit messages) as
  redirection, falsely setting `.dirty`. Reproduced in the clone too (confirmed real,
  not a local artifact), then fixed there and verified.
- FIXED, MORE SEVERE: `session_start.py` crashed with `UnicodeEncodeError` on Windows
  whenever `.ai/*.md` contained non-ASCII text (this repo's `decisions.md` has Thai in
  D-003/D-004). Root cause: Python's stdout defaults to the console codepage (cp1252)
  on Windows, not UTF-8. This reproduced on the actual live repo, not just the clone —
  **the next real SessionStart on this machine would have crashed and silently failed
  to load memory** until fixed just now (`sys.stdout.reconfigure(encoding="utf-8")`).
  Verified fixed on both this repo and the clone.

## Last Completed
Ran a full hook-cycle test against a fresh clone: SessionStart (crashed, fixed, then
passed), PostToolUse(Write) on `calculator.py` (dirty set correctly), Stop checkpoint
(blocked while stale, passed + cleared `.dirty` after honest memory update), Bash-arrow
false positive (reproduced, fixed, verified — real redirects still detected),
PreCompact guard (wrote `precompact-recovery.md` correctly). `calculator.py` itself runs
correctly (5, 3, 24, 5.0).

## Next Action
Commit + push both fixes (`session_start.py` UTF-8 fix, `track_changes.py` arrow fix)
and this checkpoint. Consider applying the same `sys.stdout.reconfigure` defensively to
other scripts if they ever print non-ASCII content directly (currently they only print
`json.dumps(...)`, which auto-escapes non-ASCII, so they're not at risk today).
