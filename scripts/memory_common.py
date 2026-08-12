import os
from pathlib import Path


def project_root(event_cwd=None) -> Path:
    """
    Resolve the project root for both Claude Code and Codex.
    Claude Code exposes CLAUDE_PROJECT_DIR.
    Otherwise, walk upward from event cwd / process cwd until .ai is found.
    """
    claude_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if claude_root:
        return Path(claude_root).resolve()

    start = Path(event_cwd or Path.cwd()).resolve()

    for candidate in (start, *start.parents):
        if (candidate / ".ai").exists():
            return candidate

    return start
