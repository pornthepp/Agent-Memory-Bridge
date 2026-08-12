import json
import re
import shlex
import sys
from pathlib import Path

from memory_common import project_root

SEPARATORS = {"&&", "||", ";", "|"}

HEREDOC_START_RE = re.compile(
    r"<<-?\s*(?:'([^']*)'|\"([^\"]*)\"|([A-Za-z_][A-Za-z0-9_]*))"
)


def strip_heredocs(command):
    """Remove heredoc bodies (`<<'EOF' ... EOF`) before tokenizing.

    shlex has no concept of heredocs — it just tracks bare quote characters.
    A heredoc body (e.g. a multi-line commit message built via
    `$(cat <<'EOF' ... EOF)`) commonly contains its own literal quote marks
    ("like this"), which desyncs shlex's quote-tracking and can make
    unrelated later text look like it's outside any quote. Heredoc bodies
    are never real shell syntax, so drop them before scanning for anything.
    """
    out = []
    pos = 0

    while True:
        match = HEREDOC_START_RE.search(command, pos)
        if not match:
            out.append(command[pos:])
            break

        delim = match.group(1) or match.group(2) or match.group(3)
        line_end = command.find("\n", match.end())

        if line_end == -1:
            out.append(command[pos:])
            break

        # Keep the heredoc marker's own line (it may carry real syntax,
        # e.g. `cat <<EOF > out.txt`); drop everything from the body on.
        out.append(command[pos:line_end + 1])

        terminator = re.compile(
            r"^[ \t]*" + re.escape(delim) + r"[ \t]*$", re.MULTILINE
        )
        term_match = terminator.search(command, line_end + 1)

        if not term_match:
            pos = len(command)
            break

        pos = term_match.end()
        if pos < len(command) and command[pos] == "\n":
            pos += 1

    return "".join(out)


def bash_write_targets(command):
    """Tokenize a Bash command (respecting quotes) and find write targets.

    Using shlex instead of scanning the raw string means text inside quotes
    (e.g. a git commit message containing "->" or a bare ">") is never
    mistaken for shell syntax — it's just part of one token.
    """
    command = strip_heredocs(command)

    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        # Unbalanced quotes: can't safely tokenize, skip detection this run
        # rather than guess.
        return [], False

    groups = [[]]
    for tok in tokens:
        if tok in SEPARATORS:
            groups.append([])
        else:
            groups[-1].append(tok)

    targets = []
    ambiguous = False

    for group in groups:
        if not group:
            continue

        for i, tok in enumerate(group):
            if tok in (">", ">>") and i + 1 < len(group):
                targets.append(group[i + 1])

        head = group[0]
        rest = group[1:]
        non_flags = [t for t in rest if not t.startswith("-")]

        if head in ("cp", "mv"):
            if non_flags:
                targets.append(non_flags[-1])
        elif head == "tee":
            if non_flags:
                targets.append(non_flags[0])
        elif head == "touch":
            targets.extend(non_flags)
        elif head == "sed" and any(f.startswith("-i") for f in rest if f.startswith("-")):
            if non_flags:
                targets.append(non_flags[-1])
        elif head == "git" and rest[:1] == ["apply"]:
            ambiguous = True
        elif head == "git" and "checkout" in rest and "--" in rest:
            ambiguous = True
        elif head == "patch":
            ambiguous = True
        elif head == "rsync" and any(f.startswith("-") and "a" in f for f in rest):
            ambiguous = True
        elif head in ("npm", "pip") and rest[:1] == ["install"]:
            ambiguous = True

    return targets, ambiguous


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
    targets, ambiguous = bash_write_targets(command)

    for target in targets:
        add_path(target)

    # Commands that write files but whose target isn't a plain argument
    # (git apply, patch, rsync -a, package installs). Can't pinpoint the
    # file, so if nothing else matched, fall back to marking dirty.
    if not changed_files and ambiguous:
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
