#!/usr/bin/env python3
"""
VS Code Spoofer main application entry point
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

import os

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.banner import print_banner
from ui.input import UserInput
from ui.progress import ProgressBar
from ui.tables import FeatureTable, identifiers_table
from utils.helpers import clean_vscode_caches, root_check
from utils.spoofer import spoof_filesystem_uuid, spoof_mac_addr, spoof_machine_id
from utils.system import change_hostname, create_user


class VSCodeSpoofer:
    """Main application class for VS Code Spoofer."""

    def __init__(self):
        """Initialize the spoofer application."""
        self.console = Console()
        self.feature_table = FeatureTable()
        self.user_input = UserInput()
        self.progress = ProgressBar()

        # Feature mapping to functions
        self.feature_functions = {
            "MAC Address": spoof_mac_addr,
            "Machine ID": spoof_machine_id,
            "Filesystem UUID": spoof_filesystem_uuid,
            "Hostname": change_hostname,
            "VS Code Caches": self._clean_caches_wrapper,
            "New User": create_user,
        }

        # User info from root check
        self.invoking_user = ""
        self.home_path = Path()

    def _clean_caches_wrapper(self) -> bool:
        """Wrapper for cache cleaning that uses the correct home path."""
        return clean_vscode_caches(self.home_path)



    def create_layout(self) -> Layout:
        """Create the main application layout."""
        layout = Layout()

        layout.split_column(
            Layout(self.display_header(), name="header", size=6),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3),
        )

        layout["main"].split_row(
            Layout(name="left", ratio=2), Layout(name="right", ratio=3)
        )

        return layout

    def run_selected_features(self, selected_features: list[str]) -> dict[str, bool]:
        """Execute the selected spoofing features."""
        results = {}

        with Live(
            self.progress.create_progress_display(), refresh_per_second=10
        ) as live:
            for feature in selected_features:
                if feature in self.feature_functions:
                    # Update progress
                    self.progress.start_task(feature)
                    live.update(self.progress.create_progress_display())

                    # Execute the function
                    try:
                        success = self.feature_functions[feature]()
                        results[feature] = success

                        # Update progress with result
                        if success:
                            self.progress.complete_task(feature, True)
                        else:
                            self.progress.complete_task(feature, False)
                    except Exception as e:
                        self.console.print(f"[red]Error executing {feature}: {e}[/red]")
                        results[feature] = False
                        self.progress.complete_task(feature, False)

                    live.update(self.progress.create_progress_display())

        return results





    def display_results(self, results: dict[str, bool]) -> None:
        """Display the results of the spoofing operations."""
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)

        if success_count == total_count:
            status_style = "green"
            status_text = "✓ All operations completed successfully!"
        elif success_count > 0:
            status_style = "yellow"
            status_text = (
                f"! {success_count}/{total_count} operations completed successfully"
            )
        else:
            status_style = "red"
            status_text = "✗ All operations failed"

        results_text = Text()
        results_text.append(f"{status_text}\n\n", style=f"bold {status_style}")

        for feature, success in results.items():
            if success:
                results_text.append(f"✓ {feature}: Success\n", style="green")
            else:
                results_text.append(f"✗ {feature}: Failed\n", style="red")

        if any(results.values()):
            results_text.append(
                "\nReboot recommended to apply all changes", style="bold yellow"
            )

        panel = Panel(
            results_text,
            title="[bold]Execution Results[/bold]",
            border_style="blue",
            padding=(1, 2),
        )

        self.console.print(panel)

    def _validate_system_requirements(self) -> bool:
        """Validate system requirements before execution."""
        try:
            # Check if we're on Linux
            import platform

            if platform.system() != "Linux":
                self.user_input.display_error("This tool only works on Linux systems.")
                return False

            # Check for required commands
            required_commands = ["ip", "systemctl", "hostnamectl"]
            missing_commands = []

            from .utils.helpers import run_cmd

            for cmd in required_commands:
                try:
                    run_cmd(f"which {cmd}", capture=True)
                except Exception:
                    missing_commands.append(cmd)

            if missing_commands:
                self.user_input.display_error(
                    f"Missing required commands: {', '.join(missing_commands)}"
                )
                return False

            return True

        except Exception as e:
            self.user_input.display_error(f"System validation failed: {e}")
            return False

    def show_main_menu(self) -> str:
        """Show main menu and get user choice."""
        self.console.print("[bold cyan]Main Menu[/bold cyan]")
        self.console.print("1. List system identifiers")
        self.console.print("2. Apply spoofing features")
        self.console.print("3. Exit")

        while True:
            choice = input("\nSelect option (1-3): ").strip()
            if choice in ["1", "2", "3"]:
                return choice
            self.console.print("[red]Invalid choice. Please enter 1, 2, or 3.[/red]")



    def run(self) -> None:
        """Main application loop."""
        try:
            # Print banner first
            print_banner()

            # Check root privileges
            try:
                self.invoking_user, self.home_path = root_check()
                if not self._validate_system_requirements():
                    sys.exit(1)
            except Exception as e:
                # Use panel only for non-sudo error
                error_text = (
                    f"[red]Error: {e}[/red]\n\n"
                    "This tool requires root privileges to modify system identifiers."
                )
                error_panel = Panel(
                    error_text,
                    title="[bold red]Permission Error[/bold red]",
                    border_style="red"
                )
                self.console.print(error_panel)
                sys.exit(1)


            # Main menu loop
            while True:
                choice = self.show_main_menu()

                if choice == "1":
                    # List system identifiers
                    self.console.print()
                    self.console.print(identifiers_table())
                    self.console.print()

                elif choice == "2":
                    # Apply spoofing features
                    self.console.print()

                    # Show available features and get user selection
                    self.console.print(self.feature_table.create_info_table())
                    self.console.print()

                    # Get user input for feature selection
                    selected_features = self.user_input.get_feature_selection(
                        self.feature_table.features
                    )

                    if not selected_features:
                        self.console.print("[yellow]No features selected.[/yellow]")
                        continue

                    # Show final warning for high-risk operations
                    high_risk_features = [
                        f for f in selected_features if "Filesystem UUID" in f
                    ]
                    if high_risk_features:
                        self.user_input.display_warning(
                            "You have selected high-risk operations that may affect "
                            "system boot. Ensure you have a recovery method available."
                        )
                        if not self.user_input.get_user_confirmation(
                            "Do you understand the risks and want to continue?", False
                        ):
                            self.console.print("[yellow]Operation cancelled.[/yellow]")
                            continue

                    # Confirm execution
                    if not self.user_input.confirm_execution(selected_features):
                        self.console.print("[yellow]Operation cancelled.[/yellow]")
                        continue

                    # Execute features
                    results = self.run_selected_features(selected_features)

                    # Display results
                    self.console.print()
                    self.display_results(results)
                    self.console.print()

                elif choice == "3":
                    self.console.print("[yellow]Exiting...[/yellow]")
                    break

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled by user.[/yellow]")
            sys.exit(0)
        except Exception as e:
            self.console.print(f"\n[red]Unexpected error: {e}[/red]")
            import traceback

            self.console.print(f"[red]Traceback: {traceback.format_exc()}[/red]")
            sys.exit(1)


def main() -> None:
    """Main entry point for the application."""
    app = VSCodeSpoofer()
    app.run()


if __name__ == "__main__":
    main()
