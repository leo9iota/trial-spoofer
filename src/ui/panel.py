"""
Panel module for displaying formatted messages to users.
Provides consistent styling for success, warning, error, and info messages.
"""

from rich.console import Console
from rich.panel import Panel as RichPanel
from rich.text import Text


class Panel:
    """Custom panel class for displaying formatted messages."""

    def __init__(self, console: Console = None):
        """Initialize the panel with an optional console."""
        self.console = console or Console()

    def success(self, message: str, title: str = "Success") -> None:
        """Display a success message in a green panel."""
        panel = RichPanel(
            Text(message, style="bold green"),
            title=f"[bold green]✓ {title}[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
        self.console.print(panel)

    def error(self, message: str, title: str = "Error") -> None:
        """Display an error message in a red panel."""
        panel = RichPanel(
            Text(message, style="bold red"),
            title=f"[bold red]✗ {title}[/bold red]",
            border_style="red",
            padding=(1, 2),
        )
        self.console.print(panel)

    def warning(self, message: str, title: str = "Warning") -> None:
        """Display a warning message in a yellow panel."""
        panel = RichPanel(
            Text(message, style="bold yellow"),
            title=f"[bold yellow]⚠ {title}[/bold yellow]",
            border_style="yellow",
            padding=(1, 2),
        )
        self.console.print(panel)

    def info(self, message: str, title: str = "Info") -> None:
        """Display an info message in a blue panel."""
        panel = RichPanel(
            Text(message, style="bold blue"),
            title=f"[bold blue]ℹ {title}[/bold blue]",
            border_style="blue",
            padding=(1, 2),
        )
        self.console.print(panel)

    def custom(
        self,
        message: str,
        title: str = "",
        style: str = "white",
        border_style: str = "white",
        title_style: str = "bold white",
    ) -> None:
        """Display a custom styled message panel."""
        panel = RichPanel(
            Text(message, style=style),
            title=f"[{title_style}]{title}[/{title_style}]" if title else "",
            border_style=border_style,
            padding=(1, 2),
        )
        self.console.print(panel)


# Convenience functions for quick access
def draw_success_panel(
    message: str, title: str = "Success", console: Console = None
) -> None:
    """Show a success message panel."""
    Panel(console).success(message, title)


def draw_error_panel(
    message: str, title: str = "Error", console: Console = None
) -> None:
    """Show an error message panel."""
    Panel(console).error(message, title)


def draw_warning_panel(
    message: str, title: str = "Warning", console: Console = None
) -> None:
    """Show a warning message panel."""
    Panel(console).warning(message, title)


def draw_info_panel(message: str, title: str = "Info", console: Console = None) -> None:
    """Show an info message panel."""
    Panel(console).info(message, title)
