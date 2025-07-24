from rich.table import Table

from ..utils import get_system_identifiers

OPTIONS_DESCRIPTION = [
    {"name": "MAC Address", "description": "Spoof network interface MAC address"},
    {"name": "Machine ID", "description": "Regenerate system machine-id"},
    {"name": "Filesystem UUID", "description": "Randomize root filesystem UUID"},
    {"name": "Hostname", "description": "Set random hostname"},
    {"name": "VS Code Caches", "description": "Delete VS Code caches and extensions"},
    {"name": "User Account", "description": "Create new user account"},
]


def draw_options_table() -> Table:
    table = Table(show_header=True, header_style="bold cyan", border_style="cyan")
    table.add_column("Feature", style="yellow", width=20)
    table.add_column("Description", style="white", width=40)

    for option in OPTIONS_DESCRIPTION:
        table.add_row(option["name"], option["description"])

    return table


def draw_system_identifiers_table() -> Table:
    table = Table(show_header=True, header_style="bold cyan", border_style="cyan")
    table.add_column("Identifier", style="yellow", width=20)
    table.add_column("Current Value", style="white", width=40)

    for system_identifier, value in get_system_identifiers().items():
        display_value = value[:37] + "…" if len(value) > 40 else value
        table.add_row(system_identifier, display_value)

    return table


def draw_comparison_table(before: dict[str, str], after: dict[str, str]) -> Table:
    table = Table(show_header=True, header_style="bold cyan", border_style="cyan")
    table.add_column("Identifier", style="yellow", width=20)
    table.add_column("Before", style="dim white", width=25)
    table.add_column("After", style="bold green", width=25)
    table.add_column("Status", justify="center", width=8)

    for identifier in before.keys():
        before_val = before.get(identifier, "Unknown")
        after_val = after.get(identifier, "Unknown")

        before_display = before_val[:22] + "…" if len(before_val) > 25 else before_val
        after_display = after_val[:22] + "…" if len(after_val) > 25 else after_val
        status = "[bold green]✓" if before_val != after_val else "[dim]✗"

        table.add_row(identifier, before_display, after_display, status)

    return table
