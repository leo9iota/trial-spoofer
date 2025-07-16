#!/usr/bin/env python3
"""
Demo script to showcase the Rich TUI interface without requiring root privileges.
"""

from __future__ import annotations

import random
import time

from rich.align import Align
from rich.console import Console
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


def demo_operation() -> bool:
    """Simulate an operation with random success/failure."""
    time.sleep(random.uniform(0.5, 2.0))  # Simulate work
    return random.choice([True, True, True, False])  # 75% success rate


def main() -> None:
    """Demo main function."""
    # Display header
    console.print(create_header())
    console.print()

    # Display features table
    console.print(create_features_table())
    console.print()

    # Confirmation prompt
    demo_prompt: str = "🚀 [bold cyan]Proceed with demo spoofing operations?[/bold cyan]"
    proceed: bool = Confirm.ask(demo_prompt, default=True)
    if not proceed:
        cancel_message: str = "Demo cancelled by user."
        cancel_panel: Panel = Panel(
            cancel_message,
            title="Cancelled",
            style="yellow",
        )
        console.print(cancel_panel)
        return

    # Demo operations
    operations: list[str] = [
        "MAC Address",
        "Machine ID",
        "Filesystem UUID",
        "Hostname",
        "VS Code Caches",
        "Boot Config",
        "New User",
    ]

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

        for operation_name in operations:
            progress_description: str = f"🔄 Processing {operation_name}..."
            progress.update(task, description=progress_description)

            success: bool = demo_operation()
            results[operation_name] = success

            progress.update(task, advance=1)

    console.print()
    console.print(create_status_panel(results))

    # Final message
    success_count: int = sum(results.values())
    total_count: int = len(results)

    if success_count == total_count:
        success_message: str = (
            "🎉 All demo operations completed successfully!\n\n"
            "💡 [bold yellow]This was just a demo[/bold yellow] - no actual "
            "system changes were made."
        )
        final_panel: Panel = Panel(
            success_message,
            title="✅ Demo Complete",
            style="bright_green",
        )
    else:
        partial_message: str = (
            f"⚠️  {success_count}/{total_count} demo operations completed "
            "successfully.\n\n"
            "💡 [bold yellow]This was just a demo[/bold yellow] - no actual "
            "system changes were made."
        )
        final_panel = Panel(
            partial_message,
            title="⚠️  Demo Complete",
            style="yellow",
        )

    console.print(final_panel)


if __name__ == "__main__":
    main()
