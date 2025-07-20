#!/usr/bin/env python3
"""
User Input Module - Handles user interaction and feature selection
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.text import Text


class Input:
    """Handles user input and interaction for the VS Code Spoofer."""

    def __init__(self):
        """Initialize the user input handler."""
        self.console = Console()

    def get_feature_selection(self, features: list[dict]) -> list[str]:
        """
        Get user selection of features to execute through individual prompts.

        Args:
            features: List of feature dictionaries with name, description, etc.

        Returns:
            List of selected feature names
        """
        selected_features = []

        # Go through each feature individually
        if Confirm.ask("Spoof MAC address?", default=True):
            selected_features.append("MAC Address")

        if Confirm.ask("Regenerate Machine ID?", default=True):
            selected_features.append("Machine ID")

        if Confirm.ask("Randomize Filesystem UUID?", default=True):
            selected_features.append("Filesystem UUID")

        if Confirm.ask("Change hostname?", default=True):
            selected_features.append("Hostname")
            if Confirm.ask("Use random hostname?", default=True):
                self._custom_hostname = None
            else:
                hostname = Prompt.ask("Enter hostname")
                self._custom_hostname = hostname

        if Confirm.ask("Clear VS Code caches?", default=True):
            selected_features.append("VS Code Caches")

        if Confirm.ask("Create new user?", default=True):
            selected_features.append("New User")
            if Confirm.ask("Use random username?", default=True):
                self._custom_username = None
            else:
                username = Prompt.ask("Enter username")
                self._custom_username = username

        return selected_features


    def get_custom_hostname(self) -> str | None:
        """Get the custom hostname if set."""
        return getattr(self, '_custom_hostname', None)

    def get_custom_username(self) -> str | None:
        """Get the custom username if set."""
        return getattr(self, '_custom_username', None)

    def display_warning(self, message: str) -> None:
        """
        Display a warning message to the user.

        Args:
            message: Warning message to display
        """
        warning_panel = Panel(
            Text(message, style="bold yellow"),
            title="[bold yellow]Warning[/bold yellow]",
            border_style="yellow",
            padding=(1, 2),
        )
        self.console.print(warning_panel)

    def display_error(self, message: str) -> None:
        """
        Display an error message to the user.

        Args:
            message: Error message to display
        """
        error_panel = Panel(
            Text(message, style="bold red"),
            title="[bold red]✗ Error[/bold red]",
            border_style="red",
            padding=(1, 2),
        )
        self.console.print(error_panel)

    def display_success(self, message: str) -> None:
        """
        Display a success message to the user.

        Args:
            message: Success message to display
        """
        success_panel = Panel(
            Text(message, style="bold green"),
            title="[bold green]✓ Success[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
        self.console.print(success_panel)
