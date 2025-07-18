#!/usr/bin/env python3

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
from rich.prompt import Confirm
from rich.text import Text

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.banner import print_banner
from ui.input import UserInput
from ui.progress import ProgressBar
from ui.tables import FeatureTable, comparison_table, identifiers_table
from utils.helpers import delete_vscode_caches, root_check
from utils.spoofer import spoof_filesystem_uuid, spoof_mac_addr, spoof_machine_id


class VSCodeSpoofer:
    def __init__(self):
        self.console = Console()
        self.feature_table = FeatureTable()
        self.user_input = UserInput()
        self.progress = ProgressBar()

        # Feature mapping to functions
        self.feature_functions = {
            "MAC Address": spoof_mac_addr,
            "Machine ID": spoof_machine_id,
            "Filesystem UUID": spoof_filesystem_uuid,
            "Hostname": self._change_hostname_wrapper,
            "VS Code Caches": self._clean_caches_wrapper,
            "New User": self._create_user_wrapper,
        }

        # User info from root check
        self.invoking_user = ""
        self.home_path = Path()

    def _clean_caches_wrapper(self) -> bool:
        return delete_vscode_caches(self.home_path)

    def _change_hostname_wrapper(self) -> bool:
        from utils.system import change_hostname

        custom_hostname = self.user_input.get_custom_hostname()
        return change_hostname(custom_hostname)

    def _create_user_wrapper(self) -> bool:
        from utils.system import create_user

        custom_username = self.user_input.get_custom_username()
        # Don't pass "vscode_sandbox" as custom since it's the default
        if custom_username == "vscode_sandbox":
            custom_username = None
        return create_user(custom_username)

    def create_layout(self) -> Layout:
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
        results = {}

        # Define realistic steps for each feature
        feature_steps = {
            "MAC Address": [
                "Detecting network interfaces",
                "Taking interface down",
                "Generating new MAC",
                "Applying new MAC",
                "Bringing interface up",
            ],
            "Machine ID": [
                "Backing up current machine-id",
                "Removing old machine-id",
                "Generating new machine-id",
                "Updating system services",
            ],
            "Filesystem UUID": [
                "Detecting filesystem type",
                "Generating new UUID",
                "Updating filesystem",
                "Updating fstab",
                "Updating bootloader",
            ],
            "Hostname": [
                "Generating new hostname",
                "Updating system hostname",
                "Updating network configuration",
            ],
            "VS Code Caches": [
                "Scanning cache directories",
                "Removing VS Code caches",
                "Removing Cursor caches",
                "Cleaning temporary files",
            ],
            "New User": [
                "Generating user credentials",
                "Creating user account",
                "Setting up home directory",
                "Configuring permissions",
            ],
        }

        with Live(
            self.progress.create_progress_display(), refresh_per_second=20
        ) as live:
            for feature in selected_features:
                if feature in self.feature_functions:
                    # Start the task
                    self.progress.start_task(feature)
                    live.update(self.progress.create_progress_display())

                    try:
                        # Execute steps with realistic progress
                        steps = feature_steps.get(feature, ["Executing operation"])
                        self.progress.execute_steps(feature, steps)
                        live.update(self.progress.create_progress_display())

                        # Execute the actual function
                        success = self.feature_functions[feature]()
                        results[feature] = success

                        # Complete the task
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

            from utils.helpers import run_cmd

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
        self.console.print("[bold cyan]Options[/bold cyan]")
        self.console.print("1. List system identifiers")
        self.console.print("2. Spoof system identifiers")
        self.console.print("3. Exit")

        while True:
            choice = input("\nSelect option (1-3): ").strip()
            if choice in ["1", "2", "3"]:
                return choice
            self.console.print("[red]Invalid choice. Please enter 1, 2, or 3.[/red]")

    def run(self) -> None:
        try:
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
                    border_style="red",
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

                    # Step 1: Get user input for feature selection (no table display)
                    selected_features = self.user_input.get_feature_selection(
                        self.feature_table.features
                    )

                    if not selected_features:
                        self.console.print("[yellow]\nNo features selected.\n[/yellow]")
                        continue

                    # Show final warning for high-risk operations
                    high_risk_features = [
                        f for f in selected_features if "Filesystem UUID" in f
                    ]
                    if high_risk_features:
                        warning_msg = (
                            "High-risk operations selected that may affect system boot. "  # noqa: E501
                            "Ensure you have a recovery method available."
                        )
                        self.console.print(f"[yellow]Warning: {warning_msg}[/yellow]")
                        risk_confirm = Confirm.ask(
                            "Do you understand the risks?", default=False
                        )
                        if not risk_confirm:
                            cancel_text = "Operation cancelled."
                            cancel_panel = Panel(
                                cancel_text,
                                border_style="yellow",
                                width=len(cancel_text) + 4,  # +4 for border and padding
                                expand=False,
                                padding=(0, 1),
                            )
                            self.console.print()  # Add spacing before
                            self.console.print(cancel_panel)
                            self.console.print()  # Add spacing after
                            continue

                    # Final verification
                    if not selected_features:
                        no_features_text = "No features selected."
                        no_features_panel = Panel(
                            no_features_text,
                            border_style="yellow",
                            width=len(no_features_text) + 4,
                            expand=False,
                            padding=(0, 1),
                        )
                        self.console.print()  # Add spacing before
                        self.console.print(no_features_panel)
                        self.console.print()  # Add spacing after
                        continue

                    count = len(selected_features)
                    # Create bullet point list of selected features
                    feature_list = []
                    for feature in selected_features:
                        feature_list.append(f"  • {feature}")

                    selected_text = (
                        f"Options{count}:\n" +
                        "\n".join(feature_list)
                    )
                    selected_panel = Panel(
                        selected_text,
                        border_style="cyan",
                        expand=False,
                        padding=(0, 1),
                    )
                    self.console.print()  # Add spacing before
                    self.console.print(selected_panel)
                    self.console.print()  # Add spacing after
                    if not Confirm.ask("Proceed with spoofing?", default=False):
                        cancel_text = "Operation cancelled."
                        cancel_panel = Panel(
                            cancel_text,
                            border_style="yellow",
                            width=len(cancel_text) + 4,  # +4 for border and padding
                            expand=False,
                            padding=(0, 1),
                        )
                        self.console.print()  # Add spacing before
                        self.console.print(cancel_panel)
                        self.console.print()  # Add spacing after
                        continue

                    # Step 2: Capture before state and execute features
                    from utils.helpers import get_identifiers

                    before_identifiers = get_identifiers()

                    self.run_selected_features(selected_features)

                    # Step 3: Capture after state and display comparison
                    after_identifiers = get_identifiers()

                    self.console.print()
                    comparison = comparison_table(before_identifiers, after_identifiers)
                    self.console.print(comparison)
                    self.console.print()

                elif choice == "3":
                    self.console.print("[yellow]Exiting...[/yellow]")
                    break

        except KeyboardInterrupt:
            # Create a panel that's exactly the width of the text
            cancel_text = "Operation cancelled by user."
            cancel_panel = Panel(
                cancel_text,
                title="[bold yellow]Cancelled[/bold yellow]",
                border_style="yellow",
                width=len(cancel_text) + 4,  # +4 for border and padding
                expand=False,
                padding=(0, 1),  # Minimal padding
            )
            self.console.print()  # Add spacing before
            self.console.print(cancel_panel)
            self.console.print()  # Add spacing after
            sys.exit(0)
        except Exception as e:
            self.console.print(f"\n[red]Unexpected error: {e}[/red]")
            import traceback

            self.console.print(f"[red]Traceback: {traceback.format_exc()}[/red]")
            sys.exit(1)


def main() -> None:
    app = VSCodeSpoofer()
    app.run()


if __name__ == "__main__":
    main()
