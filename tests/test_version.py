"""Tests for the `toolbelt version` command."""

from __future__ import annotations

from unittest import mock

import httpx
from typer.testing import CliRunner

from toolbelt.cli import app

runner = CliRunner()


def test_version_no_update() -> None:
    with mock.patch("importlib.metadata.version", return_value="0.1.0"):
        mock_resp = mock.MagicMock()
        mock_resp.json.return_value = {"info": {"version": "0.1.0"}}
        mock_resp.raise_for_status.return_value = None

        with mock.patch("httpx.get", return_value=mock_resp):
            result = runner.invoke(app, ["version"])
            assert result.exit_code == 0, result.stdout
            assert "toolbelt-cli version: 0.1.0" in result.stdout
            assert "newer version" not in result.stdout.lower()


def test_version_newer_available() -> None:
    with mock.patch("importlib.metadata.version", return_value="0.1.0"):
        mock_resp = mock.MagicMock()
        mock_resp.json.return_value = {"info": {"version": "0.2.0"}}
        mock_resp.raise_for_status.return_value = None

        with mock.patch("httpx.get", return_value=mock_resp):
            result = runner.invoke(app, ["version"])
            assert result.exit_code == 0, result.stdout
            assert "A newer version 0.2.0 is available" in result.stdout


def test_version_offline_fallback() -> None:
    with mock.patch("importlib.metadata.version", return_value="0.1.0"):
        with mock.patch("httpx.get", side_effect=httpx.ConnectError("Offline")):
            result = runner.invoke(app, ["version"])
            assert result.exit_code == 0, result.stdout
            assert "toolbelt-cli version: 0.1.0" in result.stdout
