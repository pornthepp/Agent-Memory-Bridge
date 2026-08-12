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

**Round 3-4 (proactive, not independently confirmed live):** added quote-aware
`strip_heredocs()` (heredocs are a real shlex blind spot) and `SAFE_GIT_SUBCOMMANDS` —
skip scanning entirely for `status/log/diff/.../commit/push`, which never rewrite
project files. Session-internal claims that these rounds fixed a *live* recurrence were
later found to rest on a flawed test (checking `.dirty` right after `git commit`, which
never clears it — only the Stop hook does). Code kept regardless: correct, well-tested
(21/21 cases), reduces real attack surface even without a proven live trigger.
