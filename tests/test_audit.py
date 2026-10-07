"""Tests for the `toolbelt audit` command."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from toolbelt.cli import app

runner = CliRunner()


def create_sample_repo(
    base: Path,
    include_readme: bool = True,
    include_install: bool = True,
    include_usage: bool = True,
    include_license_section: bool = True,
    include_license_file: bool = True,
    include_gitignore: bool = True,
    include_pycache: bool = True,
    include_tests: bool = True,
    include_ci: bool = True,
    include_pyproject: bool = True,
) -> None:
    """Create a sample repository tree with configurable components."""
    if include_readme:
        sections = ["# Sample Project\n"]
        if include_install:
            sections.append("## Installation\n\npip install .\n")
        if include_usage:
            sections.append("## Usage\n\ntoolbelt --help\n")
        if include_license_section:
            sections.append("## License\n\nMIT License\n")
        (base / "README.md").write_text("\n".join(sections), encoding="utf-8")

    if include_license_file:
        (base / "LICENSE").write_text(
            "MIT License\n\nCopyright (c) 2026\n", encoding="utf-8"
        )

    if include_gitignore:
        gi_lines = ["build/", "dist/"]
        if include_pycache:
            gi_lines.append("__pycache__/")
        (base / ".gitignore").write_text("\n".join(gi_lines) + "\n", encoding="utf-8")

    if include_tests:
        tests_dir = base / "tests"
        tests_dir.mkdir(parents=True, exist_ok=True)
        (tests_dir / "test_example.py").write_text(
            "def test_ok(): pass\n", encoding="utf-8"
        )

    if include_ci:
        wf_dir = base / ".github" / "workflows"
        wf_dir.mkdir(parents=True, exist_ok=True)
        (wf_dir / "ci.yml").write_text("name: CI\non: push\n", encoding="utf-8")

    if include_pyproject:
        (base / "pyproject.toml").write_text(
            '[project]\nname = "sample"\n', encoding="utf-8"
        )


def test_audit_all_pass(tmp_path: Path) -> None:
    create_sample_repo(tmp_path)
    result = runner.invoke(app, ["audit", str(tmp_path)])
    assert result.exit_code == 0, result.stdout
    assert "✅" in result.stdout
    assert "README.md exists" in result.stdout
    assert "README has Install" in result.stdout
    assert "README has Usage" in result.stdout
    assert "README has License" in result.stdout
    assert "LICENSE file" in result.stdout
    assert ".gitignore exists" in result.stdout
    assert ".gitignore has __pycache__" in result.stdout
    assert "Tests directory" in result.stdout
    assert "CI config" in result.stdout
    assert "pyproject.toml" in result.stdout


def test_audit_failures(tmp_path: Path) -> None:
    # Repo missing Usage section and LICENSE file
    create_sample_repo(tmp_path, include_usage=False, include_license_file=False)
    result = runner.invoke(app, ["audit", str(tmp_path)])
    assert result.exit_code == 1
    assert "❌" in result.stdout
    assert 'missing "## Usage" section' in result.stdout


def test_audit_json_output(tmp_path: Path) -> None:
    create_sample_repo(tmp_path)
    result = runner.invoke(app, ["audit", str(tmp_path), "--json"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert len(data) >= 10
    names = {item["name"] for item in data}
    assert "README.md exists" in names
    assert "README has Install" in names
    assert all(item["passed"] is True for item in data)


def test_audit_fix_flag(tmp_path: Path) -> None:
    # Repo missing gitignore and license
    create_sample_repo(tmp_path, include_gitignore=False, include_license_file=False)
    assert not (tmp_path / ".gitignore").exists()
    assert not (tmp_path / "LICENSE").exists()

    result = runner.invoke(app, ["audit", str(tmp_path), "--fix"], input="y\ny\nMIT\n")
    assert result.exit_code == 0
    assert (tmp_path / ".gitignore").exists()
    assert (tmp_path / "LICENSE").exists()
    assert "__pycache__" in (tmp_path / ".gitignore").read_text(encoding="utf-8")
    assert "MIT License" in (tmp_path / "LICENSE").read_text(encoding="utf-8")
