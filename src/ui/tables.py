#!/usr/bin/env python3

from rich.console import Console
from rich.table import Table

from utils.helpers import get_identifiers


class FeatureTable:
    def __init__(self):
        self.console = Console()

        # Define all available features with their properties
        self.features = [
            {
                "name": "MAC Address",
                "description": "Spoof network interface MAC address",
            },
            {
                "name": "Machine ID",
                "description": "Regenerate system machine-id",
            },
            {
                "name": "Filesystem UUID",
                "description": "Randomize root filesystem UUID",
            },
            {
                "name": "Hostname",
                "description": "Set random hostname",
            },
            {
                "name": "VS Code Caches",
                "description": "Delete VS Code caches and extensions",
            },
            {
                "name": "New User",
                "description": "Create new user account",
            },
        ]


def identifiers_table() -> Table:
    table = Table(
        show_header=True,
        header_style="bold cyan",
        border_style="cyan",
    )

    table.add_column("Identifier", style="yellow", width=20)
    table.add_column("Current Value", style="white", width=40)

    # Get current system identifiers
    identifiers = get_identifiers()

    for identifier, value in identifiers.items():
        table.add_row(identifier, value)

    return table



def comparison_table(before_data: dict[str, str], after_data: dict[str, str]) -> Table:
    """Create a side-by-side comparison table of before and after values."""
    table = Table(
        show_header=True,
        header_style="cyan",
        border_style="cyan",
    )

    table.add_column("Identifier", style="yellow", width=20)
    table.add_column("Before", style="dim white", width=25)
    table.add_column("After", style="bold green", width=25)
    table.add_column("Status", justify="center", width=12)

    for identifier in before_data.keys():
        before_value = before_data.get(identifier, "Unknown")
        after_value = after_data.get(identifier, "Unknown")

        # Truncate long values for display
        before_display = (
            before_value[:22] + "..." if len(before_value) > 25 else before_value
        )
        after_display = (
            after_value[:22] + "..." if len(after_value) > 25 else after_value
        )

        # Determine status
        if before_value != after_value:
            status_text = "[bold green]✓[/bold green]"
        else:
            status_text = "[dim]✗[/dim]"

        table.add_row(identifier, before_display, after_display, status_text)

    return table
