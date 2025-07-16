import time

from rich.console import Console
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
from rich.text import Text


class StatusSpinnerColumn(ProgressColumn):
    """Custom column that shows spinner or status symbol"""

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
            # Show spinner for active tasks
            return self.spinner.render(task)


def progress_bar_static():
    """Rich TUI progress bar - static demo"""
    progress = Progress(
        StatusSpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
    )

    task1 = progress.add_task("Downloading", total=100, status="✓")
    task2 = progress.add_task("Processing", total=100, status="✗")
    task3 = progress.add_task("Uploading", total=100, status="")

    progress.update(task1, completed=100)
    progress.update(task2, completed=45)
    progress.update(task3, completed=90)

    return Panel(
        progress,
        title="[bold yellow]Rich Progress Bars[/bold yellow]",
        border_style="yellow",
    )


def progress_bar_animated():
    """Rich TUI progress bar - animated demo"""
    console = Console()

    with Progress(
        StatusSpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task1 = progress.add_task("Downloading", total=100, status="")
        task2 = progress.add_task("Processing", total=100, status="")
        task3 = progress.add_task("Uploading", total=100, status="")

        # Track completion status
        task1_completed = False
        task2_failed = False
        task3_completed = False

        # Simulate work with animated progress
        for i in range(120):  # Extended to show completion states
            time.sleep(0.02)  # Small delay to see animation

            # Update task 1 (successful completion)
            task1_progress = min(i + 25, 100)
            if task1_progress >= 100 and not task1_completed:
                progress.update(task1, completed=100, status="✓")
                task1_completed = True
            elif not task1_completed:
                progress.update(task1, completed=task1_progress)

            # Update task 2 (fails at 60%)
            task2_progress = min(i, 100)
            if task2_progress >= 60 and not task2_failed:
                progress.update(task2, completed=60, status="✗")
                task2_failed = True
            elif not task2_failed:
                progress.update(task2, completed=task2_progress)

            # Update task 3 (successful completion, starts later)
            task3_progress = min(i - 10, 100) if i > 10 else 0
            if task3_progress >= 100 and not task3_completed:
                progress.update(task3, completed=100, status="✓")
                task3_completed = True
            elif not task3_completed and task3_progress > 0:
                progress.update(task3, completed=task3_progress)


def demo():
    """Run the progress bar demo"""
    console = Console()

    # Show static version first
    console.print("\n[bold blue]Static Progress Bar Demo:[/bold blue]")
    static_panel = progress_bar_static()
    console.print(static_panel)

    console.print("\n[bold blue]Animated Progress Bar Demo:[/bold blue]")
    console.print("(Press Ctrl+C to stop)")

    try:
        progress_bar_animated()
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]")

    console.print("\n[green]Demo completed![/green]")


if __name__ == "__main__":
    demo()
