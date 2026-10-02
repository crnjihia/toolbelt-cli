"""Implementation of `zana new <type> <name>` command."""

from __future__ import annotations

from pathlib import Path

import typer
from rich import box
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from ..services.scaffolder import Scaffolder
from ..utils.console import get_console
from ..utils.git import get_git_user_name


def main(
    project_type: str = typer.Argument(..., help="Project type: python, node, java"),
    name: str = typer.Argument(..., help="Project directory / package name"),
    author: str | None = typer.Option(None, "--author", "-a", help="Author name"),
    license_choice: str | None = typer.Option(
        None, "--license", "-l", help="License: MIT, Apache-2.0, none"
    ),
    ci: bool | None = typer.Option(
        None, "--ci/--no-ci", help="Include CI configuration"
    ),
    docker: bool | None = typer.Option(
        None, "--docker/--no-docker", help="Include Dockerfile"
    ),
    yes: bool = typer.Option(
        False, "--yes", "-y", help="Accept all defaults without prompting"
    ),
) -> None:
    """Scaffold a new Python, Node, or Java project with opinionated structure."""
    console = get_console()
    normalized_type = project_type.strip().lower()

    if normalized_type not in {"python", "node", "java"}:
        console.print(
            f"[bold red]Error:[/bold red] Unsupported project type '{project_type}'. "
            "Choose from: python, node, java."
        )
        raise typer.Exit(code=1)

    target_dir = Path(name).resolve()
    if target_dir.exists() and any(target_dir.iterdir()):
        console.print(
            f"[bold red]Error:[/bold red] Target directory '{name}' "
            "already exists and is not empty."
        )
        raise typer.Exit(code=1)

    # Interactive prompts (or flag values / defaults)
    default_author = get_git_user_name() or "Developer"
    if author is None:
        if yes:
            author = default_author
        else:
            author = Prompt.ask("Author name", default=default_author)

    if license_choice is None:
        if yes:
            license_choice = "MIT"
        else:
            license_choice = Prompt.ask(
                "License",
                choices=["MIT", "Apache-2.0", "none"],
                default="MIT",
            )
    elif license_choice not in {"MIT", "Apache-2.0", "none"}:
        console.print(
            f"[bold red]Error:[/bold red] Invalid license '{license_choice}'. "
            "Choose MIT, Apache-2.0, or none."
        )
        raise typer.Exit(code=1)

    if ci is None:
        if yes:
            ci = True
        else:
            ci = Confirm.ask("Include CI? (y/n)", default=True)

    if docker is None:
        if yes:
            docker = False
        else:
            docker = Confirm.ask("Include Docker? (y/n)", default=False)

    scaffolder = Scaffolder(
        project_type=normalized_type,
        project_name=target_dir.name,
        author=author,
        license=license_choice,
        include_ci=ci,
        include_docker=docker,
        destination=target_dir,
    )
    scaffolder.run()

    if normalized_type == "python":
        commands = f"cd {target_dir.name} && make install && make test"
    elif normalized_type == "node":
        commands = f"cd {target_dir.name} && npm install && npm test"
    else:
        commands = f"cd {target_dir.name} && mvn clean test"

    console.print(
        Panel(
            f"[bold green]✨ Project successfully scaffolded![/bold green]\n\n"
            f"[dim]Next steps:[/dim]\n"
            f"[bold cyan]{commands}[/bold cyan]",
            title="🎉 Zana Scaffold",
            border_style="green",
            box=box.ROUNDED,
        )
    )
