#!/usr/bin/env python3
"""
Linux VS Code Spoofer - Beautiful Rich TUI

Script to wipe every host-side identifier that intrusive VS Code
extensions or forks, such as Augment Code and Cursor, tend to log.

Features:
1. MAC:               Spoof MAC of the first active, non-loopback NIC.
2. Machine ID:        Regenerate machine-id.
3. Filesystem UUID:   Randomize root-filesystem UUID.
4. Hostname:          Set a fresh hostname.
5. VS Code Cache:     Purge VS Code, Cursor, and Augment Code caches.
6. New User:          Create a throw-away user.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable

from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text

from utils.cleaner import clean_vscode_caches
from utils.helper import parse_args, root_check
from utils.spoofer import spoof_fs_uuid, spoof_mac_addr, spoof_machine_id
from utils.system import change_hostname, create_user, update_boot_config

console: Console = Console()


def create_header() -> Panel:
    """Create the application header."""
    title: Text = Text("🔒 Linux VS Code Spoofer", style="bold magenta")
    subtitle: Text = Text(
        "Reset host fingerprints for VS Code extensions", style="dim cyan"
    )
    header_text: Text = Text.assemble(title, "\n", subtitle)
    return Panel(
        Align.center(header_text),
        style="bright_blue",
        padding=(1, 2),
    )


def create_features_table() -> Table:
    """Create a table showing available features."""
    table: Table = Table(
        title="🛡️ Available Security Features", show_header=True
    )
    table.add_column("Feature", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Risk Level", justify="center")

    features: list[tuple[str, str, str]] = [
        ("MAC Address", "Spoof network interface MAC", "🟢 Low"),
        ("Machine ID", "Regenerate system machine-id", "🟢 Low"),
        ("Filesystem UUID", "Randomize root filesystem UUID", "🟡 Medium"),
        ("Hostname", "Set random hostname", "🟢 Low"),
        ("VS Code Caches", "Purge editor caches", "🟢 Low"),
        ("New User", "Create sandbox user account", "🟢 Low"),
    ]

    for feature, desc, risk in features:
        table.add_row(feature, desc, risk)

    return table


def create_status_panel(results: dict[str, bool]) -> Panel:
    """Create a status panel showing operation results."""
    table: Table = Table(show_header=False, box=None)
    table.add_column("Operation", style="cyan")
    table.add_column("Status", justify="center")

    for operation, success in results.items():
        status: str = "✅ Success" if success else "❌ Failed"
        style: str = "green" if success else "red"
        table.add_row(operation, Text(status, style=style))

    return Panel(table, title="🔍 Operation Results", style="bright_green")


def main() -> None:
    """Main application entry point."""
    args: argparse.Namespace = parse_args()
    assume_yes: bool = args.non_interactive
    skip_uuid: bool = args.no_uuid

    # Check root privileges
    try:
        _inv_user, home = root_check()
    except SystemExit:
        console.print(
            Panel(
                "❌ This script requires root privileges.\n"
                "Please run with sudo.",
                title="Permission Error",
                style="red",
            )
        )
        sys.exit(1)

    # Display header
    console.print(create_header())
    console.print()

    # Display features table
    console.print(create_features_table())
    console.print()

    # Confirmation prompt
    if not assume_yes:
        proceed: bool = Confirm.ask(
            "🚀 [bold cyan]Proceed with spoofing operations?[/bold cyan]",
            default=True,
        )
        if not proceed:
            console.print(
                Panel(
                    "Operation cancelled by user.",
                    title="Cancelled",
                    style="yellow",
                )
            )
            return

    # Progress tracking
    operations: list[tuple[str, Callable[[], bool]]] = [
        ("MAC Address", lambda: spoof_mac_addr()),
        ("Machine ID", lambda: spoof_machine_id()),
        ("Filesystem UUID", lambda: spoof_fs_uuid() if not skip_uuid else True),
        ("Hostname", lambda: change_hostname()),
        ("VS Code Caches", lambda: clean_vscode_caches(home)),
        ("Boot Config", lambda: update_boot_config()),
    ]

    # Add user creation if requested
    create_user_confirmed: bool = assume_yes or Confirm.ask(
        "👤 Create throw-away user 'vscode_sandbox'?", default=False
    )
    if create_user_confirmed:
        operations.append(("New User", lambda: create_user()))

    results: dict[str, bool] = {}

    # Create progress display
    progress: Progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
    )

    with Live(progress, console=console, refresh_per_second=10):
        task: TaskID = progress.add_task(
            "Starting operations...", total=len(operations)
        )

        for name, operation in operations:
            progress.update(task, description=f"🔄 Processing {name}...")

            try:
                success: bool = operation()
                results[name] = success
            except Exception as e:
                console.print(f"Error in {name}: {e}")
                results[name] = False

            progress.update(task, advance=1)

    console.print()
    console.print(create_status_panel(results))

    # Final message
    success_count: int = sum(results.values())
    total_count: int = len(results)

    if success_count == total_count:
        final_panel: Panel = Panel(
            "🎉 All operations completed successfully!\n\n"
            "💡 [bold yellow]Reboot now[/bold yellow] so MAC, hostname "
            "and new machine-id take full effect.",
            title="✅ Success",
            style="bright_green",
        )
    else:
        final_panel = Panel(
            f"⚠️  {success_count}/{total_count} operations completed "
            "successfully.\n\n"
            "Please check the results above and retry failed operations "
            "if needed.",
            title="⚠️  Partial Success",
            style="yellow",
        )

    console.print(final_panel)


if __name__ == "__main__":
    main()