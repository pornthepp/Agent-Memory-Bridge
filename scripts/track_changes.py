import json
import re
import sys
from pathlib import Path

from memory_common import project_root


data = json.load(sys.stdin)

root = project_root(data.get("cwd"))
ai_dir = (root / ".ai").resolve()
dirty = ai_dir / ".dirty"

ai_dir.mkdir(exist_ok=True)

tool_name = str(data.get("tool_name", ""))
tool_input = data.get("tool_input") or {}

changed_files = []
ambiguous_write = False


def add_path(raw_path):
    if not raw_path:
        return

    path = Path(str(raw_path))

    if not path.is_absolute():
        path = root / path

    try:
        changed_files.append(path.resolve())
    except Exception:
        pass


# Claude Code built-in file editing tools.
if tool_name in {"Write", "Edit"}:
    add_path(tool_input.get("file_path"))

elif tool_name == "NotebookEdit":
    add_path(tool_input.get("notebook_path"))

# Claude Code Bash tool: shell commands that write files.
elif tool_name == "Bash":
    command = str(tool_input.get("command", ""))

    # > file / >> file (skip fd dup like 2>&1)
    for match in re.finditer(r"(?<![0-9&])>{1,2}(?!&)\s*([^\s;&|<>]+)", command):
        add_path(match.group(1).strip("\"'"))

    # cp / mv src... dest  (last whitespace token is the destination)
    for match in re.finditer(r"\b(?:cp|mv)\s+(?:-\S+\s+)*.+?\s(\S+)\s*(?:[;&|]|$)", command):
        add_path(match.group(1).strip("\"'"))

    # tee [-a] file
    for match in re.finditer(r"\btee\b\s+(?:-\S+\s+)*(\S+)", command):
        add_path(match.group(1).strip("\"'"))

    # touch file [file ...]
    for match in re.finditer(r"\btouch\s+(.+?)\s*(?:[;&|]|$)", command):
        for token in match.group(1).split():
            add_path(token.strip("\"'"))

    # sed -i ... file
    for match in re.finditer(r"\bsed\s+-i\S*\s+.+?\s(\S+)\s*(?:[;&|]|$)", command):
        add_path(match.group(1).strip("\"'"))

    # Commands that write files but whose target isn't a plain argument
    # (git apply, patch, rsync -a, package installs). Can't pinpoint the
    # file, so if nothing else matched, fall back to marking dirty.
    if not changed_files and re.search(
        r"\b(git\s+apply|git\s+checkout\s+--|patch\b|rsync\b[^\n]*-a|npm\s+install|pip\s+install)\b",
        command,
    ):
        ambiguous_write = True

# Codex apply_patch PostToolUse.
elif tool_name == "apply_patch" or "command" in tool_input:
    command = str(tool_input.get("command", ""))

    patch_files = re.findall(
        r"^\*\*\*\s+(?:Add|Update|Delete)\s+File:\s*(.+?)\s*$",
        command,
        flags=re.MULTILINE,
    )

    for file_name in patch_files:
        add_path(file_name.strip().strip("\"'"))


def is_inside(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


project_files = [
    path
    for path in changed_files
    if is_inside(path, root) and not is_inside(path, ai_dir)
]

if project_files or ambiguous_write:
    dirty.write_text(
        "Project has uncheckpointed changes.\n",
        encoding="utf-8",
    )
