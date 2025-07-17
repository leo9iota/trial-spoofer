#!/usr/bin/env python3
"""
User Input Module - Handles user interaction and feature selection
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text


class UserInput:
    """Handles user input and interaction for the VS Code Spoofer."""

    def __init__(self):
        """Initialize the user input handler."""
        self.console = Console()

    def get_feature_selection(self, features: list[dict]) -> list[str]:
        """
        Get user selection of features to execute.

        Args:
            features: List of feature dictionaries with name, description, etc.

        Returns:
            List of selected feature names
        """
        self.console.print("Select features (comma-separated names or 'all'):")

        # Display feature list without numbers
        selection_table = Table(show_header=True, header_style="bold magenta")
        selection_table.add_column("Feature", style="cyan", width=20)
        selection_table.add_column("Description", style="white", width=35)
        selection_table.add_column("Risk", justify="center", width=12)

        for feature in features:
            selection_table.add_row(
                feature["name"],
                feature["description"],
                feature["risk_level"],
            )

        self.console.print(selection_table)

        # Get user selection
        while True:
            try:
                selection = Prompt.ask(
                    "[bold]Enter your selection", default="all", show_default=True
                ).strip()

                if selection.lower() == "all":
                    return [feature["name"] for feature in features]

                if selection.lower() == "none" or selection == "":
                    return []

                # Parse comma-separated feature names
                selected_names = []
                feature_names = [f["name"] for f in features]

                for item in selection.split(","):
                    item = item.strip()
                    # Try exact match first
                    if item in feature_names:
                        selected_names.append(item)
                    else:
                        # Try case-insensitive match
                        found = False
                        for fname in feature_names:
                            if fname.lower() == item.lower():
                                selected_names.append(fname)
                                found = True
                                break
                        if not found:
                            raise ValueError(f"Unknown feature: {item}")

                if not selected_names:
                    self.console.print("[yellow]No valid selections made.[/yellow]")
                    continue

                # Remove duplicates while preserving order
                seen = set()
                unique_selected = []
                for name in selected_names:
                    if name not in seen:
                        seen.add(name)
                        unique_selected.append(name)

                # Show selected features
                self.console.print("[green][+] Selected:[/green]")
                for feature_name in unique_selected:
                    self.console.print(f"  [>] {feature_name}")

                return unique_selected

            except ValueError as e:
                self.console.print(f"[red]Error: {e}[/red]")
                self.console.print(
                    "[yellow]Please enter comma-separated feature names, "
                    "'all', or 'none'[/yellow]"
                )
                feature_list = ", ".join([f["name"] for f in features])
                self.console.print(f"[dim]Available features: {feature_list}[/dim]")
                continue
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Selection cancelled.[/yellow]")
                return []

    def confirm_execution(self, selected_features: list[str]) -> bool:
        """
        Confirm execution of selected features with the user.

        Args:
            selected_features: List of selected feature names

        Returns:
            True if user confirms, False otherwise
        """
        if not selected_features:
            return False

        # Create confirmation panel
        confirmation_text = Text()
        confirmation_text.append(
            "Ready to execute the operations shown above.\n\n", style="bold"
        )

        confirmation_text.append("[>] Selected operations:\n", style="bold cyan")
        for feature in selected_features:
            confirmation_text.append(f"  [>] {feature}\n", style="white")

        confirmation_text.append("\n[!] ", style="bold yellow")
        confirmation_text.append(
            "These operations will modify your system and may require a reboot.",
            style="yellow",
        )
        confirmation_text.append("\n[!] ", style="bold yellow")
        confirmation_text.append(
            "Make sure you have backups of important data.", style="yellow"
        )

        panel = Panel(
            confirmation_text,
            title="[bold red][!] Final Confirmation[/bold red]",
            border_style="red",
            padding=(1, 2),
        )

        self.console.print(panel)

        return Confirm.ask("\n[bold]Proceed with execution?", default=False)

    def get_user_confirmation(self, message: str, default: bool = False) -> bool:
        """
        Get a yes/no confirmation from the user.

        Args:
            message: The confirmation message to display
            default: Default value if user just presses Enter

        Returns:
            True if user confirms, False otherwise
        """
        return Confirm.ask(message, default=default)

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
