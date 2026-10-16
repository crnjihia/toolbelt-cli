# Toolbelt CLI

<p align="center">
  <img src="assets/demo.png" alt="Toolbelt CLI in action" width="800" />
</p>

*The screenshot above demonstrates live execution of Toolbelt CLI in Windows Terminal:*
1. **`toolbelt --help`**: Rich command overview, argument formatting, and shell completion options.
2. **`toolbelt version`**: Fast local package version readout and automated PyPI release checking.
3. **`toolbelt audit .`**: 10-point repository quality audit checking README sections, license files, `.gitignore` entries, test directories, and CI workflows.

<p align="center">
  <strong>Opinionated Developer Productivity CLI: Multi-Language Scaffolding, AI Git Commits, and Repository Auditing.</strong>
</p>

<p align="center">
  <a href="https://crnjihia.github.io/toolbelt-cli/"><img src="https://img.shields.io/badge/Docs-GitHub%20Pages-10b981?style=flat&logo=github" alt="Documentation" /></a>
  <a href="https://github.com/crnjihia/toolbelt-cli/actions/workflows/ci.yml"><img src="https://github.com/crnjihia/toolbelt-cli/actions/workflows/ci.yml/badge.svg" alt="CI Status" /></a>
  <a href="https://pypi.org/project/toolbelt-cli/"><img src="https://img.shields.io/pypi/v/toolbelt-cli.svg?color=blue" alt="PyPI Version" /></a>
  <a href="https://pypi.org/project/toolbelt-cli/"><img src="https://img.shields.io/pypi/pyversions/toolbelt-cli.svg" alt="Python Versions" /></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" /></a>
  <a href="https://mypy.readthedocs.io/"><img src="https://img.shields.io/badge/types-Mypy-blue.svg" alt="Type Checked" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" /></a>
</p>

---

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Command Reference](#command-reference)
- [Feature Tour & Usage Examples](#feature-tour)
  - [1. Project Scaffolding (`toolbelt new`)](#1-toolbelt-new-type-name)
  - [2. AI-Powered Commits (`toolbelt commit`)](#2-toolbelt-commit)
  - [3. Repository Auditing (`toolbelt audit`)](#3-toolbelt-audit-path)
  - [4. Version & Upstream Sync (`toolbelt version`)](#4-toolbelt-version)
- [Configuration & Environment Variables](#configuration--environment-variables)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Development & Testing](#development--testing)
- [GitHub Setup & Publication Guide](#github-setup--publication-guide)
- [Publishing to PyPI](#publishing-to-pypi)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**Toolbelt CLI** (`toolbelt`) is a command-line tool built with Python 3.11+, Typer, Rich, and Jinja2 that automates repetitive developer workflows:

1. 🚀 **Scaffold New Projects (`toolbelt new`)**: Instantly generate clean, production-ready project templates for **Python**, **Node.js / TypeScript**, and **Java** with pre-configured linters, test harnesses, CI pipelines, and Dockerfiles.
2. 🤖 **AI-Powered Commits (`toolbelt commit`)**: Automatically analyze staged git diffs and draft structured Conventional Commit messages using **Claude** (`claude-sonnet-4`), with an offline rule-based fallback when no API key is set.
3. 🔍 **Repository Auditing (`toolbelt audit`)**: Scan any codebase for missing documentation sections (`Installation`, `Usage`, `License`), required configuration files (`.gitignore`, `pyproject.toml`, test suites, CI workflows), and automatically repair missing files with `--fix`.
4. 📦 **Version & PyPI Sync (`toolbelt version`)**: Inspect currently installed version and verify release availability against the Python Package Index.

---

## Installation

### With `pipx` (Recommended)
Isolate CLI tools in their own dedicated virtual environments:
```bash
pipx install toolbelt-cli
```

### With `uv`
Fast single-step tool installation:
```bash
uv tool install toolbelt-cli
```

### With standard `pip`
```bash
pip install toolbelt-cli
```

### Local Development Installation
```bash
git clone https://github.com/crnjihia/toolbelt-cli.git
cd toolbelt-cli
pip install -e ".[dev]"
```

---

## Command Reference

| Command | Arguments | Flags | Description |
|:---|:---|:---|:---|
| `toolbelt new` | `<type>` `<name>` | `--author`, `--license`, `--ci/--no-ci`, `--docker/--no-docker`, `-y/--yes` | Scaffold an opinionated Python, Node, or Java project. |
| `toolbelt commit` | *(none)* | `--dry-run`, `-t/--type`, `-s/--scope`, `-y/--yes` | Inspect staged diff and generate Conventional Commit message. |
| `toolbelt audit` | `[path=.]` | `--json`, `--fix` | Run 10-point repository audit with Rich table or JSON output. |
| `toolbelt version` | *(none)* | *(none)* | Display installed version and check PyPI for updates. |
| `toolbelt --help` | *(none)* | *(none)* | Show global options and available commands. |

---

## Feature Tour

### 1. `toolbelt new <type> <name>`
Scaffolds a new project directory with interactive prompts powered by Typer and Rich:

```bash
toolbelt new python my_service
```

```text
Author name [Jane Doe]: Jane Doe
License (MIT | Apache-2.0 | none) [MIT]: MIT
Include CI? (y/n) [True]: y
Include Docker? (y/n) [False]: y

┌──────────────────────────── 🎉 Toolbelt Scaffold ────────────────────────────┐
│ ✨ Project successfully scaffolded!                                         │
│                                                                             │
│ Next steps:                                                                 │
│ cd my_service && make install && make test                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Supported Stacks & Project Layouts

- **Python (`toolbelt new python <name>`)**:
  - `src/<name>/__init__.py`, `main.py`
  - `tests/test_main.py`
  - `pyproject.toml` (configured with Ruff, MyPy, and Pytest)
  - `.pre-commit-config.yaml`
  - `Makefile` (`install`, `test`, `lint`, `format`, `clean`)
  - `README.md`, `.gitignore`, `LICENSE`
  - `.github/workflows/ci.yml` (optional)
  - `Dockerfile` (optional)

- **Node.js / TypeScript (`toolbelt new node <name>`)**:
  - `package.json` (TypeScript, ESLint, Prettier, Vitest)
  - `tsconfig.json`
  - `src/index.ts`, `src/index.test.ts`
  - `.eslintrc.json`, `.prettierrc`
  - `README.md`, `.gitignore`, `LICENSE`

- **Java (`toolbelt new java <name>`)**:
  - `pom.xml` (Maven, JUnit 5 Jupiter, compiler plugins)
  - `src/main/java/com/<name>/App.java`
  - `src/test/java/com/<name>/AppTest.java`
  - `README.md`, `.gitignore`, `LICENSE`

---

### 2. `toolbelt commit`
Reads your staged git diff (`git diff --staged`) and drafts a Conventional Commit message:

```bash
git add src/
toolbelt commit
```

```text
┌────────────────────────── Proposed Commit Message ──────────────────────────┐
│ feat(auth): add bearer token validator and refresh middleware              │
└─────────────────────────────────────────────────────────────────────────────┘
Apply commit? [y/n/edit] (y): y
✅ Commit created successfully!
```

- **Claude Sonnet 4 Integration**: Export your Anthropic API key (`export ANTHROPIC_API_KEY="sk-ant-..."`) for contextual messages following standard types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
- **Smart Fallback**: If no key is set, Toolbelt falls back to an offline heuristic analyzer that inspects diff sizes, lines added/removed, and modified file types.
- **Dry-run Mode**: Preview generated messages without applying commits using `toolbelt commit --dry-run`.
- **Safety**: Rejects any commit message shorter than 10 characters and offers interactive `[y/n/edit]` revision.

---

### 3. `toolbelt audit [path]`
Performs a structured quality check on any repository:

```bash
toolbelt audit .
```

```text
                    Repository Audit: Toolbelt-CLI                     
┌────────────────────────────┬──────────┬──────────────────────────┐
│ Check                      │  Status  │ Details                  │
├────────────────────────────┼──────────┼──────────────────────────┤
│ README.md exists           │    ✅    │ 227 lines                │
│ README has Install         │    ✅    │ found "## Installation"  │
│ README has Usage           │    ✅    │ found "## Usage"         │
│ README has License         │    ✅    │ found "## License"       │
│ LICENSE file               │    ✅    │ MIT                      │
│ .gitignore exists          │    ✅    │ 29 entries               │
│ .gitignore has __pycache__ │    ✅    │                          │
│ Tests directory            │    ✅    │ tests/ found             │
│ CI config                  │    ✅    │ .github/workflows/ci.yml │
│ pyproject.toml             │    ✅    │                          │
└────────────────────────────┴──────────┴──────────────────────────┘
```

- **Exit Code**: Returns `0` if all checks pass, and `1` if any check fails (ready for pre-commit hooks and CI gates).
- **Auto-Fix (`--fix`)**: Automatically prompts to create missing `.gitignore` files and `LICENSE` files (MIT or Apache-2.0).
- **JSON Mode (`--json`)**: Outputs machine-readable JSON for integration into reporting tools or CI/CD pipelines.

---

### 4. `toolbelt version`
Displays installed package version and checks whether updates are available on PyPI:

```bash
toolbelt version
```

---

## Configuration & Environment Variables

Copy `.env.example` to `.env` to configure your environment:

```ini
# Optional: Set Claude API key for AI-assisted git commit message generation
ANTHROPIC_API_KEY=sk-ant-api03-...

# Optional: Set debug logging
LOG_LEVEL=INFO
```

---

## Architecture & Tech Stack

```text
toolbelt-cli/
├── src/toolbelt/
│   ├── cli.py             # Typer application definition and routing
│   ├── commands/          # Subcommand handlers (new, commit, audit, version)
│   ├── services/          # Scaffolder, LLM Commit Generator, and Auditor
│   ├── templates/         # Jinja2 project templates (python, node, java)
│   └── utils/             # Git interface, Rich console helpers
├── tests/                 # Full offline pytest test suite with CliRunner
└── .github/workflows/     # CI matrix & PyPI Trusted Publishing release
```

- **CLI Framework**: [Typer](https://typer.tiangolo.com/)
- **Terminal UI**: [Rich](https://rich.readthedocs.io/)
- **Templating**: [Jinja2](https://jinja.palletsprojects.com/)
- **HTTP Client**: [HTTPX](https://www.python-httpx.org/)
- **LLM Integration**: [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- **Quality**: [Ruff](https://astral.sh/ruff) & [MyPy](https://mypy.readthedocs.io/)
- **Testing**: [Pytest](https://docs.pytest.org/) & `CliRunner`

---

## Development & Testing

Run the automated test suite locally:

```bash
# Run unit and integration tests (100% offline)
pytest -v

# Check linting and style
ruff check .
ruff format --check .

# Run static type analysis
mypy src
```

---

## GitHub Setup & Publication Guide

Follow these steps to publish this repository to your personal or organization GitHub account:

### 1. Initialize & Link GitHub Remote
Create a new repository named `toolbelt-cli` on [GitHub](https://github.com/new) (leave "Initialize with README" unchecked). Then connect your local repository:

```bash
# Add your GitHub remote
git remote add origin https://github.com/crnjihia/toolbelt-cli.git

# Ensure default branch is main
git branch -M main

# Push code, tags, and complete history to GitHub
git push -u origin main
```

### 2. Configure PyPI Trusted Publishing (OIDC)
Toolbelt CLI uses GitHub Actions **Trusted Publishing** (OIDC) so no API tokens or passwords need to be saved in repository secrets:

1. Log into your [PyPI](https://pypi.org/) account.
2. Navigate to **Account settings** → **Publishing** → **Add a GitHub publisher**.
3. Set:
   - **PyPI Project Name**: `toolbelt-cli`
   - **Owner**: `crnjihia`
   - **Repository name**: `toolbelt-cli`
   - **Workflow name**: `release.yml`
   - **Environment name**: `pypi`
4. In your GitHub repository, ensure the `pypi` environment is enabled under **Settings** → **Environments**.
5. When ready to release, simply tag and push:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
   GitHub Actions will automatically build source distributions and wheels, run `twine check`, and publish to PyPI!

### 3. Continuous Integration Checks
On every push and pull request, [`.github/workflows/ci.yml`](.github/workflows/ci.yml) automatically executes:
- Matrix testing across Python **3.11** and **3.12**.
- Fast code hygiene validation via `ruff check .`.
- Code format verification via `ruff format --check .`.
- Static type analysis via `mypy src`.
- Complete test suite execution via `pytest -v` (19 offline tests with 100% pass guarantee).

---

## Publishing to PyPI

This project is configured with GitHub Actions **Trusted Publishing** using OpenID Connect (OIDC). No long-lived API tokens are stored in repository secrets.

To release a new version:
1. Bump the version in `pyproject.toml` and `src/toolbelt/__init__.py`.
2. Update `CHANGELOG.md`.
3. Create and push a git tag:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
4. The `.github/workflows/release.yml` workflow will automatically build wheels and sdist distributions and publish them directly to PyPI.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository on GitHub.
2. Create a feature branch: `git checkout -b feat/my-new-feature`
3. Ensure all tests and linters pass: `pytest && ruff check . && mypy src`
4. Commit your changes using conventional commits: `git commit -m "feat(scope): describe change"`
5. Open a Pull Request.

---

## License

Distributed under the [MIT License](LICENSE).
