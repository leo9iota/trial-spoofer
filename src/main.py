#!/usr/bin/env python3

from __future__ import annotations

import os
import sys
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.prompt import Confirm
from rich.table import Table

# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # Not needed with relative imports
from .core.config import get_config
from .core.spoof import (
    spoof_filesystem_uuid,
    spoof_mac_address,
    spoof_machine_id,
    spoof_vscode,
)
from .ui.banner import print_banner
from .ui.input import Input
from .ui.menu import draw_main_menu
from .ui.panel import Panel
from .ui.progress import SPOOFING_STEPS, ProgressBar
from .ui.table import OPTIONS, draw_comparison_table, draw_system_identifiers_table
from .utils import check_root, check_system_requirements, get_system_identifiers


class Main:
    def __init__(self):
        self.console = Console()
        self.config = get_config()
        self.feature_table = Table()
        self.user_input = Input()
        self.progress = ProgressBar(console=self.console)
        self.panel = Panel(console=self.console)

        # Option mapping to functions
        self.option_functions = {
            "MAC Address": spoof_mac_address,
            "Machine ID": spoof_machine_id,
            "Filesystem UUID": spoof_filesystem_uuid,
            "Hostname": change_hostname,
            "VS Code Caches": lambda: spoof_vscode(self.home_path),
            "User Account": create_new_user,
        }

        # User info from root check
        self.invoking_user = ""
        self.home_path = Path()

    def run_selected_options(self, selected_options: list[str]) -> dict[str, bool]:
        results = {}

        with Live(
            self.progress.draw_progress(),
            console=self.console,
            refresh_per_second=20,
        ):
            for option in selected_options:
                if option in self.option_functions:
                    # Start the task
                    self.progress.start_task(option)

                    try:
                        # Execute steps with realistic progress
                        steps = SPOOFING_STEPS.get(option, ["Executing operation"])
                        self.progress.execute_steps(option, steps)

                        # Execute the actual function
                        success = self.option_functions[option]()
                        results[option] = success

                        # Complete the task
                        if success:
                            self.progress.complete_task(option, True)
                        else:
                            self.progress.complete_task(option, False)
                    except Exception as e:
                        self.console.print(f"[red]Error executing {option}: {e}[/red]")
                        results[option] = False
                        self.progress.complete_task(option, False)

        return results

    def run(self) -> None:
        try:
            print_banner()

            # Check root privileges
            try:
                self.invoking_user, self.home_path = check_root()
                if not check_system_requirements():
                    sys.exit(1)
            except Exception as e:
                # Use panel for error display
                error_text = (
                    f"Error: {e}\n\n"
                    "This tool requires root privileges to modify system identifiers."
                )
                self.panel.error(error_text, "Permission Error")
                sys.exit(1)

            # Main menu loop
            while True:
                choice = draw_main_menu()

                if choice == "1":
                    # List system identifiers
                    self.console.print()
                    self.console.print(draw_system_identifiers_table())
                    self.console.print()

                elif choice == "2":
                    # Apply spoofing features
                    self.console.print()

                    # Step 1: Get user input for feature selection (no table display)
                    selected_features = self.user_input.get_feature_selection(OPTIONS)

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
                            self.console.print()
                            self.panel.warning("Operation cancelled.")
                            self.console.print()
                            continue

                    # Final verification
                    if not selected_features:
                        self.console.print()
                        self.panel.warning("No features selected.")
                        self.console.print()
                        continue

                    count = len(selected_features)
                    # Create bullet point list of selected features
                    feature_list = []
                    for feature in selected_features:
                        feature_list.append(f"  • {feature}")

                    selected_text = f"Options selected: {count}\n" + "\n".join(
                        feature_list
                    )
                    self.console.print()
                    self.panel.info(selected_text, "Selected Features")
                    self.console.print()
                    if not Confirm.ask("Proceed with spoofing?", default=False):
                        self.console.print()
                        self.panel.warning("Operation cancelled.")
                        self.console.print()
                        continue

                    # Step 2: Capture before state and execute features
                    before_identifiers = get_system_identifiers()

                    self.run_selected_options(selected_features)

                    # Step 3: Capture after state and display comparison
                    after_identifiers = get_system_identifiers()

                    self.console.print()
                    comparison = draw_comparison_table(
                        before_identifiers, after_identifiers
                    )
                    self.console.print(comparison)
                    self.console.print()

                elif choice == "3":
                    self.console.print("[yellow]Exiting...[/yellow]")
                    break

        except KeyboardInterrupt:
            self.console.print()
            self.panel.warning("Operation cancelled by user.", "Cancelled")
            self.console.print()
            sys.exit(0)
        except Exception as e:
            self.console.print(f"\n[red]Unexpected error: {e}[/red]")
            import traceback

            self.console.print(f"[red]Traceback: {traceback.format_exc()}[/red]")
            sys.exit(1)


def main():
    """Entry point for the application."""
    app = Main()
    app.run()


if __name__ == "__main__":
    # Handle both direct execution and module execution
    try:
        main()
    except ImportError:
        # Fallback for direct execution - add current directory to path
        import os
        import sys

        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

        # Re-import with absolute imports
        from core.config import get_config
        from utils import check_root, check_system_requirements, get_system_identifiers
        from core.spoof import (
            spoof_filesystem_uuid,
            spoof_mac_address,
            spoof_machine_id,
            spoof_vscode,
        )
        from core.system import change_hostname, create_new_user
        from ui.banner import print_banner
        from ui.input import Input
        from ui.menu import draw_main_menu
        from ui.panel import Panel
        from ui.progress import SPOOFING_STEPS, ProgressBar
        from ui.table import OPTIONS, draw_comparison_table, draw_system_identifiers_table

        # Recreate Main class with absolute imports
        globals().update(locals())
        main()
