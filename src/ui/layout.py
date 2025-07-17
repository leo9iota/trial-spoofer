#!/usr/bin/env python3
"""
UI Layout Manager - Comprehensive layout with input controls on left and tables on right
"""

from typing import Optional
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.columns import Columns
from rich.prompt import Confirm
import time

from .input import FeatureInputManager
from .tables import FeatureTable, identifiers_table, modified_identifiers_table


class VSCodeSpooferUI:
    """Main UI manager with left-right layout: input controls | data tables."""
    
    def __init__(self):
        """Initialize the UI manager."""
        self.console = Console()
        self.input_manager = FeatureInputManager()
        self.feature_table = FeatureTable()
        self.layout = Layout()
        self.modifications: dict[str, str] = {}
        
        # Setup the main layout structure
        self._setup_layout()
    
    def _setup_layout(self) -> None:
        """Setup the main layout structure."""
        # Create main layout with header and body
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body")
        )
        
        # Split body into left (input) and right (tables)
        self.layout["body"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=3)
        )
        
        # Split right side into top and bottom tables
        self.layout["right"].split_column(
            Layout(name="features_table"),
            Layout(name="identifiers_section")
        )
        
        # Split identifiers section into current and modified
        self.layout["identifiers_section"].split_row(
            Layout(name="current_ids"),
            Layout(name="modified_ids")
        )
    
    def _create_header(self) -> Panel:
        """Create the application header."""
        return Panel(
            "[bold blue]🔒 VSCode Spoofer - Interactive Dashboard[/bold blue]\n"
            "[dim]Left: Feature Controls | Right: System Status & Tables[/dim]",
            style="bold blue",
            padding=(0, 2),
        )
    
    def _create_input_panel(self) -> Panel:
        """Create the input controls panel."""
        content = []
        
        # Feature selection status
        selected_count = len(self.feature_table.get_selected_features())
        total_count = len(self.feature_table.features)
        
        content.append(f"[bold yellow]Feature Selection ({selected_count}/{total_count})[/bold yellow]")
        content.append("")
        
        # List all features with selection status
        for feature in self.feature_table.features:
            selected = self.feature_table.selections[feature["name"]]
            icon = "✅" if selected else "⬜"
            risk_color = "yellow" if "Medium" in feature["risk_level"] else "green"
            
            content.append(
                f"{icon} {feature['icon']} [cyan]{feature['name']}[/cyan] "
                f"[{risk_color}]{feature['risk_level']}[/{risk_color}]"
            )
        
        content.append("")
        content.append("[dim]Use interactive mode to modify selections[/dim]")
        
        return Panel(
            "\n".join(content),
            title="🎛️ Input Controls",
            border_style="yellow",
            padding=(1, 2)
        )
    
    def _create_features_panel(self) -> Panel:
        """Create the features table panel."""
        table = self.feature_table.create_info_table()
        return Panel(
            table,
            title="📊 Features Status",
            border_style="blue",
            padding=(0, 1)
        )
    
    def _create_current_ids_panel(self) -> Panel:
        """Create the current identifiers panel."""
        table = identifiers_table()
        return Panel(
            table,
            title="🔍 Current IDs",
            border_style="cyan",
            padding=(0, 1)
        )
    
    def _create_modified_ids_panel(self) -> Panel:
        """Create the modified identifiers panel."""
        if self.modifications:
            table = modified_identifiers_table(self.modifications)
        else:
            # Create empty table with message
            from rich.table import Table
            table = Table(show_header=False, border_style="green")
            table.add_column("Message", justify="center")
            table.add_row("[dim]No modifications yet[/dim]")
        
        return Panel(
            table,
            title="✨ Modified IDs",
            border_style="green",
            padding=(0, 1)
        )
    
    def update_layout(self) -> None:
        """Update all layout components with current data."""
        self.layout["header"].update(self._create_header())
        self.layout["left"].update(self._create_input_panel())
        self.layout["features_table"].update(self._create_features_panel())
        self.layout["current_ids"].update(self._create_current_ids_panel())
        self.layout["modified_ids"].update(self._create_modified_ids_panel())
    
    def show_static_dashboard(self) -> None:
        """Display the static dashboard."""
        self.update_layout()
        self.console.print(self.layout)
    
    def show_live_dashboard(self, duration: float = 10.0) -> None:
        """Display the live updating dashboard."""
        with Live(self.layout, console=self.console, refresh_per_second=2) as live:
            start_time = time.time()
            
            while time.time() - start_time < duration:
                self.update_layout()
                time.sleep(0.5)
    
    def interactive_feature_selection(self) -> dict[str, bool]:
        """Run interactive feature selection and update the UI."""
        self.console.clear()
        
        # Show initial dashboard
        self.show_static_dashboard()
        self.console.print()
        
        # Run feature selection
        self.console.print("[bold yellow]🎯 Interactive Feature Selection[/bold yellow]")
        self.console.print("[dim]Configure which features to enable...[/dim]")
        self.console.print()
        
        selections = self.input_manager.collect_feature_inputs()
        
        # Update feature table with selections
        self.feature_table.set_selections(selections)
        
        # Show updated dashboard
        self.console.clear()
        self.show_static_dashboard()
        
        return selections
    
    def simulate_operations(self, selected_features: list[str]) -> dict[str, str]:
        """Simulate running operations and update status in real-time."""
        import random
        import uuid
        
        modifications = {}
        
        self.console.print()
        self.console.print("[bold green]🚀 Executing Selected Operations[/bold green]")
        self.console.print()
        
        with Live(self.layout, console=self.console, refresh_per_second=4) as live:
            for feature in selected_features:
                # Update status to running
                self.feature_table.update_feature_status(feature, "Running")
                self.update_layout()
                
                # Simulate work
                time.sleep(2)
                
                # Generate mock modifications
                if feature == "MAC Address":
                    modifications[feature] = "02:42:ac:11:00:02"
                elif feature == "Machine ID":
                    modifications[feature] = str(uuid.uuid4()).replace('-', '')
                elif feature == "Filesystem UUID":
                    modifications[feature] = str(uuid.uuid4())
                elif feature == "Hostname":
                    modifications[feature] = f"vscode-dev-{random.randint(1000, 9999)}"
                elif feature == "VS Code Caches":
                    modifications[feature] = "Cleared 245 MB"
                elif feature == "New User":
                    modifications[feature] = f"user-{random.randint(100, 999)}"
                
                # Update status to complete
                success = random.choice([True] * 9 + [False])  # 90% success rate
                status = "Complete" if success else "Failed"
                self.feature_table.update_feature_status(feature, status)
                
                # Update modifications
                if success:
                    self.modifications.update({feature: modifications[feature]})
                
                self.update_layout()
                time.sleep(1)
        
        return self.modifications
    
    def show_final_summary(self) -> None:
        """Show final summary with all results."""
        self.console.print()
        self.console.print("[bold green]✅ Operations Complete![/bold green]")
        self.console.print()
        
        # Show final dashboard
        self.show_static_dashboard()
        
        # Show summary statistics
        selected_count = len(self.feature_table.get_selected_features())
        completed_count = len([f for f in self.feature_table.features if f["status"] == "Complete"])
        failed_count = len([f for f in self.feature_table.features if f["status"] == "Failed"])
        
        summary_panel = Panel(
            f"[bold]Summary:[/bold]\n"
            f"• Selected: {selected_count} features\n"
            f"• Completed: [green]{completed_count}[/green]\n"
            f"• Failed: [red]{failed_count}[/red]\n"
            f"• Modified: [cyan]{len(self.modifications)}[/cyan] identifiers",
            title="📈 Execution Summary",
            style="bold",
            padding=(1, 2)
        )
        
        self.console.print()
        self.console.print(summary_panel)
    
    def run_full_workflow(self) -> None:
        """Run the complete workflow: selection -> execution -> summary."""
        try:
            # Step 1: Interactive feature selection
            selections = self.interactive_feature_selection()
            
            # Step 2: Confirm before proceeding
            if not self.input_manager.confirm_proceed():
                self.console.print("\n[yellow]❌ Operations cancelled by user[/yellow]")
                return
            
            # Step 3: Execute selected operations
            selected_features = self.feature_table.get_selected_features()
            if selected_features:
                self.simulate_operations(selected_features)
            
            # Step 4: Show final summary
            self.show_final_summary()
            
        except KeyboardInterrupt:
            self.console.print("\n\n[red]❌ Application interrupted by user[/red]")
        except Exception as e:
            self.console.print(f"\n[red]❌ Error: {e}[/red]")


def create_demo_layout() -> VSCodeSpooferUI:
    """Create a demo UI instance with some pre-selected features."""
    ui = VSCodeSpooferUI()
    
    # Pre-select some features for demo
    ui.feature_table.select_feature("MAC Address")
    ui.feature_table.select_feature("Machine ID")
    ui.feature_table.select_feature("Hostname")
    
    return ui
