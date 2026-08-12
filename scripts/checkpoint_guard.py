import json
import subprocess
import sys

from memory_common import project_root


data = json.load(sys.stdin)

root = project_root(data.get("cwd"))
ai_dir = root / ".ai"

DIRTY = ai_dir / ".dirty"
STATE = ai_dir / "state.md"
PLAN = ai_dir / "plan.md"
RECOVERY = ai_dir / "precompact-recovery.md"
RETRY = ai_dir / ".checkpoint-retry"

VALIDATOR = root / "scripts" / "validate_memory.py"

MAX_RETRIES = 2


def get_retry_count():
    if not RETRY.exists():
        return 0

    try:
        return int(RETRY.read_text(encoding="utf-8").strip())
    except Exception:
        return 0


def increment_retry():
    count = get_retry_count() + 1
    RETRY.write_text(str(count), encoding="utf-8")
    return count


# No project change: allow stop.
if not DIRTY.exists():
    RETRY.unlink(missing_ok=True)
    print(json.dumps({"continue": True}))
    sys.exit(0)


dirty_time = DIRTY.stat().st_mtime_ns

state_ok = STATE.exists() and STATE.stat().st_mtime_ns > dirty_time
plan_ok = PLAN.exists() and PLAN.stat().st_mtime_ns > dirty_time


# Memory is stale: force the agent to update it.
if not state_ok or not plan_ok:
    missing = []

    if not state_ok:
        missing.append(".ai/state.md")

    if not plan_ok:
        missing.append(".ai/plan.md")

    reason = (
        "PROJECT CHECKPOINT REQUIRED.\n\n"
        "Project files changed after the last memory checkpoint.\n\n"
        "Update these files before finishing:\n"
        + "\n".join(f"- {x}" for x in missing)
        + "\n\n"
        "state.md must describe the actual current project state, "
        "completed work, issues, and next action.\n"
        "plan.md must reflect completed and upcoming milestone-level work.\n"
        "Do not update decisions.md unless an important project decision was made.\n"
        "Do not manually delete runtime flag files."
    )

    print(json.dumps({
        "decision": "block",
        "reason": reason
    }))

    sys.exit(0)


# Memory timestamps are fresh; validate content/format.
result = subprocess.run(
    [sys.executable, str(VALIDATOR)],
    cwd=str(root),
    capture_output=True,
    text=True,
)

if result.returncode == 0:
    DIRTY.unlink(missing_ok=True)
    RECOVERY.unlink(missing_ok=True)
    RETRY.unlink(missing_ok=True)

    print(json.dumps({"continue": True}))
    sys.exit(0)


validation_error = (
    result.stdout.strip()
    or result.stderr.strip()
    or "Unknown memory validation error."
)

retry_count = increment_retry()

if retry_count <= MAX_RETRIES:
    print(json.dumps({
        "decision": "block",
        "reason":
            "PROJECT MEMORY VALIDATION FAILED.\n\n"
            + validation_error
            + "\n\n"
            + f"Correction attempt {retry_count}/{MAX_RETRIES}.\n"
            + "Fix the project memory files before finishing."
    }))

    sys.exit(0)


# Fail open after bounded retries, but preserve dirty state for manual review.
print(json.dumps({
    "continue": True,
    "systemMessage":
        "WARNING: Project memory validation failed "
        f"after {MAX_RETRIES} correction attempts.\n"
        "The .dirty flag has been preserved for manual review.\n\n"
        + validation_error
}))

sys.exit(0)
