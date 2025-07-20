#!/usr/bin/env python3

from __future__ import annotations

import os
import sys
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.prompt import Confirm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.banner import print_banner
from ui.input import Input
from ui.progress import ProgressBar
from utils.helpers import delete_vscode_caches, root_check
from utils.spoofer import spoof_filesystem_uuid, spoof_mac_addr, spoof_machine_id


class Spoofer:
    def __init__(self):
        self.console = Console()
        self.feature_table = Table()
        self.user_input = Input()
        self.progress = ProgressBar(console=self.console)

        # Feature mapping to functions
        self.feature_functions = {
            "MAC Address": spoof_mac_addr,
            "Machine ID": spoof_machine_id,
            "Filesystem UUID": spoof_filesystem_uuid,
            "Hostname": lambda: self._change_hostname(),
            "VS Code Caches": lambda: delete_vscode_caches(self.home_path),
            "New User": lambda: self._create_user(),
        }

        # User info from root check
        self.invoking_user = ""
        self.home_path = Path()

    def _change_hostname(self) -> bool:
        from utils.system import change_hostname

        custom_hostname = self.user_input.get_custom_hostname()
        return change_hostname(custom_hostname)

    def _create_user(self) -> bool:
        from utils.system import create_new_user

        custom_username = self.user_input.get_custom_username()
        # Don't pass "vscode_sandbox" as custom since it's the default
        if custom_username == "vscode_sandbox":
            custom_username = None
        return create_new_user(custom_username)

    def run_selected_features(self, selected_features: list[str]) -> dict[str, bool]:
        results = {}

        with Live(
            self.progress.draw_progress(),
            console=self.console,
            refresh_per_second=20,
        ):
            for feature in selected_features:
                if feature in self.feature_functions:
                    # Start the task
                    self.progress.start_task(feature)

                    try:
                        # Execute steps with realistic progress
                        steps = feature_steps.get(feature, ["Executing operation"])
                        self.progress.execute_steps(feature, steps)

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

        return results

    def draw_main_menu(self) -> str:
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
                if not self.check_system_requirements():
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
                choice = self.draw_main_menu()

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

                    selected_text = f"Options selected: {count}\n" + "\n".join(
                        feature_list
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
    app = Spoofer()
    app.run()


if __name__ == "__main__":
    main()
