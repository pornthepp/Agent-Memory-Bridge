import json
import sys
from datetime import datetime

from memory_common import project_root


data = json.load(sys.stdin)

root = project_root(data.get("cwd"))
ai_dir = root / ".ai"
dirty_file = ai_dir / ".dirty"
recovery_file = ai_dir / "precompact-recovery.md"

trigger = data.get("trigger", "unknown")
session_id = data.get("session_id", "unknown")
turn_id = data.get("turn_id", data.get("prompt_id", "unknown"))

ai_dir.mkdir(exist_ok=True)

if not dirty_file.exists():
    # Empty valid JSON is safe for both Codex and Claude Code.
    print(json.dumps({"continue": True}))
    sys.exit(0)

content = f"""# Pre-Compact Recovery

## Status
UNCOMMITTED PROJECT MEMORY DETECTED

## What Happened
Project files were modified but the project memory checkpoint
was not completed before context compaction.

## Recovery Required
After compaction:

1. Treat `.ai/state.md` and `.ai/plan.md` as potentially stale.
2. Inspect the actual project files and current changes.
3. Continue the current task.
4. Before finishing, reconcile and update project memory.
5. Do not remove `.dirty` manually.

## Metadata
- Trigger: {trigger}
- Session: {session_id}
- Turn: {turn_id}
- Created: {datetime.now().isoformat()}
"""

recovery_file.write_text(content, encoding="utf-8")

# Claude Code discards systemMessage/continue on PreCompact, but the file side-effect remains.
# Codex may surface the message.
print(json.dumps({
    "continue": True,
    "systemMessage":
        "Uncheckpointed project changes detected. "
        "Recovery state saved before compaction."
}))
