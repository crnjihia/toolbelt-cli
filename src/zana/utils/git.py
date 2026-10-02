"""Git wrapper utilities for Zana CLI."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


def run_git(args: list[str], cwd: Path | None = None) -> str:
    """Run a git command, returning stdout as text."""
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        err = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"Git command failed: git {' '.join(args)}\n{err}")
    return result.stdout.strip()


def get_git_user_name(cwd: Path | None = None) -> str:
    """Return user.name from git config, environment, or empty string."""
    try:
        name = run_git(["config", "user.name"], cwd=cwd)
        if name:
            return name
    except Exception:
        pass
    return (
        os.getenv("GIT_AUTHOR_NAME") or os.getenv("USER") or os.getenv("USERNAME") or ""
    )


def git_diff_staged(cwd: Path | None = None) -> str:
    """Return diff of staged changes."""
    return run_git(["diff", "--staged"], cwd=cwd)


def git_commit(message: str, cwd: Path | None = None) -> None:
    """Create a commit with the given message."""
    run_git(["commit", "-m", message], cwd=cwd)


def is_git_repo(cwd: Path | None = None) -> bool:
    """Check if the directory is inside a git repository."""
    try:
        run_git(["rev-parse", "--is-inside-work-tree"], cwd=cwd)
        return True
    except Exception:
        return False
