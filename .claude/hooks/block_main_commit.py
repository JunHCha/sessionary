#!/usr/bin/env python3
"""
Claude Code PreToolUse Hook: Block git commit/push on main branch.

Exit codes:
- 0: Allow the command
- 2: Block the command with message
"""

import json
import os
import shlex
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


def parse_git_subcommand(command: str) -> tuple[str | None, list[str]]:
    """Parse git subcommand and args, tolerating global options."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        return None, []

    if not tokens or tokens[0] != "git":
        return None, []

    i = 1
    # Skip global options like -C, -c, --git-dir, --work-tree
    while i < len(tokens) and tokens[i].startswith("-"):
        if tokens[i] in ("-C", "-c", "--git-dir", "--work-tree") and i + 1 < len(tokens):
            i += 2
        else:
            i += 1

    if i >= len(tokens):
        return None, []

    return tokens[i], tokens[i + 1:]


def push_targets_protected(args: list[str]) -> bool:
    """Check if push targets a protected branch."""
    protected = {"main", "master", "refs/heads/main", "refs/heads/master"}
    for arg in args:
        if arg.startswith("-"):
            continue
        if ":" in arg:
            # Handle refspec like HEAD:main or :main
            _, dst = arg.split(":", 1)
            if dst in protected:
                return True
        elif arg in protected:
            return True
    return False


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

    # Parse git subcommand
    subcmd, args = parse_git_subcommand(command)
    if subcmd not in ("commit", "push"):
        sys.exit(0)

    # Check current branch
    branch = get_current_branch()

    # For commit: block if on protected branch
    if subcmd == "commit":
        if not is_protected_branch(branch):
            sys.exit(0)
    # For push: block if on protected branch OR pushing to protected branch
    else:
        if not is_protected_branch(branch) and not push_targets_protected(args):
            sys.exit(0)

    # Block the command
    print(f"BLOCKED: git {subcmd} on protected branch '{branch}'")
    print("")
    print("Direct commits to main/master are not allowed.")
    print("Please create a feature branch first:")
    print("  git checkout -b feature/your-feature-name")
    sys.exit(2)


if __name__ == "__main__":
    main()
