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

        # Feature mapping to demo functions (matching real app structure)
        self.feature_functions = {
            "MAC Address": self._demo_spoof_mac_addr,
            "Machine ID": self._demo_spoof_machine_id,
            "Filesystem UUID": self._demo_spoof_filesystem_uuid,
            "Hostname": self._demo_change_hostname,
            "VS Code Caches": self._demo_clean_caches,
            "New User": self._demo_create_user,
        }

        # Demo system state
        self.demo_identifiers = {
            "MAC Address": "5c:28:86:bf:57:bf",
            "Machine ID": "706b8acc1acd4c4a9f6a15132bef3a7b",
            "Filesystem UUID": "d65e6196-a41a-49e5-bf9e-0bc1fbd0fc7d",
            "Hostname": "sandbox-3199",
            "VS Code Caches": "~/.vscode (cached)",
            "Users": "1 user account",
        }

        # Track changes for results display
        self.original_values = self.demo_identifiers.copy()
        self.changed_values = {}
        self.user_credentials = {}

        # User info from simulated root check
        self.invoking_user = "demo_user"
        self.home_path = Path("/home/demo_user")

    def _demo_spoof_mac_addr(self) -> bool:
        """Demo version of MAC address spoofing."""
        try:
            # Simulate realistic execution time
            time.sleep(random.uniform(1.0, 2.0))
            # Generate random MAC
            mac_parts = [f"{random.randint(0, 255):02x}" for _ in range(6)]
            new_mac = ":".join(mac_parts)
            self.changed_values["MAC Address"] = new_mac
            self.demo_identifiers["MAC Address"] = new_mac
            # Simulate occasional failures (10% failure rate)
            return random.random() > 0.1
        except Exception:
            return False

    def _demo_spoof_machine_id(self) -> bool:
        """Demo version of machine ID spoofing."""
        try:
            time.sleep(random.uniform(1.5, 2.5))
            new_id = uuid.uuid4().hex
            self.changed_values["Machine ID"] = new_id
            self.demo_identifiers["Machine ID"] = new_id
            return random.random() > 0.1
        except Exception:
            return False

    def _demo_spoof_filesystem_uuid(self) -> bool:
        """Demo version of filesystem UUID spoofing."""
        try:
            # Longer execution time for high-risk operation
            time.sleep(random.uniform(3.0, 5.0))
            new_uuid = str(uuid.uuid4())
            self.changed_values["Filesystem UUID"] = new_uuid
            self.demo_identifiers["Filesystem UUID"] = new_uuid
            return random.random() > 0.1
        except Exception:
            return False

    def _demo_change_hostname(self) -> bool:
        """Demo version of hostname change."""
        try:
            time.sleep(random.uniform(1.0, 2.0))
            adjectives = ["swift", "bright", "clever", "quiet", "bold", "calm"]
            nouns = ["falcon", "tiger", "eagle", "wolf", "bear", "fox"]
            adj = random.choice(adjectives)
            noun = random.choice(nouns)
            num = random.randint(100, 999)
            new_hostname = f"{adj}-{noun}-{num}"
            self.changed_values["Hostname"] = new_hostname
            self.demo_identifiers["Hostname"] = new_hostname
            return random.random() > 0.1
        except Exception:
            return False

    def _demo_clean_caches(self) -> bool:
        """Demo version of VS Code cache cleaning."""
        try:
            time.sleep(random.uniform(1.0, 2.0))
            self.changed_values["VS Code Caches"] = "~/.vscode (cleared)"
            self.demo_identifiers["VS Code Caches"] = "~/.vscode (cleared)"
            return random.random() > 0.1
        except Exception:
            return False

    def _demo_create_user(self) -> bool:
        """Demo version of user creation."""
        try:
            time.sleep(random.uniform(2.0, 3.5))
            if self.user_credentials:
                username = self.user_credentials.get("username", "sandbox")
                self.changed_values["Users"] = f"2 user accounts (+{username})"
                self.demo_identifiers["Users"] = f"2 user accounts (+{username})"
            else:
                self.changed_values["Users"] = "2 user accounts (+vscode_sandbox)"
                self.demo_identifiers["Users"] = "2 user accounts (+vscode_sandbox)"
            return random.random() > 0.1
        except Exception:
            return False

    def _validate_system_requirements(self) -> bool:
        """Simulate system requirements validation."""
        try:
            # Simulate validation checks
            self.console.print("[dim]Validating system requirements...[/dim]")
            time.sleep(0.5)

            # Always pass in demo mode
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

    def run_selected_features(self, selected_features: list[str]) -> dict[str, bool]:
        """Execute the selected spoofing features (demo version)."""
        results = {}

        with Live(
            self.progress.create_progress_display(), refresh_per_second=10
        ) as live:
            for feature in selected_features:
                if feature in self.feature_functions:
                    # Update progress
                    self.progress.start_task(feature)
                    live.update(self.progress.create_progress_display())

                    # Execute the demo function
                    try:
                        success = self.feature_functions[feature]()
                        results[feature] = success

                        # Update progress with result
                        if success:
                            self.progress.complete_task(feature, True)
                        else:
                            self.progress.complete_task(feature, False)
                    except Exception as e:
                        self.console.print(f"[red]Demo error executing {feature}: {e}[/red]")
                        results[feature] = False
                        self.progress.complete_task(feature, False)

                    live.update(self.progress.create_progress_display())

        return results

    def display_results(self, results: dict[str, bool]) -> None:
        """Display the results of the demo spoofing operations."""
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
                results_text.append(f"✓ {feature}: Success (simulated)\n", style="green")
            else:
                results_text.append(f"✗ {feature}: Failed (simulated)\n", style="red")

        if any(results.values()):
            results_text.append(
                "\n[Demo] In real mode, reboot would be recommended", style="bold yellow"
            )

        panel = Panel(
            results_text,
            title="[bold]Demo Execution Results[/bold]",
            border_style="blue",
            padding=(1, 2),
        )

        self.console.print(panel)

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

    def simulate_feature_execution(
        self, selected_features: list[str]
    ) -> dict[str, bool]:
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
            if self.user_credentials:
                username = self.user_credentials.get("username", "sandbox")
                self.changed_values["Users"] = f"2 user accounts (+{username})"
                self.demo_identifiers["Users"] = f"2 user accounts (+{username})"
            else:
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
        before_table = Table(
            title="CURRENT VALUES", header_style="bold yellow"
        )
        before_table.add_column("Identifier", style="yellow", width=20)
        before_table.add_column("Current Value", style="white", width=35)

        # After table (planned values) - left-bound
        after_table = Table(
            title="NEW VALUES", header_style="bold yellow"
        )
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
                before_table.add_row(
                    "Filesystem UUID", self.original_values["Filesystem UUID"]
                )
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
                before_table.add_row(
                    "VS Code Caches", self.original_values["VS Code Caches"]
                )
                after_table.add_row("VS Code Caches", "~/.vscode (cleared)")

            elif feature == "New User":
                before_table.add_row("Users", self.original_values["Users"])
                if self.user_credentials:
                    username = self.user_credentials.get("username", "sandbox")
                    after_table.add_row("Users", f"2 user accounts (+{username})")
                else:
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
        results_table = Table(
            title="EXECUTION RESULTS", show_header=True, header_style="bold cyan"
        )
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
            summary_text = (
                f"! {success_count}/{total} operations completed successfully"
            )
        else:
            summary_style = "red"
            summary_text = "✗ All operations failed"

        self.console.print()
        self.console.print(
            f"[bold {summary_style}]{summary_text}[/bold {summary_style}]"
        )

    def show_system_info(self) -> None:
        """Display comprehensive system information in a left-bound table."""
        from rich.table import Table
        import platform

        # System Information table - left-bound
        info_table = Table(
            title="SYSTEM INFORMATION", show_header=True, header_style="bold cyan"
        )
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
            "Load Average": "0.15, 0.23, 0.18",
        }

        for category, info in system_info.items():
            info_table.add_row(category, info)

        self.console.print(info_table)

        # Additional network information table
        network_table = Table(
            title="NETWORK CONFIGURATION", show_header=True, header_style="bold green"
        )
        network_table.add_column("Interface", style="cyan", width=15)
        network_table.add_column("IP Address", style="white", width=18)
        network_table.add_column("MAC Address", style="white", width=20)
        network_table.add_column("Status", style="white", width=12)

        # Demo network interfaces
        network_info = [
            (
                "eth0",
                "192.168.1.100",
                self.demo_identifiers["MAC Address"],
                "[green]UP[/green]",
            ),
            ("lo", "127.0.0.1", "00:00:00:00:00:00", "[green]UP[/green]"),
        ]

        for interface, ip, mac, status in network_info:
            network_table.add_row(interface, ip, mac, status)

        self.console.print()
        self.console.print(network_table)

    def show_network_info(self) -> None:
        """Display network information in a left-bound table."""
        from rich.table import Table

        # Network information table - left-bound
        network_table = Table(
            title="NETWORK INFORMATION", show_header=True, header_style="bold green"
        )
        network_table.add_column("Interface", style="cyan", width=15)
        network_table.add_column("IP Address", style="white", width=18)
        network_table.add_column("MAC Address", style="white", width=20)
        network_table.add_column("Status", style="white", width=12)
        network_table.add_column("Type", style="white", width=15)

        # Demo network interfaces
        network_info = [
            (
                "eth0",
                "192.168.1.100",
                self.demo_identifiers["MAC Address"],
                "[green]UP[/green]",
                "Ethernet",
            ),
            ("lo", "127.0.0.1", "00:00:00:00:00:00", "[green]UP[/green]", "Loopback"),
            (
                "wlan0",
                "192.168.1.101",
                "aa:bb:cc:dd:ee:ff",
                "[red]DOWN[/red]",
                "Wireless",
            ),
        ]

        for interface, ip, mac, status, net_type in network_info:
            network_table.add_row(interface, ip, mac, status, net_type)

        self.console.print(network_table)

    def show_system_modifications(self) -> None:
        """Display side-by-side comparison of what has been changed or not changed."""
        from rich.table import Table
        from rich.columns import Columns

        # Current values table
        current_table = Table(
            title="CURRENT VALUES", header_style="bold yellow"
        )
        current_table.add_column("Identifier", style="yellow", width=20)
        current_table.add_column("Current Value", style="white", width=35)

        # Modified values table
        modified_table = Table(
            title="MODIFIED VALUES", header_style="bold yellow"
        )
        modified_table.add_column("Identifier", style="yellow", width=20)
        modified_table.add_column("Modified Value", style="white", width=35)

        # Populate tables
        for identifier, original_value in self.original_values.items():
            current_value = self.demo_identifiers.get(identifier, original_value)

            # Add to current table
            display_value = str(current_value)
            if len(display_value) > 35:
                display_value = display_value[:35] + "..."
            current_table.add_row(identifier, display_value)

            # Add to modified table
            if identifier in self.changed_values:
                modified_value = self.changed_values[identifier]
                status = "✓ Modified"
                modified_table.add_row(identifier, f"{status}: {str(modified_value)[:25]}...")
            else:
                modified_table.add_row(identifier, "✗ Not modified")

        # Display tables side by side using Columns
        self.console.print()
        tables_group = Columns([current_table, modified_table], equal=True, expand=True)
        self.console.print(tables_group)
        self.console.print()

    def get_individual_feature_selection(self) -> list[str]:
        """Get feature selection by going through each feature individually."""
        from rich.prompt import Confirm

        selected_features = []

        for feature in self.feature_table.features:
            # Create simple prompt based on feature
            if feature["name"] == "MAC Address":
                prompt = "Spoof MAC address?"
            elif feature["name"] == "Machine ID":
                prompt = "Regenerate machine ID?"
            elif feature["name"] == "Filesystem UUID":
                prompt = "Randomize filesystem UUID?"
            elif feature["name"] == "Hostname":
                prompt = "Set random hostname?"
            elif feature["name"] == "VS Code Caches":
                prompt = "Clear VS Code caches?"
            elif feature["name"] == "New User":
                prompt = "Add user account?"
            elif feature["name"] == "System Info":
                prompt = "Display system info?"
            else:
                prompt = f"{feature['description']}?"

            choice = Confirm.ask(prompt, default=True)

            if choice:
                selected_features.append(feature["name"])

                # Handle user account creation - prompt immediately
                if feature["name"] == "New User":
                    self.console.print()
                    self.user_credentials = self.get_user_credentials()

        return selected_features

    def get_user_credentials(self) -> dict:
        """Get username and password for new user account."""
        from rich.prompt import Prompt, Confirm

        self.console.print()
        manual_username = Confirm.ask("Create username manually?", default=False)

        if manual_username:
            username = Prompt.ask("Enter username")
            manual_password = Confirm.ask("Create password manually?", default=False)

            if manual_password:
                password = Prompt.ask("Enter password", password=True)
            else:
                password = self.generate_random_password()
                self.console.print(f"Generated password: {password}")
        else:
            username = self.generate_random_username()
            password = self.generate_random_password()
            self.console.print(f"Generated username: {username}")
            self.console.print(f"Generated password: {password}")

        return {"username": username, "password": password}

    def generate_random_username(self) -> str:
        """Generate a random username."""
        import random

        adjectives = [
            "quick",
            "bright",
            "clever",
            "swift",
            "bold",
            "calm",
            "wise",
            "cool",
        ]
        nouns = ["fox", "wolf", "eagle", "tiger", "bear", "lion", "hawk", "deer"]
        return f"{random.choice(adjectives)}-{random.choice(nouns)}-{random.randint(10, 99)}"

    def generate_random_password(self) -> str:
        """Generate a random password."""
        import random
        import string

        length = 12
        chars = string.ascii_letters + string.digits + "!@#$%"
        return "".join(random.choice(chars) for _ in range(length))

    def get_user_action(self) -> str:
        """Get user action after showing before/after comparison."""
        from rich.prompt import Prompt

        self.console.print("[bold yellow]What would you like to do?[/bold yellow]")
        self.console.print("1. [green]Proceed[/green]")
        self.console.print("2. [red]Abort[/red]")
        self.console.print("3. [cyan]Restart[/cyan]")

        while True:
            choice = Prompt.ask(
                "Enter your choice",
                choices=["1", "2", "3", "proceed", "abort", "new"],
                default="1",
            ).lower()

            if choice in ["1", "proceed"]:
                return "proceed"
            elif choice in ["2", "abort"]:
                return "abort"
            elif choice in ["3", "new"]:
                return "new"

    def run(self) -> None:
        """Main demo application loop."""
        try:
            print_banner()

            # Show demo notice
            demo_notice = Panel(
                "[bold green]DEMO MODE ACTIVE[/bold green]\n\n"
                "This is a safe demonstration version.\n"
                "No actual system changes will be made.\n"
                "All operations are simulated for testing purposes.",
                title="[bold green]Demo Information[/bold green]",
                border_style="green",
            )
            self.console.print(demo_notice)
            self.console.print()

            # Simulate root check and system validation
            try:
                # Simulate the root check process
                self.console.print("[dim]Simulating root privileges check...[/dim]")
                time.sleep(0.5)
                if not self._validate_system_requirements():
                    import sys
                    sys.exit(1)
            except Exception as e:
                # Simulate permission error
                error_text = (
                    f"[red]Demo Error: {e}[/red]\n\n"
                    "This tool requires root privileges to modify system identifiers."
                )
                error_panel = Panel(
                    error_text,
                    title="[bold red]Demo Permission Error[/bold red]",
                    border_style="red",
                )
                self.console.print(error_panel)
                import sys
                sys.exit(1)

            # Main menu loop
            while True:
                choice = self.show_main_menu()

                if choice == "1":
                    # List system identifiers
                    self.console.print()
                    self.show_current_identifiers()
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
                    self.console.print("[yellow]Exiting demo...[/yellow]")
                    break

        except KeyboardInterrupt:
            self.console.print("\n[yellow]Demo operation cancelled by user.[/yellow]")
            import sys
            sys.exit(0)
        except Exception as e:
            self.console.print(f"\n[red]Demo unexpected error: {e}[/red]")
            import traceback
            self.console.print(f"[red]Traceback: {traceback.format_exc()}[/red]")
            import sys
            sys.exit(1)


def main() -> None:
    """Main entry point for the demo application."""
    demo = DemoVSCodeSpoofer()
    demo.run()


if __name__ == "__main__":
    main()
