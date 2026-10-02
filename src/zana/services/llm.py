"""Anthropic Claude LLM wrapper with rule-based fallback commit generator."""

from __future__ import annotations

import os
import re
from typing import Any

import anthropic

DEFAULT_MODEL = "claude-sonnet-4"

SYSTEM_PROMPT = (
    "You generate Conventional Commits messages. Given a git diff, output ONLY "
    "the commit message. Format: <type>(<scope>): <subject>\n\n<body if needed>. "
    "Types: feat, fix, docs, style, refactor, test, chore. Max 72 chars for subject."
)


class CommitMessageGenerator:
    """Generate Conventional Commit messages from a git diff."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")

    def generate(
        self,
        diff: str,
        commit_type: str | None = None,
        scope: str | None = None,
    ) -> str:
        """Generate a conventional commit message."""
        if self.api_key and self.api_key.strip():
            return self._call_claude(diff, commit_type, scope)
        return self._fallback(diff, commit_type, scope)

    def _call_claude(
        self,
        diff: str,
        commit_type: str | None,
        scope: str | None,
    ) -> str:
        client = anthropic.Anthropic(api_key=self.api_key)
        user_prompt = diff
        instructions = []
        if commit_type:
            instructions.append(f"Commit type MUST be: {commit_type}")
        if scope:
            instructions.append(f"Commit scope MUST be: {scope}")
        if instructions:
            user_prompt = f"[{'; '.join(instructions)}]\n\n{diff}"

        response = client.messages.create(
            model=DEFAULT_MODEL,
            max_tokens=256,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )

        content: Any = response.content
        if isinstance(content, list) and content:
            item = content[0]
            if hasattr(item, "text"):
                return str(item.text).strip()
            if isinstance(item, dict) and "text" in item:
                return str(item["text"]).strip()
            return str(item).strip()
        if hasattr(content, "text"):
            return str(content.text).strip()
        return str(content).strip()

    def _fallback(
        self,
        diff: str,
        commit_type: str | None = None,
        scope: str | None = None,
    ) -> str:
        """Rule-based generator when no Anthropic API key is available."""
        lines = diff.splitlines()
        added = sum(
            1 for line in lines if line.startswith("+") and not line.startswith("+++")
        )
        removed = sum(
            1 for line in lines if line.startswith("-") and not line.startswith("---")
        )
        files = set(re.findall(r"^\+\+\+ b/(.+)$", diff, flags=re.MULTILINE))
        files_count = max(len(files), 1)

        if commit_type:
            guess_type = commit_type.strip()
        else:
            diff_lower = diff.lower()
            if any(term in diff_lower for term in ["test", "tests/"]):
                guess_type = "test"
            elif any(term in diff_lower for term in ["doc", "docs/", "readme"]):
                guess_type = "docs"
            elif any(term in diff_lower for term in [".css", ".scss", "style"]):
                guess_type = "style"
            else:
                guess_type = "chore"

        scope_part = f"({scope.strip()})" if scope and scope.strip() else ""
        file_label = "file" if files_count == 1 else "files"
        stats = f"(+{added}/-{removed} lines)"
        return f"{guess_type}{scope_part}: update {files_count} {file_label} {stats}"
