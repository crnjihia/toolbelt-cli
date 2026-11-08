# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.4] - 2026-11-08

### Changed
- Restored linked README badge images with verified image endpoints.
- Added the documentation badge to the GitHub Pages site.

## [0.2.3] - 2026-11-08

### Changed
- Replaced external README badge images with reliable text links.

## [0.2.2] - 2026-11-08

### Changed
- Replaced the README badge markup with standard Markdown badges and removed the externally hosted Ruff badge endpoint.

## [0.2.1] - 2026-11-08

### Changed
- Updated the README with accurate installation, command usage, configuration, and deployment instructions.
- Synchronized the docs site and version-command fallback with the package version.
- Updated GitHub Actions to current Node.js 24-compatible major versions.
- Restricted CI workflow permissions to read-only repository contents.

## [0.2.0] - 2026-10-17

### Added
- Official GitHub Pages documentation portal (`docs/`):
  - Modern responsive layout with dark/light themes and design tokens.
  - Interactive browser-based Terminal Simulator with live command previews.
  - Instant keyboard-accessible documentation search (`Ctrl+K` / `Cmd+K`).
  - Interactive multi-tool installation switcher (`pipx`, `uv`, `pip`, source).
  - One-click copy-to-clipboard functionality across all command snippets.
  - Sticky table of contents and scrollspy navigation.
- GitHub Actions workflow (`.github/workflows/pages.yml`) for automated documentation deployment.
- Documentation URL in `pyproject.toml` pointing to `https://crnjihia.github.io/toolbelt-cli/`.
- Docs status badge in `README.md`.

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
