"""Tests for the `zana commit` command."""

from __future__ import annotations

from unittest import mock

import pytest
from typer.testing import CliRunner

from zana.cli import app

runner = CliRunner()

SAMPLE_DIFF = """diff --git a/src/index.ts b/src/index.ts
index 1234567..89abcdef 100644
--- a/src/index.ts
+++ b/src/index.ts
@@ -1,3 +1,5 @@
+export const VERSION = "1.0.0";
+export function run() {}
-oldFunction();
"""


def test_commit_empty_diff(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("zana.commands.commit.git_diff_staged", lambda: "")
    result = runner.invoke(app, ["commit"])
    assert result.exit_code == 1
    assert "Nothing staged. Run git add first." in result.stdout


def test_commit_dry_run(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("zana.commands.commit.git_diff_staged", lambda: SAMPLE_DIFF)
    mock_commit = mock.MagicMock()
    monkeypatch.setattr("zana.commands.commit.git_commit", mock_commit)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")

    result = runner.invoke(app, ["commit", "--dry-run"])
    assert result.exit_code == 0
    assert "Dry run – commit not performed." in result.stdout
    assert not mock_commit.called


def test_commit_fallback_with_yes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("zana.commands.commit.git_diff_staged", lambda: SAMPLE_DIFF)
    mock_commit = mock.MagicMock()
    monkeypatch.setattr("zana.commands.commit.git_commit", mock_commit)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")

    result = runner.invoke(app, ["commit", "--yes"])
    assert result.exit_code == 0
    assert mock_commit.called
    commit_msg = mock_commit.call_args[0][0]
    assert "update 1 file" in commit_msg.lower()
    assert "✅ Commit created successfully!" in result.stdout


def test_commit_fallback_with_type_and_scope(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("zana.commands.commit.git_diff_staged", lambda: SAMPLE_DIFF)
    mock_commit = mock.MagicMock()
    monkeypatch.setattr("zana.commands.commit.git_commit", mock_commit)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")

    result = runner.invoke(
        app, ["commit", "--type", "feat", "--scope", "parser", "--yes"]
    )
    assert result.exit_code == 0
    assert mock_commit.called
    commit_msg = mock_commit.call_args[0][0]
    assert commit_msg.startswith("feat(parser):")


def test_commit_with_anthropic(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("zana.commands.commit.git_diff_staged", lambda: SAMPLE_DIFF)
    mock_commit = mock.MagicMock()
    monkeypatch.setattr("zana.commands.commit.git_commit", mock_commit)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-api-key")

    mock_client = mock.MagicMock()
    mock_msg = mock.MagicMock()
    mock_msg.content = [
        {"type": "text", "text": "feat(core): export version constant and run helper"}
    ]
    mock_client.messages.create.return_value = mock_msg

    with mock.patch("anthropic.Anthropic", return_value=mock_client):
        result = runner.invoke(app, ["commit", "--yes"])
        assert result.exit_code == 0
        assert mock_commit.called
        assert (
            mock_commit.call_args[0][0]
            == "feat(core): export version constant and run helper"
        )

        # Verify system prompt passed to Claude
        call_kwargs = mock_client.messages.create.call_args[1]
        assert call_kwargs["model"] == "claude-sonnet-4"
        assert "Conventional Commits" in call_kwargs["system"]


def test_commit_user_abort(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("zana.commands.commit.git_diff_staged", lambda: SAMPLE_DIFF)
    mock_commit = mock.MagicMock()
    monkeypatch.setattr("zana.commands.commit.git_commit", mock_commit)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")

    result = runner.invoke(app, ["commit"], input="n\n")
    assert result.exit_code == 1
    assert "Commit aborted by user." in result.stdout
    assert not mock_commit.called


def test_commit_user_edit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("zana.commands.commit.git_diff_staged", lambda: SAMPLE_DIFF)
    mock_commit = mock.MagicMock()
    monkeypatch.setattr("zana.commands.commit.git_commit", mock_commit)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "")

    result = runner.invoke(
        app, ["commit"], input="edit\nfix(app): manually edited commit message\n"
    )
    assert result.exit_code == 0
    assert mock_commit.called
    assert mock_commit.call_args[0][0] == "fix(app): manually edited commit message"


def test_commit_too_short_abort(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("zana.commands.commit.git_diff_staged", lambda: SAMPLE_DIFF)
    monkeypatch.setattr(
        "zana.services.llm.CommitMessageGenerator.generate", lambda *a, **kw: "short"
    )
    result = runner.invoke(app, ["commit", "--yes"])
    assert result.exit_code == 1
    assert "too short" in result.stdout
