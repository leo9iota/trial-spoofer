#!/usr/bin/env python3
"""
Table UI Components - Rich tables for VSCode Spoofer features and system identifiers
"""

from rich.console import Console
from rich.table import Table


class FeatureTable:
    """Manages feature selection and display with Rich tables."""

    def __init__(self):
        """Initialize the feature table manager."""
        self.console = Console()
        self.selections: dict[str, bool] = {}

        # Define all available features with their properties
        self.features = [
            {
                "name": "MAC Address",
                "description": "Spoof network interface MAC address",
                "risk_level": "[green]Low[/green]",
                "icon": "",
                "status": "Ready",
            },
            {
                "name": "Machine ID",
                "description": "Regenerate system machine-id",
                "risk_level": "[green]Low[/green]",
                "icon": "",
                "status": "Ready",
            },
            {
                "name": "Filesystem UUID",
                "description": "Randomize root filesystem UUID",
                "risk_level": "[yellow]Medium[/yellow]",
                "icon": "",
                "status": "Ready",
            },
            {
                "name": "Hostname",
                "description": "Set random hostname",
                "risk_level": "[green]Low[/green]",
                "icon": "",
                "status": "Ready",
            },
            {
                "name": "VS Code Caches",
                "description": "Purge editor caches and extensions",
                "risk_level": "[green]Low[/green]",
                "icon": "",
                "status": "Ready",
            },
            {
                "name": "New User",
                "description": "Create sandbox user account",
                "risk_level": "[green]Low[/green]",
                "icon": "",
                "status": "Ready",
            },
            {
                "name": "System Info",
                "description": "Display comprehensive system information",
                "risk_level": "[green]Low[/green]",
                "icon": "",
                "status": "Ready",
            },
        ]

        # Initialize selections (all False by default)
        for feature in self.features:
            self.selections[feature["name"]] = False

    def create_info_table(self) -> Table:
        """Create the main features information table."""
        table = Table(
            title="VSCode Spoofer Features",
            show_header=True,
            header_style="bold magenta",
            border_style="blue",
        )

        table.add_column("Selected", justify="center", width=8, style="bold")
        table.add_column("Feature", style="cyan", justify="left")
        table.add_column("Description", style="white", justify="left")
        table.add_column("Risk", style="white", justify="left")

        for feature in self.features:
            # Selection indicator
            if self.selections[feature["name"]]:
                selected_icon = "[[bold green]✓[/bold green]]"
            else:
                selected_icon = "[[bold red]✗[/bold red]]"

            table.add_row(
                selected_icon,
                feature['name'],
                feature["description"],
                feature["risk_level"],
            )

        return table

    def create_selection_summary_table(self) -> Table:
        """Create a summary table of selected features only."""
        selected_features = self.get_selected_features()

        if not selected_features:
            # Create empty table with message
            table = Table(
                title="📋 Selected Features", show_header=False, border_style="yellow"
            )
            table.add_column("Message", justify="center")
            table.add_row("[yellow]No features selected[/yellow]")
            return table

        table = Table(
            title="📋 Selected Features",
            show_header=True,
            header_style="bold green",
            border_style="green",
        )

        table.add_column("Feature", style="cyan", justify="left")
        table.add_column("Description", style="white", justify="left")
        table.add_column("Risk", style="white", justify="left")

        for feature_name in selected_features:
            feature = self.get_feature_by_name(feature_name)
            if feature:
                table.add_row(
                    f"{feature['icon']} {feature['name']}",
                    feature["description"],
                    feature["risk_level"],
                )

        return table

    def select_feature(self, feature_name: str) -> bool:
        """Select a specific feature."""
        if feature_name in self.selections:
            self.selections[feature_name] = True
            return True
        return False

    def deselect_feature(self, feature_name: str) -> bool:
        """Deselect a specific feature."""
        if feature_name in self.selections:
            self.selections[feature_name] = False
            return True
        return False

    def toggle_feature(self, feature_name: str) -> bool:
        """Toggle selection state of a feature."""
        if feature_name in self.selections:
            self.selections[feature_name] = not self.selections[feature_name]
            return True
        return False

    def select_all(self) -> None:
        """Select all features."""
        for feature_name in self.selections:
            self.selections[feature_name] = True

    def deselect_all(self) -> None:
        """Deselect all features."""
        for feature_name in self.selections:
            self.selections[feature_name] = False

    def get_selected_features(self) -> list[str]:
        """Get list of selected feature names."""
        return [name for name, selected in self.selections.items() if selected]

    def get_feature_by_name(self, name: str) -> dict | None:
        """Get feature definition by name."""
        for feature in self.features:
            if feature["name"] == name:
                return feature
        return None

    def update_feature_status(self, feature_name: str, status: str) -> bool:
        """Update the status of a specific feature."""
        for feature in self.features:
            if feature["name"] == feature_name:
                feature["status"] = status
                return True
        return False

    def get_selections_dict(self) -> dict[str, bool]:
        """Get the complete selections dictionary."""
        return self.selections.copy()

    def set_selections(self, selections: dict[str, bool]) -> None:
        """Set the selections from a dictionary."""
        for feature_name, selected in selections.items():
            if feature_name in self.selections:
                self.selections[feature_name] = selected


def identifiers_table() -> Table:
    """Create a table showing current system identifiers."""
    table = Table(
        title="Current System Identifiers",
        show_header=True,
        header_style="bold cyan",
        border_style="cyan",
    )

    table.add_column("Identifier", style="yellow", width=20)
    table.add_column("Current Value", style="white", width=40)

    # Get current system identifiers
    identifiers = _get_current_identifiers()

    for identifier, value in identifiers.items():
        table.add_row(identifier, value)

    return table


def modified_identifiers_table(modifications: dict[str, str]) -> Table:
    """Create a table showing modified system identifiers."""
    table = Table(
        title="Modified System Identifiers",
        show_header=True,
        header_style="bold green",
        border_style="green",
    )

    table.add_column("Identifier", style="yellow", width=20)
    table.add_column("Old Value", style="dim white", width=18)
    table.add_column("New Value", style="bold green", width=18)
    table.add_column("Status", justify="center", width=12)

    for identifier, new_value in modifications.items():
        # Get current/old value
        current_identifiers = _get_current_identifiers()
        old_value = current_identifiers.get(identifier, "Unknown")

        # Truncate long values for display
        old_display = old_value[:15] + "..." if len(old_value) > 18 else old_value
        new_display = new_value[:15] + "..." if len(new_value) > 18 else new_value

        status_text = "[bold green][~] Modified[/bold green]"
        table.add_row(identifier, old_display, new_display, status_text)

    return table


def _get_current_identifiers() -> dict[str, str]:
    """Get current system identifiers."""
    identifiers = {}

    try:
        # MAC Address (first active interface)
        import subprocess

        result = subprocess.run(
            ["ip", "link", "show"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.split("\n")
            for line in lines:
                if "link/ether" in line and "state UP" in lines[lines.index(line) - 1]:
                    mac = line.split("link/ether")[1].split()[0]
                    identifiers["MAC Address"] = mac
                    break
            if "MAC Address" not in identifiers:
                identifiers["MAC Address"] = "Not found"
        else:
            identifiers["MAC Address"] = "Not found"
    except Exception:
        identifiers["MAC Address"] = "Not found"

    try:
        # Machine ID
        with open("/etc/machine-id") as f:
            identifiers["Machine ID"] = f.read().strip()
    except Exception:
        identifiers["Machine ID"] = "Not found"

    try:
        # Filesystem UUID (root partition)
        result = subprocess.run(
            ["findmnt", "-n", "-o", "UUID", "/"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            identifiers["Filesystem UUID"] = result.stdout.strip()
        else:
            identifiers["Filesystem UUID"] = "Not found"
    except Exception:
        identifiers["Filesystem UUID"] = "Not found"

    try:
        # Hostname
        with open("/etc/hostname") as f:
            identifiers["Hostname"] = f.read().strip()
    except Exception:
        try:
            result = subprocess.run(
                ["hostname"], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                identifiers["Hostname"] = result.stdout.strip()
            else:
                identifiers["Hostname"] = "Not found"
        except Exception:
            identifiers["Hostname"] = "Not found"

    return identifiers
