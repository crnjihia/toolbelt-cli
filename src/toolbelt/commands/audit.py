"""Implementation of `toolbelt audit [path]` command."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich import box
from rich.table import Table

from ..services.auditor import Auditor
from ..utils.console import get_console


def main(
    path: str = typer.Argument(".", help="Path to repository to audit."),
    json_output: bool = typer.Option(
        False, "--json", help="Output machine-readable JSON."
    ),
    fix: bool = typer.Option(
        False, "--fix", help="Auto-create missing .gitignore and LICENSE."
    ),
) -> None:
    """Audit repo for README sections, .gitignore, licenses, and CI."""
    console = get_console()
    repo_path = Path(path).resolve()

    if not repo_path.exists() or not repo_path.is_dir():
        console.print(f"[bold red]Error:[/bold red] Invalid directory: {path}")
        raise typer.Exit(code=1)

    auditor = Auditor(repo_path, console=console)
    results = auditor.run(fix=fix)

    if json_output:
        data = [r.to_dict() for r in results]
        console.print(json.dumps(data, indent=2))
    else:
        table = Table(
            title=f"Repository Audit: {repo_path.name}",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan",
        )
        table.add_column("Check", style="bold white", min_width=25)
        table.add_column("Status", justify="center", width=8)
        table.add_column("Details", style="dim white")

        for res in results:
            status_symbol = (
                "[bold green]✅[/bold green]"
                if res.passed
                else "[bold red]❌[/bold red]"
            )
            table.add_row(res.name, status_symbol, res.details)

        console.print(table)

    all_passed = all(r.passed for r in results)
    if not all_passed:
        raise typer.Exit(code=1)
    raise typer.Exit(code=0)
