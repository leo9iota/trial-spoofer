#!/usr/bin/env python3
"""
Enhanced Table Demo - Show the new feature selection table
"""

import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

# Add src to path so we can import from ui
sys.path.append(str(Path(__file__).parent.parent))

from ui.table import FeatureTable


def main():
    """Demonstrate the enhanced feature table with selection."""
    console = Console()

    # Header
    header = Panel(
        "🛡️ Enhanced Feature Table Demo",
        style="bold blue",
        padding=(1, 2),
    )
    console.print(header)
    console.print()

    # Create feature table instance
    feature_table = FeatureTable()

    # Show initial table (no selections)
    console.print("[bold yellow]1. Initial Feature Table (No Selections)[/bold yellow]")
    console.print(feature_table.create_info_table())
    console.print()

    # Interactive selection demo
    console.print("[bold yellow]2. Interactive Feature Selection[/bold yellow]")
    console.print("Let's select some features interactively...")
    console.print()

    # Select some features based on user input
    if Confirm.ask("Select MAC Address spoofing?", default=True):
        feature_table.select_feature("MAC Address")

    if Confirm.ask("Select Machine ID regeneration?", default=True):
        feature_table.select_feature("Machine ID")

    if Confirm.ask("Select Filesystem UUID randomization?", default=False):
        feature_table.select_feature("Filesystem UUID")

    if Confirm.ask("Select Hostname change?", default=True):
        feature_table.select_feature("Hostname")

    if Confirm.ask("Select VS Code cache cleaning?", default=True):
        feature_table.select_feature("VS Code Caches")

    if Confirm.ask("Create new user?", default=False):
        feature_table.select_feature("New User")

    console.print()

    # Show updated table with selections
    console.print("[bold yellow]3. Updated Table with Selections[/bold yellow]")
    console.print(feature_table.create_info_table())
    console.print()

    # Show selection summary
    console.print("[bold yellow]4. Selection Summary[/bold yellow]")
    console.print(feature_table.create_selection_summary_table())
    console.print()

    # Show selected features list
    selected = feature_table.get_selected_features()
    console.print(f"[bold green]Selected Features:[/bold green] {', '.join(selected)}")
    console.print()

    # Demo toggle functionality
    console.print("[bold yellow]5. Toggle Feature Demo[/bold yellow]")
    if selected:
        feature_to_toggle = selected[0]
        console.print(f"Toggling '{feature_to_toggle}'...")
        feature_table.toggle_feature(feature_to_toggle)
        console.print("After toggle:")
        console.print(feature_table.create_info_table())
        console.print()

    # Demo select/deselect all
    console.print("[bold yellow]6. Select/Deselect All Demo[/bold yellow]")

    action = Prompt.ask(
        "Choose action",
        choices=["select_all", "deselect_all", "skip"],
        default="skip"
    )

    if action == "select_all":
        feature_table.select_all()
        console.print("All features selected:")
    elif action == "deselect_all":
        feature_table.deselect_all()
        console.print("All features deselected:")
    else:
        console.print("No changes made:")

    console.print(feature_table.create_info_table())
    console.print()

    # Final summary
    final_selected = feature_table.get_selected_features()
    console.print("[bold green]✅ Demo completed![/bold green]")
    console.print(f"Final selection: {len(final_selected)} features selected")

    if final_selected:
        console.print("Selected features:")
        for feature in final_selected:
            console.print(f"  • [cyan]{feature}[/cyan]")


if __name__ == "__main__":
    main()
