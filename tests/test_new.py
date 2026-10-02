"""Tests for the `zana new` command."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from zana.cli import app

runner = CliRunner()


def test_new_python_scaffold(tmp_path: Path) -> None:
    proj_path = tmp_path / "myproj"
    result = runner.invoke(
        app,
        ["new", "python", str(proj_path)],
        input="Test Author\nMIT\ny\ny\n",
    )
    assert result.exit_code == 0, result.stdout
    assert (proj_path / "src" / "myproj" / "__init__.py").exists()
    assert (proj_path / "src" / "myproj" / "main.py").exists()
    assert (proj_path / "tests" / "test_main.py").exists()
    assert (proj_path / "pyproject.toml").exists()
    assert (proj_path / ".pre-commit-config.yaml").exists()
    assert (proj_path / "Makefile").exists()
    assert (proj_path / "README.md").exists()
    assert (proj_path / ".gitignore").exists()
    assert (proj_path / ".github" / "workflows" / "ci.yml").exists()
    assert (proj_path / "Dockerfile").exists()

    # Check pyproject.toml content has correct project name
    pyproject_text = (proj_path / "pyproject.toml").read_text(encoding="utf-8")
    assert 'name = "myproj"' in pyproject_text

    # Verify LICENSE contains MIT text
    license_text = (proj_path / "LICENSE").read_text(encoding="utf-8")
    assert "MIT License" in license_text
    assert "Test Author" in license_text


def test_new_node_scaffold(tmp_path: Path) -> None:
    proj_path = tmp_path / "nodeproj"
    result = runner.invoke(
        app,
        ["new", "node", str(proj_path)],
        input="Node Author\nApache-2.0\nn\nn\n",
    )
    assert result.exit_code == 0, result.stdout
    assert (proj_path / "package.json").exists()
    assert (proj_path / "tsconfig.json").exists()
    assert (proj_path / "src" / "index.ts").exists()
    assert (proj_path / "src" / "index.test.ts").exists()
    assert (proj_path / ".eslintrc.json").exists()
    assert (proj_path / ".prettierrc").exists()
    assert (proj_path / "README.md").exists()
    assert (proj_path / "LICENSE").exists()

    package_json = (proj_path / "package.json").read_text(encoding="utf-8")
    assert '"name": "nodeproj"' in package_json

    license_text = (proj_path / "LICENSE").read_text(encoding="utf-8")
    assert "Apache License" in license_text


def test_new_java_scaffold(tmp_path: Path) -> None:
    proj_path = tmp_path / "javaproj"
    result = runner.invoke(
        app,
        ["new", "java", str(proj_path)],
        input="Java Author\nnone\nn\nn\n",
    )
    assert result.exit_code == 0, result.stdout
    assert (proj_path / "pom.xml").exists()
    assert (
        proj_path / "src" / "main" / "java" / "com" / "javaproj" / "App.java"
    ).exists()
    assert (
        proj_path / "src" / "test" / "java" / "com" / "javaproj" / "AppTest.java"
    ).exists()
    assert not (proj_path / "LICENSE").exists()


def test_new_invalid_type(tmp_path: Path) -> None:
    proj_path = tmp_path / "invalidproj"
    result = runner.invoke(app, ["new", "golang", str(proj_path)])
    assert result.exit_code == 1
    assert "Unsupported project type" in result.stdout
