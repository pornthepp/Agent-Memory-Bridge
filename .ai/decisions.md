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
User proposed instead telling the agent in CLAUDE.md/AGENTS.md to manually flag `.dirty`
after Bash writes. Rejected per D-002: that reintroduces dependence on the model
remembering. Detection stays hook-side (mechanical), even though the regex approach is
best-effort, not a full shell parser — see README "ข้อจำกัด v1.1".

---

## D-004 — Project named "Agent Memory Bridge"

**Status:** Accepted

**Decision:**
Rename the project (was "AI Project Memory Universal") to **Agent Memory Bridge**.
GitHub remote already uses this name: `github.com/pornthepp/Agent-Memory-Bridge`.

**Reason:**
User picked it from suggested names; reflects what the tool actually does — bridges
project memory across agents (Codex ↔ Claude Code) and across sessions.

---

## D-005 — Supersedes D-003: tokenize Bash commands instead of regex-scanning them

**Status:** Accepted

**Decision:**
Detect Bash write targets by `shlex.split()`-tokenizing the command, not by regex over
the raw string.

**Reason:**
D-003's regex approach broke twice on real commit messages: first `->` arrows read as
redirects, then (after patching that) a bare `>` in prose ("before > in the lookbehind")
read the same way. Both were text inside a quoted `-m` argument. Regex can't reliably
tell quoted text from shell syntax without re-implementing a shell tokenizer — so use
`shlex`, which already does that: quoted text becomes one token, and `>`/`>>` only match
as their own unquoted token.
