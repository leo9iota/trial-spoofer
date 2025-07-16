import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


def progress_bar(self):
    """Rich TUI progress bar"""
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    )

    task1 = progress.add_task("Downloading...", total=100)
    task2 = progress.add_task("Processing...", total=100)
    task3 = progress.add_task("Uploading...", total=100)

    progress.update(task1, completed=75)
    progress.update(task2, completed=45)
    progress.update(task3, completed=90)

    return Panel(
        progress,
        title="[bold yellow]Rich Progress Bars[/bold yellow]",
        border_style="yellow",
    )
