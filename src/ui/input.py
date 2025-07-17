#!/usr/bin/env python3
"""
Feature Input Manager - Handles user input for all VSCode Spoofer features
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table


class FeatureInputManager:
    """Manages user input for all spoofing features with Rich TUI."""

    def __init__(self):
        """Initialize the feature input manager."""
        self.console = Console()
        self.selections: dict[str, bool] = {}

        # Define all available features with their properties
        self.features = [
            {
                "name": "MAC Address",
                "description": "Spoof network interface MAC address",
                "prompt": "Spoof MAC address?",
                "risk_level": "🟢 Low",
                "icon": "🌐",
                "default": False,
            },
            {
                "name": "Machine ID",
                "description": "Regenerate system machine-id",
                "prompt": "Regenerate machine ID?",
                "risk_level": "🟢 Low",
                "icon": "🔧",
                "default": False,
            },
            {
                "name": "Filesystem UUID",
                "description": "Randomize root filesystem UUID",
                "prompt": "Change filesystem UUID?",
                "risk_level": "🟡 Medium",
                "icon": "💾",
                "default": False,
            },
            {
                "name": "Hostname",
                "description": "Set random hostname",
                "prompt": "Change hostname?",
                "risk_level": "🟢 Low",
                "icon": "🏷️",
                "default": False,
            },
            {
                "name": "VS Code Caches",
                "description": "Purge editor caches and extensions",
                "prompt": "Clear VS Code caches?",
                "risk_level": "🟢 Low",
                "icon": "🗑️",
                "default": False,
            },
            {
                "name": "New User",
                "description": "Create sandbox user account",
                "prompt": "Create new user?",
                "risk_level": "🟢 Low",
                "icon": "👤",
                "default": False,
            },
        ]

        # Initialize selections with defaults (all False)
        for feature in self.features:
            self.selections[feature["name"]] = feature["default"]

    def show_header(self) -> None:
        """Display the application header."""
        header = Panel(
            "[bold blue]🔒 VSCode Spoofer - Feature Selection[/bold blue]\n"
            "[dim]Select which features to enable (all default to 'n')[/dim]",
            style="bold blue",
            padding=(1, 2),
        )
        self.console.print(header)
        self.console.print()

    def show_features_overview(self) -> None:
        """Display an overview table of all available features."""
        table = Table(
            title="Available Features", show_header=True, header_style="bold magenta"
        )
        table.add_column("Feature", style="cyan", width=20)
        table.add_column("Description", style="white", width=35)
        table.add_column("Risk", justify="center", width=12)
        table.add_column("Default", justify="center", width=10)

        for feature in self.features:
            default_text = "No" if not feature["default"] else "Yes"
            table.add_row(
                f"{feature['icon']} {feature['name']}",
                feature["description"],
                feature["risk_level"],
                f"[dim]{default_text}[/dim]",
            )

        self.console.print(table)
        self.console.print()

    def collect_feature_inputs(self) -> dict[str, bool]:
        """Collect user input for all features."""
        self.show_header()
        self.show_features_overview()

        self.console.print("[bold yellow]Feature Selection[/bold yellow]")
        self.console.print(
            "[dim]Press Enter to accept default (n) or type 'y' to enable[/dim]"
        )
        self.console.print()

        for feature in self.features:
            # Create a styled prompt
            prompt_text = f"{feature['icon']} {feature['prompt']}"

            # Show risk level for medium/high risk features
            if "Medium" in feature["risk_level"] or "High" in feature["risk_level"]:
                prompt_text += f" [{feature['risk_level']}]"

            # Get user input with default 'n'
            response = Confirm.ask(prompt_text, default=feature["default"])
            self.selections[feature["name"]] = response

            # Show immediate feedback
            status = "✅ Selected" if response else "❌ Skipped"
            self.console.print(f"   {status}")
            self.console.print()

        return self.selections

    def get_selected_features(self) -> list[str]:
        """Get list of selected feature names."""
        return [name for name, selected in self.selections.items() if selected]

    def get_selections_dict(self) -> dict[str, bool]:
        """Get the complete selections dictionary."""
        return self.selections.copy()

    def show_selection_summary(self) -> None:
        """Display a summary of selected features."""
        selected_features = self.get_selected_features()

        if not selected_features:
            panel = Panel(
                "[yellow]⚠️ No features selected[/yellow]\n"
                "[dim]All operations will be skipped[/dim]",
                title="Selection Summary",
                style="yellow",
            )
        else:
            features_text = "\n".join(
                [f"• [green]{feature}[/green]" for feature in selected_features]
            )
            panel = Panel(
                f"[bold green]✅ {len(selected_features)} feature(s) selected:[/bold green]\n\n{features_text}",
                title="Selection Summary",
                style="green",
            )

        self.console.print(panel)
        self.console.print()

    def confirm_proceed(self) -> bool:
        """Show summary and get final confirmation to proceed."""
        self.show_selection_summary()

        selected_count = len(self.get_selected_features())

        if selected_count == 0:
            return Confirm.ask(
                "[yellow]No features selected. Continue anyway?[/yellow]", default=False
            )
        else:
            return Confirm.ask(
                f"[bold]Proceed with {selected_count} selected operation(s)?[/bold]",
                default=True,
            )

    def get_feature_by_name(self, name: str) -> dict | None:
        """Get feature definition by name."""
        for feature in self.features:
            if feature["name"] == name:
                return feature
        return None

    def set_feature_selection(self, feature_name: str, selected: bool) -> bool:
        """Set selection state for a specific feature."""
        if feature_name in self.selections:
            self.selections[feature_name] = selected
            return True
        return False

    def toggle_feature_selection(self, feature_name: str) -> bool:
        """Toggle selection state for a specific feature."""
        if feature_name in self.selections:
            self.selections[feature_name] = not self.selections[feature_name]
            return True
        return False

    def select_all_features(self) -> None:
        """Select all features."""
        for feature_name in self.selections:
            self.selections[feature_name] = True

    def deselect_all_features(self) -> None:
        """Deselect all features."""
        for feature_name in self.selections:
            self.selections[feature_name] = False
