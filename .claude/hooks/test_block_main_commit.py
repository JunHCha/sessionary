"""Tests for block-main-commit hook."""

import subprocess
import sys
import json


def run_hook(command: str, branch: str) -> tuple[int, str, str]:
    """Run the hook script with given command and branch."""
    env = {"CURRENT_BRANCH": branch}
    input_data = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})

    result = subprocess.run(
        [sys.executable, "block_main_commit.py"],
        input=input_data,
        capture_output=True,
        text=True,
        cwd="/Users/chajunhyeong/Desktop/repo/sessionary/.claude/hooks",
        env={**env, "PATH": "/usr/bin:/bin"}
    )
    return result.returncode, result.stdout, result.stderr


class TestBlockMainCommit:
    """Test cases for main branch protection hook."""

    def test_block_git_commit_on_main(self):
        """Should block git commit on main branch."""
        code, stdout, _ = run_hook("git commit -m 'test'", "main")
        assert code == 2
        assert "main" in stdout.lower() or "block" in stdout.lower()

    def test_block_git_commit_on_master(self):
        """Should block git commit on master branch."""
        code, stdout, _ = run_hook("git commit -m 'test'", "master")
        assert code == 2

    def test_block_git_push_on_main(self):
        """Should block git push on main branch."""
        code, stdout, _ = run_hook("git push origin main", "main")
        assert code == 2

    def test_allow_git_commit_on_feature_branch(self):
        """Should allow git commit on feature branches."""
        code, _, _ = run_hook("git commit -m 'test'", "feature/test")
        assert code == 0

    def test_allow_git_push_on_feature_branch(self):
        """Should allow git push on feature branches."""
        code, _, _ = run_hook("git push origin feature/test", "feature/test")
        assert code == 0

    def test_allow_non_git_commands(self):
        """Should allow non-git commands."""
        code, _, _ = run_hook("ls -la", "main")
        assert code == 0

    def test_allow_git_status_on_main(self):
        """Should allow git status on main branch."""
        code, _, _ = run_hook("git status", "main")
        assert code == 0

    def test_allow_git_log_on_main(self):
        """Should allow git log on main branch."""
        code, _, _ = run_hook("git log --oneline", "main")
        assert code == 0

    def test_block_git_commit_amend_on_main(self):
        """Should block git commit --amend on main branch."""
        code, _, _ = run_hook("git commit --amend", "main")
        assert code == 2


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
