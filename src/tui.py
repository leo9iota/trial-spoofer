#!/usr/bin/env python3
"""
Rich-based TUI components for displaying application information,
progress, and user interactions.
"""

from __future__ import annotations

from collections.abc import Callable

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


class TUI:
    """TUI manager for the VS Code Spoofer application."""

    def __init__(self) -> None:
        """Initialize the TUI with a Rich console."""
        self.console: Console = Console()

    def create_header(self) -> Panel:
        """Create the application header."""
        title: Text = Text(
            text="🔒 Linux VS Code Spoofer", style="bold magenta"
        )
        subtitle: Text = Text(
            "Reset host fingerprints for VS Code extensions", style="dim cyan"
        )
        header_text: Text = Text.assemble(title, "\n", subtitle)
        return Panel(
            Align.center(header_text),
            style="bright_blue",
            padding=(1, 2),
        )

    def create_features_table(self) -> Table:
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

    def create_status_panel(self, results: dict[str, bool]) -> Panel:
        """Create a status panel showing operation results."""
        table: Table = Table(show_header=False, box=None)
        table.add_column("Operation", style="cyan")
        table.add_column("Status", justify="center")

        for operation, success in results.items():
            status: str = "✅ Success" if success else "❌ Failed"
            style: str = "green" if success else "red"
            table.add_row(operation, Text(status, style=style))

        return Panel(table, title="🔍 Operation Results", style="bright_green")

    def create_error_panel(self, message: str, title: str = "Error") -> Panel:
        """Create an error panel with the given message."""
        return Panel(
            message,
            title=title,
            style="red",
        )

    def create_cancel_panel(
        self, message: str = "Operation cancelled by user."
    ) -> Panel:
        """Create a cancellation panel."""
        return Panel(
            message,
            title="Cancelled",
            style="yellow",
        )

    def create_success_panel(
        self, message: str, title: str = "✅ Success"
    ) -> Panel:
        """Create a success panel."""
        return Panel(
            message,
            title=title,
            style="bright_green",
        )

    def create_warning_panel(
        self, message: str, title: str = "⚠️  Partial Success"
    ) -> Panel:
        """Create a warning panel."""
        return Panel(
            message,
            title=title,
            style="yellow",
        )

    def ask_confirmation(self, message: str, default: bool = True) -> bool:
        """Ask for user confirmation with a styled prompt."""
        return Confirm.ask(message, default=default)

    def print(self, *args, **kwargs) -> None:
        """Print to the console."""
        self.console.print(*args, **kwargs)

    def run_operations_with_progress(
        self, operations: list[tuple[str, Callable[[], bool]]]
    ) -> dict[str, bool]:
        """
        Run a list of operations with a progress display.

        Args:
            operations: List of (operation_name, operation_function) tuples

        Returns:
            Dictionary mapping operation names to success status
        """
        results: dict[str, bool] = {}

        # Create progress display
        progress: Progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self.console,
        )

        with Live(progress, console=self.console, refresh_per_second=10):
            task: TaskID = progress.add_task(
                "Starting operations...", total=len(operations)
            )

            for operation_name, operation_func in operations:
                progress_description: str = f"🔄 Processing {operation_name}..."
                progress.update(task, description=progress_description)

                try:
                    success: bool = operation_func()
                    results[operation_name] = success
                except Exception as e:
                    error_msg: str = str(e)
                    error_text: str = f"Error in {operation_name}: {error_msg}"
                    self.console.print(error_text)
                    results[operation_name] = False

                progress.update(task, advance=1)

        return results

    def display_final_results(self, results: dict[str, bool]) -> None:
        """Display the final results of all operations."""
        success_count: int = sum(results.values())
        total_count: int = len(results)

        if success_count == total_count:
            success_message: str = (
                "🎉 All operations completed successfully!\n\n"
                "💡 [bold yellow]Reboot now[/bold yellow] so MAC, hostname "
                "and new machine-id take full effect."
            )
            final_panel: Panel = self.create_success_panel(success_message)
        else:
            partial_message: str = (
                f"⚠️  {success_count}/{total_count} operations completed "
                "successfully.\n\n"
                "Please check the results above and retry failed operations "
                "if needed."
            )
            final_panel = self.create_warning_panel(partial_message)

        self.print(final_panel)


# Convenience function for creating a TUI instance
def create_tui() -> TUI:
    """Create and return a new TUI instance."""
    return TUI()
