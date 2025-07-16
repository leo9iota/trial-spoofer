#!/usr/bin/env python3
"""
Feature Input Manager - Collect user input for all VSCode Spoofer features
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text


class FeatureInputManager:
    """Manages input collection for all VSCode Spoofer features."""

    def __init__(self) -> None:
        """Initialize the input manager."""
        self.console = Console()
        self.features = [
            {
                "name": "MAC Address",
                "description": "Spoof network interface MAC",
                "risk_level": "🟢 Low",
                "prompt": "Spoof MAC address of the first active network interface?",
                "selected": False,
            },
            {
                "name": "Machine ID",
                "description": "Regenerate system machine-id",
                "risk_level": "🟢 Low",
                "prompt": "Regenerate the system machine-id?",
                "selected": False,
            },
            {
                "name": "Filesystem UUID",
                "description": "Randomize root filesystem UUID",
                "risk_level": "🟡 Medium",
                "prompt": "Randomize root filesystem UUID? (Requires reboot)",
                "selected": False,
            },
            {
                "name": "Hostname",
                "description": "Set random hostname",
                "risk_level": "🟢 Low",
                "prompt": "Set a random hostname?",
                "selected": False,
            },
            {
                "name": "VS Code Caches",
                "description": "Purge editor caches",
                "risk_level": "🟢 Low",
                "prompt": "Purge VS Code, Cursor, and Augment Code caches?",
                "selected": False,
            },
            {
                "name": "New User",
                "description": "Create sandbox user account",
                "risk_level": "🟢 Low",
                "prompt": "Create a throw-away user 'vscode_sandbox'?",
                "selected": False,
            },
        ]

    def create_header(self) -> Panel:
        """Create the application header."""
        title = Text("🔒 VSCode Spoofer - Feature Selection", style="bold magenta")
        subtitle = Text("Select which operations to perform", style="dim cyan")
        header_text = Text.assemble(title, "\n", subtitle)
        return Panel(
            header_text,
            style="bright_blue",
            padding=(1, 2),
        )

    def create_features_table(self) -> Table:
        """Create a table showing all available features."""
        table = Table(
            title="🛡️ Available Security Features",
            show_header=True,
            header_style="bold magenta"
        )
        table.add_column("Selected", justify="center", style="bold", width=8)
        table.add_column("Feature", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Risk Level", justify="center", width=12)

        for feature in self.features:
            selected_icon = "✅" if feature["selected"] else "❌"
            selected_text = Text(
                selected_icon,
                style="green" if feature["selected"] else "red"
            )

            table.add_row(
                selected_text,
                feature["name"],
                feature["description"],
                feature["risk_level"]
            )

        return table

    def collect_feature_inputs(self) -> dict[str, bool]:
        """Collect input for all features with default 'n'."""
        self.console.print(self.create_header())
        self.console.print()

        # Show initial table
        self.console.print(self.create_features_table())
        self.console.print()

        self.console.print("[bold yellow]Configure each feature:[/bold yellow]")
        self.console.print("[dim]Default is 'n' (no) for all features[/dim]")
        self.console.print()

        # Collect input for each feature
        for feature in self.features:
            # Ask for confirmation with default=False (n)
            response = Confirm.ask(
                f"🤔 {feature['prompt']} [{feature['risk_level']}]",
                default=False
            )
            feature["selected"] = response

            # Show updated status
            status = "✅ Selected" if response else "❌ Skipped"
            style = "green" if response else "red"
            self.console.print(f"   {Text(status, style=style)}")
            self.console.print()

        # Show final selection summary
        self._show_selection_summary()

        # Return results as dictionary
        return {feature["name"]: feature["selected"] for feature in self.features}

    def _show_selection_summary(self) -> None:
        """Show a summary of selected features."""
        self.console.print("[bold yellow]📋 Selection Summary:[/bold yellow]")
        self.console.print()

        # Create summary table
        summary_table = Table(
            title="Selected Operations",
            show_header=True,
            header_style="bold green"
        )
        summary_table.add_column("Feature", style="cyan", no_wrap=True)
        summary_table.add_column("Description", style="white")
        summary_table.add_column("Risk Level", justify="center")

        selected_count = 0
        for feature in self.features:
            if feature["selected"]:
                summary_table.add_row(
                    feature["name"],
                    feature["description"],
                    feature["risk_level"]
                )
                selected_count += 1

        if selected_count == 0:
            summary_table.add_row(
                Text("No features selected", style="dim italic"),
                Text("All operations will be skipped", style="dim italic"),
                Text("—", style="dim")
            )

        self.console.print(summary_table)
        self.console.print()

        # Show count
        if selected_count > 0:
            message = f"[bold green]✅ {selected_count} feature(s) selected[/bold green]"
            self.console.print(message)
        else:
            self.console.print("[yellow]⚠️ No features selected[/yellow]")
        self.console.print()

    def get_selected_features(self) -> list[str]:
        """Get list of selected feature names."""
        return [feature["name"] for feature in self.features if feature["selected"]]

    def confirm_proceed(self) -> bool:
        """Ask for final confirmation to proceed."""
        selected_count = len(self.get_selected_features())

        if selected_count == 0:
            message = "[yellow]❌ No features selected. Nothing to do.[/yellow]"
            self.console.print(message)
            return False

        return Confirm.ask(
            f"🚀 Proceed with {selected_count} selected operation(s)?",
            default=True
        )


def main():
    """Demo the feature input manager."""
    manager = FeatureInputManager()

    # Collect inputs
    selections = manager.collect_feature_inputs()

    # Show results
    print("\n" + "="*50)
    print("FINAL RESULTS:")
    for feature, selected in selections.items():
        status = "SELECTED" if selected else "SKIPPED"
        print(f"  {feature}: {status}")

    # Final confirmation
    if manager.confirm_proceed():
        print("\n✅ User confirmed to proceed with operations")
    else:
        print("\n❌ User cancelled operations")


if __name__ == "__main__":
    main()