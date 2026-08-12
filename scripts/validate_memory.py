from pathlib import Path
import sys

from memory_common import project_root


root = project_root()
ai_dir = root / ".ai"

STATE = ai_dir / "state.md"
PLAN = ai_dir / "plan.md"
DECISIONS = ai_dir / "decisions.md"

errors = []


def read_file(path: Path) -> str:
    if not path.exists():
        errors.append(f"Missing file: {path}")
        return ""

    text = path.read_text(encoding="utf-8").strip()

    if not text:
        errors.append(f"Empty file: {path}")

    return text


def require_sections(filename: str, text: str, sections: list[str]):
    for section in sections:
        if section not in text:
            errors.append(f"{filename}: missing section `{section}`")


state = read_file(STATE)
plan = read_file(PLAN)
decisions = read_file(DECISIONS)

require_sections(
    "state.md",
    state,
    [
        "## Current Phase",
        "## Current Status",
        "## In Progress",
        "## Current Issues",
        "## Last Completed",
        "## Next Action",
    ],
)

require_sections(
    "plan.md",
    plan,
    [
        "## Goal",
        "## Current Phase",
        "## Completed Milestones",
        "## Current Tasks",
        "## Next Milestone",
    ],
)

if decisions and "# Decision Log" not in decisions:
    errors.append("decisions.md: missing `# Decision Log`")

# SessionStart hook output is capped at 10,000 characters in Claude Code.
# Keep the normal injected memory comfortably below that limit.
if len(state) > 3500:
    errors.append("state.md is too large (> 3500 characters)")

if len(plan) > 3500:
    errors.append("plan.md is too large (> 3500 characters)")

if len(decisions) > 2500:
    errors.append("decisions.md is too large (> 2500 characters)")

if len(state) + len(plan) + len(decisions) > 8500:
    errors.append("combined project memory is too large (> 8500 characters)")

if errors:
    print("MEMORY VALIDATION FAILED")
    print()

    for error in errors:
        print(f"- {error}")

    sys.exit(1)

print("MEMORY VALIDATION PASSED")
sys.exit(0)
