#!/usr/bin/env python3
"""
Demo version of VS Code Spoofer - Safe testing without system changes
"""

import random
import time
import uuid
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from src.ui.banner import print_banner
from src.ui.input import UserInput
from src.ui.progress import ProgressBar
from src.ui.tables import FeatureTable


class DemoVSCodeSpoofer:
    """Demo version of VS Code Spoofer - no actual system changes."""

    def __init__(self):
        """Initialize the demo spoofer application."""
        self.console = Console()
        self.feature_table = FeatureTable()
        self.user_input = UserInput()
        self.progress = ProgressBar()

        # Demo system state
        self.demo_identifiers = {
            "MAC Address": "5c:28:86:bf:57:bf",
            "Machine ID": "706b8acc1acd4c4a9f6a15132bef3a7b",
            "Filesystem UUID": "d65e6196-a41a-49e5-bf9e-0bc1fbd0fc7d",
            "Hostname": "sandbox-3199",
            "VS Code Caches": "~/.vscode (cached)",
            "Users": "1 user account",
            "System Info": "Ubuntu 22.04.3 LTS (x86_64)"
        }

        # Track changes for before/after comparison
        self.original_values = self.demo_identifiers.copy()
        self.changed_values = {}

    def show_main_menu(self) -> str:
        """Show main menu and get user choice."""
        self.console.print("[bold cyan]Main Menu[/bold cyan]")
        self.console.print("1. List system identifiers")
        self.console.print("2. Apply spoofing features")
        self.console.print("3. Show system information")
        self.console.print("4. Exit")

        while True:
            choice = input("\nSelect option (1-4): ").strip()
            if choice in ["1", "2", "3", "4"]:
                return choice
            self.console.print("[red]Invalid choice. Please enter 1, 2, 3, or 4.[/red]")

    def show_current_identifiers(self) -> None:
        """Display current system identifiers."""
        from rich.table import Table

        table = Table(
            title="Current System Identifiers",
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
        )

        table.add_column("Identifier", style="yellow", width=20)
        table.add_column("Current Value", style="white", width=40)

        for identifier, value in self.demo_identifiers.items():
            if identifier in ["VS Code Caches", "Users", "System Info"]:
                continue  # Skip non-identifier entries

            table.add_row(identifier, value)

        self.console.print(table)

    def simulate_feature_execution(self, selected_features: list[str]) -> dict[str, bool]:
        """Simulate executing selected features with realistic timing and occasional failures."""
        results = {}

        with Live(
            self.progress.create_progress_display(), refresh_per_second=10
        ) as live:
            for feature in selected_features:
                # Update progress
                self.progress.start_task(feature)
                live.update(self.progress.create_progress_display())

                # Simulate realistic execution time
                if feature == "Filesystem UUID":
                    time.sleep(random.uniform(3.0, 5.0))  # Longer for risky operations
                elif feature == "New User":
                    time.sleep(random.uniform(2.0, 3.5))  # User creation takes time
                else:
                    time.sleep(random.uniform(1.0, 2.5))  # Normal operations

                # Simulate occasional failures (10% failure rate for realism)
                success = random.random() > 0.1
                
                if success:
                    # Update demo values to simulate changes
                    self._apply_demo_change(feature)
                    results[feature] = True
                    self.progress.complete_task(feature, True)
                else:
                    results[feature] = False
                    self.progress.complete_task(feature, False)
                
                live.update(self.progress.create_progress_display())

        return results

    def _apply_demo_change(self, feature: str) -> None:
        """Apply simulated changes to demo system state."""
        if feature == "MAC Address":
            # Generate random MAC
            mac_parts = [f"{random.randint(0, 255):02x}" for _ in range(6)]
            new_mac = ":".join(mac_parts)
            self.changed_values["MAC Address"] = new_mac
            self.demo_identifiers["MAC Address"] = new_mac
            
        elif feature == "Machine ID":
            # Generate random machine ID
            new_id = uuid.uuid4().hex
            self.changed_values["Machine ID"] = new_id
            self.demo_identifiers["Machine ID"] = new_id
            
        elif feature == "Filesystem UUID":
            # Generate random UUID
            new_uuid = str(uuid.uuid4())
            self.changed_values["Filesystem UUID"] = new_uuid
            self.demo_identifiers["Filesystem UUID"] = new_uuid
            
        elif feature == "Hostname":
            # Generate random hostname
            adjectives = ["swift", "bright", "clever", "quiet", "bold", "calm"]
            nouns = ["falcon", "tiger", "eagle", "wolf", "bear", "fox"]
            adj = random.choice(adjectives)
            noun = random.choice(nouns)
            num = random.randint(100, 999)
            new_hostname = f"{adj}-{noun}-{num}"
            self.changed_values["Hostname"] = new_hostname
            self.demo_identifiers["Hostname"] = new_hostname
            
        elif feature == "VS Code Caches":
            self.changed_values["VS Code Caches"] = "~/.vscode (cleared)"
            self.demo_identifiers["VS Code Caches"] = "~/.vscode (cleared)"
            
        elif feature == "New User":
            self.changed_values["Users"] = "2 user accounts (+sandbox)"
            self.demo_identifiers["Users"] = "2 user accounts (+sandbox)"

        elif feature == "System Info":
            # System Info doesn't change anything, just displays information
            self.changed_values["System Info"] = "Information displayed"
            self.demo_identifiers["System Info"] = "Information displayed"

    def show_before_after_comparison(self, selected_features: list[str]) -> None:
        """Show side-by-side before and after comparison of planned changes."""
        from rich.columns import Columns
        from rich.table import Table

        # Before table (current values) - left-bound
        before_table = Table(title="CURRENT VALUES", show_header=True, header_style="bold yellow")
        before_table.add_column("Identifier", style="yellow", width=20)
        before_table.add_column("Current Value", style="white", width=35)

        # After table (planned values) - left-bound
        after_table = Table(title="PLANNED VALUES", show_header=True, header_style="bold green")
        after_table.add_column("Identifier", style="yellow", width=20)
        after_table.add_column("New Value", style="green", width=35)

        # Generate planned changes for preview
        for feature in selected_features:
            if feature == "MAC Address":
                # Generate random MAC
                mac_parts = [f"{random.randint(0, 255):02x}" for _ in range(6)]
                new_mac = ":".join(mac_parts)
                before_table.add_row("MAC Address", self.original_values["MAC Address"])
                after_table.add_row("MAC Address", new_mac)

            elif feature == "Machine ID":
                # Generate random machine ID
                new_id = uuid.uuid4().hex
                before_table.add_row("Machine ID", self.original_values["Machine ID"])
                after_table.add_row("Machine ID", new_id)

            elif feature == "Filesystem UUID":
                # Generate random UUID
                new_uuid = str(uuid.uuid4())
                before_table.add_row("Filesystem UUID", self.original_values["Filesystem UUID"])
                after_table.add_row("Filesystem UUID", new_uuid)

            elif feature == "Hostname":
                # Generate random hostname
                adjectives = ["swift", "bright", "clever", "quiet", "bold", "calm"]
                nouns = ["falcon", "tiger", "eagle", "wolf", "bear", "fox"]
                adj = random.choice(adjectives)
                noun = random.choice(nouns)
                num = random.randint(100, 999)
                new_hostname = f"{adj}-{noun}-{num}"
                before_table.add_row("Hostname", self.original_values["Hostname"])
                after_table.add_row("Hostname", new_hostname)

            elif feature == "VS Code Caches":
                before_table.add_row("VS Code Caches", self.original_values["VS Code Caches"])
                after_table.add_row("VS Code Caches", "~/.vscode (cleared)")

            elif feature == "New User":
                before_table.add_row("Users", self.original_values["Users"])
                after_table.add_row("Users", "2 user accounts (+sandbox)")

            elif feature == "System Info":
                before_table.add_row("System Info", "Not displayed")
                after_table.add_row("System Info", "Comprehensive info shown")

        # Display side by side
        if before_table.row_count > 0:
            self.console.print(Columns([before_table, after_table]))
        else:
            self.console.print("[yellow]No changes to display.[/yellow]")

    def show_execution_results(self, results: dict[str, bool]) -> None:
        """Show execution results in a left-bound table with status updates."""
        from rich.table import Table

        # Results table - left-bound
        results_table = Table(title="EXECUTION RESULTS", show_header=True, header_style="bold cyan")
        results_table.add_column("Feature", style="cyan", width=20)
        results_table.add_column("Status", style="white", width=15)
        results_table.add_column("Details", style="dim white", width=35)

        success_count = 0
        for feature, success in results.items():
            if success:
                status = "[green]✓ Success[/green]"
                details = f"{feature} has been modified"
                success_count += 1
            else:
                status = "[red]✗ Failed[/red]"
                details = f"Failed to modify {feature}"

            results_table.add_row(feature, status, details)

        self.console.print(results_table)

        # Summary
        total = len(results)
        if success_count == total:
            summary_style = "green"
            summary_text = f"✓ All {total} operations completed successfully!"
        elif success_count > 0:
            summary_style = "yellow"
            summary_text = f"! {success_count}/{total} operations completed successfully"
        else:
            summary_style = "red"
            summary_text = "✗ All operations failed"

        self.console.print()
        self.console.print(f"[bold {summary_style}]{summary_text}[/bold {summary_style}]")

    def show_system_info(self) -> None:
        """Display comprehensive system information in a left-bound table."""
        from rich.table import Table
        import platform


        # System Information table - left-bound
        info_table = Table(title="SYSTEM INFORMATION", show_header=True, header_style="bold cyan")
        info_table.add_column("Category", style="yellow", width=20)
        info_table.add_column("Information", style="white", width=50)

        # Gather system information (simulated for demo)
        system_info = {
            "Operating System": "Ubuntu 22.04.3 LTS",
            "Kernel Version": "5.15.0-91-generic",
            "Architecture": "x86_64",
            "CPU": "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz",
            "Memory": "16.0 GB",
            "Disk Space": "512 GB SSD",
            "Network Interfaces": "eth0, lo",
            "Python Version": f"{platform.python_version()}",
            "Current User": "demo_user",
            "Home Directory": "/home/demo_user",
            "Shell": "/bin/bash",
            "Timezone": "UTC",
            "Uptime": "2 days, 14:32:15",
            "Load Average": "0.15, 0.23, 0.18"
        }

        for category, info in system_info.items():
            info_table.add_row(category, info)

        self.console.print(info_table)

        # Additional network information table
        network_table = Table(title="NETWORK CONFIGURATION", show_header=True, header_style="bold green")
        network_table.add_column("Interface", style="cyan", width=15)
        network_table.add_column("IP Address", style="white", width=18)
        network_table.add_column("MAC Address", style="white", width=20)
        network_table.add_column("Status", style="white", width=12)

        # Demo network interfaces
        network_info = [
            ("eth0", "192.168.1.100", self.demo_identifiers["MAC Address"], "[green]UP[/green]"),
            ("lo", "127.0.0.1", "00:00:00:00:00:00", "[green]UP[/green]"),
        ]

        for interface, ip, mac, status in network_info:
            network_table.add_row(interface, ip, mac, status)

        self.console.print()
        self.console.print(network_table)

    def run(self) -> None:
        """Main demo application loop."""
        try:
            # Print banner first
            print_banner()
            
            # Show demo notice
            demo_notice = Panel(
                "[bold green]DEMO MODE ACTIVE[/bold green]\n\n"
                "This is a safe demonstration version.\n"
                "No actual system changes will be made.\n"
                "All operations are simulated for testing purposes.",
                title="[bold green]Demo Information[/bold green]",
                border_style="green"
            )
            self.console.print(demo_notice)
            self.console.print()

            # Main menu loop
            while True:
                choice = self.show_main_menu()
                
                if choice == "1":
                    # List system identifiers
                    self.console.print()
                    self.show_current_identifiers()
                    self.console.print()
                    
                elif choice == "2":
                    # Apply spoofing features - Three-step flow
                    self.console.print()

                    # Step 1: Feature selection
                    self.console.print("[bold cyan]Step 1: Feature Selection[/bold cyan]")
                    selected_features = self.user_input.get_feature_selection(
                        self.feature_table.features
                    )

                    if not selected_features:
                        self.console.print("[yellow]No features selected.[/yellow]")
                        continue

                    # Step 2: Before/After identifier comparison
                    self.console.print()
                    self.console.print("[bold cyan]Step 2: Before/After Comparison[/bold cyan]")
                    self.show_before_after_comparison(selected_features)

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

                    # Step 3: Progress display
                    self.console.print()
                    self.console.print("[bold cyan]Step 3: Execution Progress[/bold cyan]")
                    results = self.simulate_feature_execution(selected_features)

                    # Show final results
                    self.console.print()
                    self.show_execution_results(results)
                    self.console.print()
                    
                elif choice == "3":
                    self.console.print("[yellow]Exiting demo...[/yellow]")
                    break

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Demo interrupted by user.[/yellow]")
        except Exception as e:
            error_panel = Panel(
                f"[red]Demo Error: {e}[/red]\n\nThis is a demo error simulation.",
                title="[bold red]Demo Error[/bold red]",
                border_style="red"
            )
            self.console.print(error_panel)


def main() -> None:
    """Main entry point for the demo application."""
    demo = DemoVSCodeSpoofer()
    demo.run()


if __name__ == "__main__":
    main()
