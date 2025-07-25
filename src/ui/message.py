#!/usr/bin/env python3


"""
Message Class (message.py)

Display error, warning, and success messages to the user.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class Message:
    """Message panel for displaying information to the user."""

    def __init__(self, console: Console | None = None) -> None:
        """
        Initialize the Message class.

        Args:
            console: Optional Rich Console instance. If None, creates a new one.
        """
        self.console = console or Console()

    def error(self, message: str, title: str = "Error") -> None:
        """
        Display an error message in a red box.

        Args:
            message: The error message to display
            title: The title for the error box (default: "Error")
        """
        panel = Panel(
            Text(message, style="white"),
            title=f"[bold red]{title}[/bold red]",
            border_style="red",
            padding=(1, 2),
        )
        self.console.print(panel)

    def warning(self, message: str, title: str = "Warning") -> None:
        """
        Display a warning message in a yellow box.

        Args:
            message: The warning message to display
            title: The title for the warning box (default: "Warning")
        """
        panel = Panel(
            Text(message, style="black"),
            title=f"[bold yellow]{title}[/bold yellow]",
            border_style="yellow",
            padding=(1, 2),
        )
        self.console.print(panel)

    def success(self, message: str, title: str = "Success") -> None:
        """
        Display a success message in a green box.

        Args:
            message: The success message to display
            title: The title for the success box (default: "Success")
        """
        panel = Panel(
            Text(message, style="white"),
            title=f"[bold green]{title}[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
        self.console.print(panel)

    def info(self, message: str, title: str = "Info") -> None:
        """
        Display an info message in a blue box.

        Args:
            message: The info message to display
            title: The title for the info box (default: "Info")
        """
        panel = Panel(
            Text(message, style="white"),
            title=f"[bold blue]{title}[/bold blue]",
            border_style="blue",
            padding=(1, 2),
        )
        self.console.print(panel)

    def custom(
        self,
        message: str,
        title: str = "Message",
        border_color: str = "white",
        title_color: str = "white",
        text_color: str = "white",
    ) -> None:
        """
        Display a custom styled message box.

        Args:
            message: The message to display
            title: The title for the box
            border_color: Color for the border
            title_color: Color for the title
            text_color: Color for the message text
        """
        panel = Panel(
            Text(message, style=text_color),
            title=f"[bold {title_color}]{title}[/bold {title_color}]",
            border_style=border_color,
            padding=(1, 2),
        )
        self.console.print(panel)

    def display(self, message: str, box_type: str = "info") -> None:
        """
        Display a message using the specified box type.

        Args:
            message: The message to display
            box_type: Type of box ('error', 'warning', 'success', 'info')
        """
        box_type = box_type.lower()
        if box_type == "error":
            self.error(message)
        elif box_type == "warning":
            self.warning(message)
        elif box_type == "success":
            self.success(message)
        elif box_type == "info":
            self.info(message)
        else:
            self.info(message)  # Default to info if unknown type

    def __str__(self) -> str:
        """Return string representation of the Box class."""
        return "Box(console=<Rich Console>)"

    def __repr__(self) -> str:
        """Return detailed string representation of the Box class."""
        return f"Box(console={self.console!r})"
