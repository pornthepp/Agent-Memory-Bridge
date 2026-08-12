# Decision Log

## D-001 — Shared AI Project Memory

**Status:** Accepted

**Decision:**
Use `.ai/` as the shared project memory directory for Codex and Claude Code.

**Reason:**
Both agents should read/maintain the same project state, not separate memory systems.

---

## D-002 — Runtime Lifecycle Hooks

**Status:** Accepted

**Decision:**
Use runtime lifecycle hooks to load and protect project memory.

**Reason:**
Critical memory behavior must not depend only on the model remembering to update files.

---

## D-003 — Bash writes: detect via hook, not a CLAUDE.md ask (Superseded by D-005)

**Status:** Superseded

**Decision:** Extended `PostToolUse` to `Bash` via regex patterns, mechanically —
rejected the alternative of asking the agent to flag `.dirty` manually (per D-002).
Regex itself proved unreliable; see D-005.

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

**Round 3-4 (proactive, not confirmed live):** added quote-aware `strip_heredocs()` and
`SAFE_GIT_SUBCOMMANDS` skip-scan. "Fixed a live recurrence" claims rested on a flawed
test (`.dirty` only clears via the Stop hook, not `git commit`). Code kept: correct,
well-tested (21/21 cases).

---

## D-006 — Antigravity: no SessionStart/PreCompact hook, fallback via AGENTS.md

**Status:** Accepted

**Decision:**
Antigravity has no `SessionStart`/`PreCompact`-equivalent hook (confirmed: only
`PreToolUse`/`PostToolUse`/`PreInvocation`/`PostInvocation`/`Stop` exist). Full
`hooks.json` support deferred. Instead, `AGENTS.md` (auto-loaded natively by
Antigravity) now tells non-hook agents to read `.ai/*.md` themselves as step one.

**Reason:**
Closes the worst gap (memory never loading) at zero engineering cost, without
committing to the bigger hooks.json integration yet.
