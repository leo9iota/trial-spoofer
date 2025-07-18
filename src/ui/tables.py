#!/usr/bin/env python3

from rich.console import Console
from rich.table import Table

from utils.helpers import get_identifiers


class FeatureTable:
    def __init__(self):
        self.console = Console()
        self.selections: dict[str, bool] = {}

        # Define all available features with their properties
        self.features = [
            {
                "name": "MAC Address",
                "description": "Spoof network interface MAC address",
                "risk_level": "[green]Low[/green]",
                "icon": "",
                "status": "Ready",
            },
            {
                "name": "Machine ID",
                "description": "Regenerate system machine-id",
                "risk_level": "[green]Low[/green]",
                "icon": "",
                "status": "Ready",
            },
            {
                "name": "Filesystem UUID",
                "description": "Randomize root filesystem UUID",
                "risk_level": "[yellow]Medium[/yellow]",
                "icon": "",
                "status": "Ready",
            },
            {
                "name": "Hostname",
                "description": "Set random hostname",
                "risk_level": "[green]Low[/green]",
                "icon": "",
                "status": "Ready",
            },
            {
                "name": "VS Code Caches",
                "description": "Purge editor caches and extensions",
                "risk_level": "[green]Low[/green]",
                "icon": "",
                "status": "Ready",
            },
            {
                "name": "New User",
                "description": "Create sandbox user account",
                "risk_level": "[green]Low[/green]",
                "icon": "",
                "status": "Ready",
            },
            {
                "name": "System Info",
                "description": "Display comprehensive system information",
                "risk_level": "[green]Low[/green]",
                "icon": "",
                "status": "Ready",
            },
        ]

    def feature_info_table():
        print("Feature info")


# TODO: Remove wrapper function if unnecessary
def get_current_identifiers() -> dict[str, str]:
    return get_identifiers()


def identifiers_table() -> Table:
    table = Table(
        title="Current System Identifiers",
        show_header=True,
        header_style="bold cyan",
        border_style="cyan",
    )

    table.add_column("Identifier", style="yellow", width=20)
    table.add_column("Current Value", style="white", width=40)

    # Get current system identifiers
    identifiers = get_current_identifiers()

    for identifier, value in identifiers.items():
        table.add_row(identifier, value)

    return table


def modified_identifiers_table(modifications: dict[str, str]) -> Table:
    table = Table(
        title="Modified System Identifiers",
        show_header=True,
        header_style="bold green",
        border_style="green",
    )

    table.add_column("Identifier", style="yellow", width=20)
    table.add_column("Old Value", style="dim white", width=18)
    table.add_column("New Value", style="bold green", width=18)
    table.add_column("Status", justify="center", width=12)

    for identifier, new_value in modifications.items():
        # Get current/old value
        current_identifiers = get_current_identifiers()
        old_value = current_identifiers.get(identifier, "Unknown")

        # Truncate long values for display
        old_display = old_value[:15] + "..." if len(old_value) > 18 else old_value
        new_display = new_value[:15] + "..." if len(new_value) > 18 else new_value

        status_text = "[bold green][~] Modified[/bold green]"
        table.add_row(identifier, old_display, new_display, status_text)

    return table


def comparison_table(before_data: dict[str, str], after_data: dict[str, str]) -> Table:
    """Create a side-by-side comparison table of before and after values."""
    table = Table(
        title="Before/After Comparison",
        show_header=True,
        header_style="bold cyan",
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
