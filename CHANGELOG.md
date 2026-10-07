# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-10-02

### Added
- Core Typer CLI framework with `toolbelt` entry point and Rich formatting.
- `toolbelt new <type> <name>` command supporting opinionated scaffolds for `python`, `node`, and `java`.
- Complete Jinja2 templates for Python, Node.js/TypeScript, and Java projects.
- `toolbelt commit` command integrating Anthropic Claude (`claude-sonnet-4`) with interactive `Y/n/edit` prompt and rule-based fallback generator.
- `toolbelt audit [path]` command with 10 repository quality checks, Rich table output, `--json` export, and `--fix` automated repair.
- `toolbelt version` command providing installed version detection and automated PyPI update checks.
- Comprehensive test suite covering all CLI commands using `pytest` and `typer.testing.CliRunner`.
- GitHub Actions CI workflow with multi-version Python matrix, Ruff linting, formatting, MyPy, and Pytest.
- GitHub Actions Release workflow using PyPI Trusted Publishing via OIDC.
- Full `pyproject.toml` packaging configuration with metadata, dependencies, classifiers, and tool specifications.
- Complete documentation including README with command reference, badges, examples, and contributing guidelines.
