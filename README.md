# Zana CLI

<p align="center">
  <img src="assets/demo.png" alt="Zana CLI in action" width="800" />
</p>

<p align="center">
  <strong>Opinionated Developer Productivity CLI: Multi-Language Scaffolding, AI Git Commits, and Repository Auditing.</strong>
</p>

<p align="center">
  <a href="https://github.com/crnji/Zana-CLI/actions/workflows/ci.yml"><img src="https://github.com/crnji/Zana-CLI/actions/workflows/ci.yml/badge.svg" alt="CI Status" /></a>
  <a href="https://pypi.org/project/zana-cli/"><img src="https://img.shields.io/pypi/v/zana-cli.svg?color=blue" alt="PyPI Version" /></a>
  <a href="https://pypi.org/project/zana-cli/"><img src="https://img.shields.io/pypi/pyversions/zana-cli.svg" alt="Python Versions" /></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" /></a>
  <a href="https://mypy.readthedocs.io/"><img src="https://img.shields.io/badge/types-Mypy-blue.svg" alt="Type Checked" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" /></a>
</p>

---

## Overview

**Zana CLI** (`zana`) is a command-line tool built with Python 3.11+, Typer, Rich, and Jinja2 that automates repetitive developer workflows:

1. 🚀 **Scaffold New Projects (`zana new`)**: Instantly generate clean, production-ready project templates for **Python**, **Node.js / TypeScript**, and **Java** with pre-configured linters, test harnesses, CI pipelines, and Dockerfiles.
2. 🤖 **AI-Powered Commits (`zana commit`)**: Automatically analyze staged git diffs and draft structured Conventional Commit messages using **Claude** (`claude-sonnet-4`), with an offline rule-based fallback when no API key is set.
3. 🔍 **Repository Auditing (`zana audit`)**: Scan any codebase for missing documentation sections (`Installation`, `Usage`, `License`), required configuration files (`.gitignore`, `pyproject.toml`, test suites, CI workflows), and automatically repair missing files with `--fix`.
4. 📦 **Version & PyPI Sync (`zana version`)**: Inspect currently installed version and verify release availability against the Python Package Index.

---

## Installation

### With `pipx` (Recommended)
Isolate CLI tools in their own dedicated virtual environments:
```bash
pipx install zana-cli
```

### With `uv`
Fast single-step tool installation:
```bash
uv tool install zana-cli
```

### With standard `pip`
```bash
pip install zana-cli
```

### Local Development Installation
```bash
git clone https://github.com/crnji/Zana-CLI.git
cd Zana-CLI
pip install -e ".[dev]"
```

---

## Command Reference

| Command | Arguments | Flags | Description |
|:---|:---|:---|:---|
| `zana new` | `<type>` `<name>` | `--author`, `--license`, `--ci/--no-ci`, `--docker/--no-docker`, `-y/--yes` | Scaffold an opinionated Python, Node, or Java project. |
| `zana commit` | *(none)* | `--dry-run`, `-t/--type`, `-s/--scope`, `-y/--yes` | Inspect staged diff and generate Conventional Commit message. |
| `zana audit` | `[path=.]` | `--json`, `--fix` | Run 10-point repository audit with Rich table or JSON output. |
| `zana version` | *(none)* | *(none)* | Display installed version and check PyPI for updates. |
| `zana --help` | *(none)* | *(none)* | Show global options and available commands. |

---

## Feature Tour

### 1. `zana new <type> <name>`
Scaffolds a new project directory with interactive prompts powered by Typer and Rich:

```bash
zana new python my_service
```

```text
Author name [Jane Doe]: Jane Doe
License (MIT | Apache-2.0 | none) [MIT]: MIT
Include CI? (y/n) [True]: y
Include Docker? (y/n) [False]: y

┌───────────────────────────── 🎉 Zana Scaffold ──────────────────────────────┐
│ ✨ Project successfully scaffolded!                                         │
│                                                                             │
│ Next steps:                                                                 │
│ cd my_service && make install && make test                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Supported Stacks & Project Layouts

- **Python (`zana new python <name>`)**:
  - `src/<name>/__init__.py`, `main.py`
  - `tests/test_main.py`
  - `pyproject.toml` (configured with Ruff, MyPy, and Pytest)
  - `.pre-commit-config.yaml`
  - `Makefile` (`install`, `test`, `lint`, `format`, `clean`)
  - `README.md`, `.gitignore`, `LICENSE`
  - `.github/workflows/ci.yml` (optional)
  - `Dockerfile` (optional)

- **Node.js / TypeScript (`zana new node <name>`)**:
  - `package.json` (TypeScript, ESLint, Prettier, Vitest)
  - `tsconfig.json`
  - `src/index.ts`, `src/index.test.ts`
  - `.eslintrc.json`, `.prettierrc`
  - `README.md`, `.gitignore`, `LICENSE`

- **Java (`zana new java <name>`)**:
  - `pom.xml` (Maven, JUnit 5 Jupiter, compiler plugins)
  - `src/main/java/com/<name>/App.java`
  - `src/test/java/com/<name>/AppTest.java`
  - `README.md`, `.gitignore`, `LICENSE`

---

### 2. `zana commit`
Reads your staged git diff (`git diff --staged`) and drafts a Conventional Commit message:

```bash
git add src/
zana commit
```

```text
┌────────────────────────── Proposed Commit Message ──────────────────────────┐
│ feat(auth): add bearer token validator and refresh middleware              │
└─────────────────────────────────────────────────────────────────────────────┘
Apply commit? [y/n/edit] (y): y
✅ Commit created successfully!
```

- **Claude Sonnet 4 Integration**: Export your Anthropic API key (`export ANTHROPIC_API_KEY="sk-ant-..."`) for contextual messages following standard types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
- **Smart Fallback**: If no key is set, Zana falls back to an offline heuristic analyzer that inspects diff sizes, lines added/removed, and modified file types.
- **Dry-run Mode**: Preview generated messages without applying commits using `zana commit --dry-run`.
- **Safety**: Rejects any commit message shorter than 10 characters and offers interactive `[y/n/edit]` revision.

---

### 3. `zana audit [path]`
Performs a structured quality check on any repository:

```bash
zana audit .
```

```text
                     Repository Audit: Zana-CLI                     
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

### 4. `zana version`
Displays installed package version and checks whether updates are available on PyPI:

```bash
zana version
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
zana-cli/
├── src/zana/
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

## Publishing to PyPI

This project is configured with GitHub Actions **Trusted Publishing** using OpenID Connect (OIDC). No long-lived API tokens are stored in repository secrets.

To release a new version:
1. Bump the version in `pyproject.toml` and `src/zana/__init__.py`.
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
