#!/usr/bin/env python3

"""
A system level tool to process the claude code Notification hook event.

Sends notifications to Hammerspoon via hs.urlevent for canvas overlay display.

See https://code.claude.com/docs/en/hooks for more details.
"""

import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlencode


def send_notification(repo_name: str, hook_event_name: str, message: str) -> None:
    """Send notification to Hammerspoon via URL event."""
    params = urlencode(
        {
            "repo_name": repo_name,
            "hook_event_name": hook_event_name,
            "message": message,
        }
    )
    url = f"hammerspoon://claude-notify?{params}"

    # Use -g flag to open in background (avoid focus change)
    subprocess.run(["open", "-g", url], check=False)


def main() -> int:
    """Process Claude Code notification hook and send notification."""
    data = json.load(sys.stdin)

    cwd = data.get("cwd", "")
    hook_event_name = data.get("hook_event_name", "")
    notification_type = data.get("notification_type", "")
    message = data.get("message", "No message found")
    message = message[:50]

    if notification_type == "idle_prompt":
        return 0

    repo_name = Path(cwd).name if cwd else "Claude Code"
    send_notification(repo_name, hook_event_name, message)

    return 0


if __name__ == "__main__":
    sys.exit(main())
