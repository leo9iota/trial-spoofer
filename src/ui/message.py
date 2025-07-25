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
        Display an error message in a red message.

        Args:
            message: The error message to display
            title: The title for the error message (default: "Error")
        """
        panel: Panel = Panel(
            renderable=Text(text=message, style="white"),
            title=f"[bold red]{title}[/bold red]",
            border_style="red",
            padding=(1, 2),
        )
        self.console.print(panel)

    def warning(self, message: str, title: str = "Warning") -> None:
        """
        Display a warning message in a yellow message.

        Args:
            message: The warning message to display
            title: The title for the warning message (default: "Warning")
        """
        panel: Panel = Panel(
            renderable=Text(text=message, style="black"),
            title=f"[bold yellow]{title}[/bold yellow]",
            border_style="yellow",
            padding=(1, 2),
        )
        self.console.print(panel)

    def success(self, message: str, title: str = "Success") -> None:
        """
        Display a success message in a green message.

        Args:
            message: The success message to display
            title: The title for the success message (default: "Success")
        """
        panel: Panel = Panel(
            renderable=Text(text=message, style="white"),
            title=f"[bold green]{title}[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
        self.console.print(panel)

    def info(self, message: str, title: str = "Info") -> None:
        """
        Display an info message in a blue message.

        Args:
            message: The info message to display
            title: The title for the info message (default: "Info")
        """
        panel: Panel = Panel(
            renderable=Text(text=message, style="white"),
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
        Display a custom styled message message.

        Args:
            message: The message to display
            title: The title for the message
            border_color: Color for the border
            title_color: Color for the title
            text_color: Color for the message text
        """
        panel: Panel = Panel(
            renderable=Text(text=message, style=text_color),
            title=f"[bold {title_color}]{title}[/bold {title_color}]",
            border_style=border_color,
            padding=(1, 2),
        )
        self.console.print(panel)

    def display(self, message: str, message_type: str = "info") -> None:
        """
        Display a message using the specified message type.

        Args:
            message: The message to display
            message_type: Type of message ('error', 'warning', 'success', 'info')
        """
        msg_type: str = message_type.lower()
        if msg_type == "error":
            self.error(message)
        elif msg_type == "warning":
            self.warning(message)
        elif msg_type == "success":
            self.success(message)
        elif msg_type == "info":
            self.info(message)
        else:
            self.info(message)  # Default to info if unknown type

    def __str__(self) -> str:
        """Return string representation of the Message class."""
        return "Message(console=<Rich Console>)"

    def __repr__(self) -> str:
        """Return detailed string representation of the Message class."""
        return f"Message(console={self.console!r})"
