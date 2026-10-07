"""Rich console helpers for Toolbelt CLI."""

from __future__ import annotations

import sys

from rich.console import Console
from rich.panel import Panel

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

_console = Console()


def get_console() -> Console:
    """Return a shared singleton Rich console."""
    return _console


def success_panel(message: str, title: str = "Success") -> Panel:
    """Create a green success panel."""
    return Panel(message, title=f"✅ {title}", border_style="green")


def error_panel(message: str, title: str = "Error") -> Panel:
    """Create a red error panel."""
    return Panel(message, title=f"❌ {title}", border_style="red")


def info_panel(message: str, title: str = "Info") -> Panel:
    """Create a cyan info panel."""
    return Panel(message, title=f"ℹ️ {title}", border_style="cyan")
