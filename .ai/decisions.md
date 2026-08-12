# Decision Log

## D-001 — Shared AI Project Memory

**Status:** Accepted

**Decision:**
Use `.ai/` as the shared project memory directory for Codex and Claude Code.

**Reason:**
Both agents should read and maintain the same project state instead of creating separate memory systems.

---

## D-002 — Runtime Lifecycle Hooks

**Status:** Accepted

**Decision:**
Use runtime lifecycle hooks to load and protect project memory.

**Reason:**
Critical memory behavior must not depend only on the model remembering to read or update files.

---

## D-003 — Bash writes detected via regex patterns, not asked in CLAUDE.md

**Status:** Accepted

**Decision:**
Extend PostToolUse change detection to the `Bash` tool using regex patterns for common
write commands (`>`, `>>`, `cp`, `mv`, `tee`, `touch`, `sed -i`), with a broad dirty
fallback for ambiguous write commands (`git apply`, `patch`, `rsync -a`, installs).

**Reason:**
User proposed telling the agent in CLAUDE.md/AGENTS.md to flag `.dirty` manually
instead. Rejected per D-002. Superseded by D-005 (regex proved unreliable).

---

## D-004 — Project named "Agent Memory Bridge"

**Status:** Accepted

**Decision:**
Rename the project (was "AI Project Memory Universal") to **Agent Memory Bridge**.
GitHub remote already uses this name: `github.com/pornthepp/Agent-Memory-Bridge`.

**Reason:**
User picked it from suggested names; reflects the tool's function — bridges project
memory across agents and sessions.

---

## D-005 — Supersedes D-003: tokenize Bash commands instead of regex-scanning them

**Status:** Accepted

**Decision:**
Detect Bash write targets by `shlex.split()`-tokenizing the command, not by regex over
the raw string.

**Reason:**
D-003's regex broke twice on real commit messages (`->` arrows, bare `>` in prose) —
text inside a quoted `-m` argument that regex can't tell from shell syntax.

**Round 3:** shlex alone wasn't enough — a heredoc-built commit message desynced
shlex's quote-tracking (shlex has no heredoc concept). Added `strip_heredocs()`, but as
a quote-*unaware* regex scan it also misfired.

**Round 4:** rewrote `strip_heredocs()` quote-aware (tracks `'`/`"`, only treats `<<` as
a heredoc when unquoted, no longer truncates on missing terminator). Added
`SAFE_GIT_SUBCOMMANDS`: skip scanning entirely for `status/log/diff/.../commit/push` —
none rewrite project files, and all 4 failures happened inside one of them. Two
independent layers now. 21/21 cases pass.
