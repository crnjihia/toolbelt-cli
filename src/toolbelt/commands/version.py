"""Implementation of `toolbelt version` command."""

from __future__ import annotations

import importlib.metadata

import httpx
from rich.panel import Panel

from ..utils.console import get_console


def main() -> None:
    """Print the current version and check PyPI for newer releases."""
    console = get_console()
    try:
        current_version = importlib.metadata.version("toolbelt-cli")
    except Exception:
        current_version = "0.2.3"

    console.print(
        Panel(
            f"[bold]toolbelt-cli version:[/bold] {current_version}",
            style="green",
            border_style="green",
        )
    )

    pypi_url = "https://pypi.org/pypi/toolbelt-cli/json"
    try:
        resp = httpx.get(pypi_url, timeout=5.0)
        resp.raise_for_status()
        data = resp.json()
        latest = data.get("info", {}).get("version")
        if latest and latest != current_version:
            console.print(
                Panel(
                    f"[yellow]A newer version {latest} is available![/yellow]\n"
                    f"Run: [bold cyan]pip install -U toolbelt-cli[/bold cyan]",
                    style="yellow",
                    border_style="yellow",
                    title="Update Available",
                )
            )
    except Exception:
        # Ignore network errors or unavailable PyPI endpoint
        pass
