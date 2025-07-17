#!/usr/bin/env python3
"""
Demo script to showcase VS Code Spoofer UI components without requiring root privileges.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from ui.tables import FeatureTable, identifiers_table
from ui.input import UserInput
from ui.progress import ProgressBar


def demo_header():
    """Demo the application header."""
    console = Console()
    
    header_text = Text()
    header_text.append("🛡️ VS Code Spoofer v0.1.0\n", style="bold cyan")
    header_text.append("Linux system identifier spoofing utility\n", style="white")
    header_text.append("⚠️  Requires root privileges", style="bold yellow")
    
    header = Panel(
        header_text,
        title="[bold blue]VS Code Spoofer[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    )
    
    console.print(header)
    return header


def demo_tables():
    """Demo the feature and identifier tables."""
    console = Console()
    
    console.print("\n[bold cyan]Feature Table Demo:[/bold cyan]")
    feature_table = FeatureTable()
    console.print(feature_table.create_info_table())
    
    console.print("\n[bold cyan]System Identifiers Demo:[/bold cyan]")
    console.print(identifiers_table())


def demo_progress():
    """Demo the progress bar functionality."""
    console = Console()
    
    console.print("\n[bold cyan]Progress Bar Demo:[/bold cyan]")
    progress = ProgressBar()
    
    # Create a simple progress display
    import time
    from rich.live import Live
    
    with Live(progress.create_progress_display(), refresh_per_second=10) as live:
        # Simulate some tasks
        tasks = ["MAC Address", "Machine ID", "Hostname"]
        
        for task in tasks:
            progress.start_task(task)
            live.update(progress.create_progress_display())
            time.sleep(1)  # Simulate work
            
            progress.complete_task(task, True)
            live.update(progress.create_progress_display())
            time.sleep(0.5)


def demo_input_simulation():
    """Demo the input handling (simulation only)."""
    console = Console()
    
    console.print("\n[bold cyan]Input Handling Demo:[/bold cyan]")
    
    # Show what the feature selection would look like
    user_input = UserInput()
    
    # Create a mock feature list
    mock_features = [
        {
            "name": "MAC Address",
            "description": "Spoof network interface MAC address",
            "risk_level": "🟢 Low",
            "icon": "🌐"
        },
        {
            "name": "Machine ID", 
            "description": "Regenerate system machine-id",
            "risk_level": "🟢 Low",
            "icon": "🔧"
        }
    ]
    
    # Show the selection table (without actually prompting)
    console.print("This is what the feature selection interface looks like:")
    console.print("(In actual use, you would select features interactively)")
    
    from rich.table import Table
    selection_table = Table(show_header=True, header_style="bold magenta")
    selection_table.add_column("No.", justify="center", width=4)
    selection_table.add_column("Feature", style="cyan", width=18)
    selection_table.add_column("Description", style="white", width=35)
    selection_table.add_column("Risk", justify="center", width=12)
    
    for i, feature in enumerate(mock_features, 1):
        selection_table.add_row(
            str(i),
            f"{feature['icon']} {feature['name']}",
            feature['description'],
            feature['risk_level']
        )
    
    console.print(selection_table)


def main():
    """Run the demo."""
    console = Console()
    
    console.print("[bold green]🎯 VS Code Spoofer Demo[/bold green]")
    console.print("[yellow]This demo showcases the UI components without requiring root privileges.[/yellow]")
    console.print()
    
    # Demo each component
    demo_header()
    demo_tables()
    demo_input_simulation()
    demo_progress()
    
    console.print("\n[bold green]✅ Demo completed![/bold green]")
    console.print("[yellow]To run the actual application, use: sudo uv run python src/main.py[/yellow]")


if __name__ == "__main__":
    main()
