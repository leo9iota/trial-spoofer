#!/usr/bin/env python3
"""
Progress UI components for indicating state of operations.
"""

from __future__ import annotations

from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    ProgressColumn,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from rich.text import Text


class ProgressSpinner(ProgressColumn):
    def __init__(self):
        super().__init__()
        self.spinner = SpinnerColumn()

    def render(self, task):
        status = task.fields.get("status", "")
        if status == "✓":
            return Text("✓", style="bold green")
        elif status == "✗":
            return Text("✗", style="bold red")
        elif status:
            return Text(status, style="bold")
        else:
            return self.spinner.render(task)


class ProgressBar:
    def __init__(self):
        self.progress = Progress(
            ProgressSpinner(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
        )
        self.tasks = {}
        self.task_status = {}

    def start_task(self, feature_name: str) -> None:
        if feature_name not in self.tasks:
            task_id = self.progress.add_task(
                f"Executing {feature_name}...", total=100, status=""
            )
            self.tasks[feature_name] = task_id
            self.task_status[feature_name] = "running"

        self.progress.update(self.tasks[feature_name], completed=0, status="")

    def complete_task(self, feature_name: str, success: bool) -> None:
        if feature_name in self.tasks:
            task_id = self.tasks[feature_name]
            if success:
                self.progress.update(task_id, completed=100, status="✓")
                self.task_status[feature_name] = "success"
            else:
                self.progress.update(task_id, completed=100, status="✗")
                self.task_status[feature_name] = "failed"

    def create_progress_display(self) -> Panel:
        return Panel(
            self.progress,
            title="[bold cyan]Execution Progress[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )

    def get_summary_table(self) -> Table:
        table = Table(
            title="Execution Summary",
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
        )

        table.add_column("Feature", style="white", width=20)
        table.add_column("Status", justify="center", width=12)
        table.add_column("Result", style="white", width=30)

        for feature_name, status in self.task_status.items():
            if status == "success":
                status_icon = "[bold green]✓ Success[/bold green]"
                result_text = "Operation completed successfully"
            elif status == "failed":
                status_icon = "[bold red]✗ Failed[/bold red]"
                result_text = "Operation failed - check logs"
            else:
                status_icon = "[yellow]Running[/yellow]"
                result_text = "Operation in progress"

            table.add_row(feature_name, status_icon, result_text)

        return table
