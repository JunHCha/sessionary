#!/usr/bin/env python3
"""
Claude Code PreToolUse Hook: Block git commit/push on main branch.

Exit codes:
- 0: Allow the command
- 2: Block the command with message
"""

import json
import os
import re
import subprocess
import sys


def get_current_branch() -> str:
    """Get current git branch name."""
    # Check environment variable first (for testing)
    if "CURRENT_BRANCH" in os.environ:
        return os.environ["CURRENT_BRANCH"]

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except Exception:
        return ""


def is_protected_branch(branch: str) -> bool:
    """Check if branch is protected (main or master)."""
    return branch in ("main", "master")


def is_git_commit_or_push(command: str) -> bool:
    """Check if command is git commit or git push."""
    # Pattern to match git commit or git push commands
    patterns = [
        r"\bgit\s+commit\b",
        r"\bgit\s+push\b",
    ]
    return any(re.search(pattern, command) for pattern in patterns)


def main():
    """Main hook logic."""
    # Read input from stdin
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        sys.exit(0)  # Allow on invalid input

    # Only process Bash tool calls
    tool_name = input_data.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    # Get command from tool input
    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    if not command:
        sys.exit(0)

    # Check if it's a git commit/push command
    if not is_git_commit_or_push(command):
        sys.exit(0)

    # Check current branch
    branch = get_current_branch()
    if not is_protected_branch(branch):
        sys.exit(0)

    # Block the command
    print(f"BLOCKED: git commit/push on protected branch '{branch}'")
    print("")
    print("Direct commits to main/master are not allowed.")
    print("Please create a feature branch first:")
    print("  git checkout -b feature/your-feature-name")
    sys.exit(2)


if __name__ == "__main__":
    main()
