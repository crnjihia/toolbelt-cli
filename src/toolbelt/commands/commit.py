"""Implementation of `toolbelt commit` command."""

from __future__ import annotations

import typer
from rich.panel import Panel
from rich.prompt import Prompt

from ..services.llm import CommitMessageGenerator
from ..utils.console import get_console
from ..utils.git import git_commit, git_diff_staged


def main(
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Print proposed commit message without committing."
    ),
    commit_type: str | None = typer.Option(
        None, "--type", "-t", help="Force commit type (feat, fix, docs, etc.)."
    ),
    scope: str | None = typer.Option(None, "--scope", "-s", help="Force commit scope."),
    yes: bool = typer.Option(
        False, "--yes", "-y", help="Skip confirmation prompt and commit immediately."
    ),
) -> None:
    """Generate Conventional Commit message from staged diff using Claude."""
    console = get_console()

    try:
        diff = git_diff_staged()
    except Exception as exc:
        console.print(f"[bold red]Git error:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc

    if not diff or not diff.strip():
        console.print("[bold red]Nothing staged. Run git add first.[/bold red]")
        raise typer.Exit(code=1)

    generator = CommitMessageGenerator()
    message = generator.generate(diff, commit_type=commit_type, scope=scope)

    if len(message.strip()) < 10:
        console.print(
            "[bold red]Commit message too short (< 10 chars); aborting.[/bold red]"
        )
        raise typer.Exit(code=1)

    console.print(Panel(message, title="Proposed Commit Message", border_style="cyan"))

    if dry_run:
        console.print("[green]Dry run – commit not performed.[/green]")
        raise typer.Exit(code=0)

    if not yes:
        choice = (
            Prompt.ask(
                "Apply commit? [y/n/edit]",
                choices=["y", "n", "edit", "e"],
                default="y",
            )
            .strip()
            .lower()
        )

        if choice in {"n", "no"}:
            console.print("[yellow]Commit aborted by user.[/yellow]")
            raise typer.Exit(code=1)

        if choice in {"edit", "e"}:
            edited = Prompt.ask("Edit message", default=message).strip()
            if len(edited) < 10:
                console.print(
                    "[bold red]Commit message too short (< 10 chars).[/bold red]"
                )
                raise typer.Exit(code=1)
            message = edited

    try:
        git_commit(message)
    except Exception as exc:
        console.print(f"[bold red]Commit failed:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc

    console.print("[bold green]✅ Commit created successfully![/bold green]")
