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


def progress_bar():
    """Rich TUI progress bar"""
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
