"""Entry point for the Zana CLI using Typer."""

from __future__ import annotations

import typer

from .commands import audit, commit, new, version

app = typer.Typer(
    name="zana",
    help=("Zana – developer productivity CLI: scaffolding, AI commits, and audits."),
    rich_markup_mode="rich",
    no_args_is_help=True,
)

# Explicitly register subcommands with designated names
app.command(
    name="new",
    help="Scaffold a new project (python, node, java) with opinionated defaults.",
)(new.main)

app.command(
    name="commit",
    help="Generate Conventional Commit messages from diff using Claude API.",
)(commit.main)

app.command(
    name="audit",
    help="Audit repo for README sections, .gitignore, licenses, and CI.",
)(audit.main)

app.command(
    name="version",
    help="Print installed version and check PyPI for updates.",
)(version.main)


def main() -> None:
    """Run the Zana CLI application."""
    app()


if __name__ == "__main__":
    main()
