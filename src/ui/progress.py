#!/usr/bin/env python3

from __future__ import annotations

import time

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
from rich.spinner import Spinner
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
        self.current_steps = {}  # Track current steps for each feature
        self.panel = None  # Store the panel to avoid recreating it

    def start_task(self, feature_name: str) -> None:
        if feature_name not in self.tasks:
            task_id = self.progress.add_task(
                f"Executing {feature_name}...", total=100, status=""
            )
            self.tasks[feature_name] = task_id
            self.task_status[feature_name] = "running"

        self.progress.update(self.tasks[feature_name], completed=0, status="")

    def update_task_progress(
        self, feature_name: str, progress_percent: int, status_text: str = ""
    ) -> None:
        if feature_name in self.tasks:
            task_id = self.tasks[feature_name]
            self.progress.update(
                task_id, completed=progress_percent, status=status_text
            )

    def execute_steps(self, feature_name: str, steps: list[str]) -> None:
        """Execute steps for a feature with realistic progress updates."""
        if feature_name not in self.tasks:
            return

        self.current_steps[feature_name] = []
        step_progress = 100 // len(steps)

        # Create Rich spinner for current step animation
        current_spinner = Spinner("dots", style="cyan")
        waiting_spinner = Spinner("dots", style="dim")

        for i, _ in enumerate(steps):
            # Update task description to show all steps with spinners
            task_id = self.tasks[feature_name]

            # Simulate realistic progress for this step
            start_progress = i * step_progress
            end_progress = min((i + 1) * step_progress, 100)

            for progress in range(start_progress, end_progress + 1):
                # Build the steps display with appropriate spinners/checkmarks
                steps_display_lines = []

                for j, step_text in enumerate(steps):
                    if j < i:
                        # Completed step - show green checkmark
                        steps_display_lines.append(f"  [green]✓[/green] {step_text}")
                    elif j == i:
                        # Current step - show animated cyan spinner
                        # Use Rich's spinner frame based on progress
                        spinner_frame = current_spinner.render(time.time())
                        steps_display_lines.append(f"  {spinner_frame} {step_text}")
                    else:
                        # Future step - show dim waiting spinner
                        waiting_frame = waiting_spinner.render(time.time())
                        steps_display_lines.append(f"  {waiting_frame} {step_text}")

                steps_display = "\n".join(steps_display_lines)
                description = f"{feature_name}:\n{steps_display}"
                self.progress.update(
                    task_id, description=description, completed=progress
                )
                time.sleep(0.03)  # Realistic delay

            # Brief pause between steps
            time.sleep(0.2)

        # Final update with all steps completed
        final_steps = [f"  [green]✓[/green] {step}" for step in steps]
        final_display = "\n".join(final_steps)
        description = f"{feature_name}:\n{final_display}"
        self.progress.update(task_id, description=description, completed=100)

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
        if self.panel is None:
            self.panel = Panel(
                self.progress,
                title="[bold cyan]Progress[/bold cyan]",
                border_style="cyan",
                padding=(1, 2),
                width=120,  # Wider to accommodate multi-line descriptions
                expand=False,  # Don't expand to full terminal width
            )
        return self.panel
