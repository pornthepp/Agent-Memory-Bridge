from pathlib import Path
from memory_common import project_root

root = project_root()

memory_files = [
    root / ".ai" / "state.md",
    root / ".ai" / "plan.md",
    root / ".ai" / "decisions.md",
]

recovery_file = root / ".ai" / "precompact-recovery.md"

parts = ["=== PROJECT MEMORY ==="]

for file in memory_files:
    parts.append(f"\n--- {file.name} ---")

    if file.exists():
        parts.append(file.read_text(encoding="utf-8"))
    else:
        parts.append("File not found.")

if recovery_file.exists():
    parts.append("\n!!! PRE-COMPACT RECOVERY REQUIRED !!!")
    parts.append(recovery_file.read_text(encoding="utf-8"))

parts.append("\n=== END PROJECT MEMORY ===")

output = "\n".join(parts)

# Keep injected context below Claude Code's 10,000-character hook-output cap.
if len(output) > 9500:
    output = (
        output[:9000]
        + "\n\n[PROJECT MEMORY TRUNCATED: run scripts/validate_memory.py and reduce memory size.]"
    )

print(output)
