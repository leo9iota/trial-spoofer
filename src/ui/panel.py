def status_panel(self, results: dict[str, bool]) -> Panel:
        """Create a status panel showing operation results."""
        table: Table = Table(show_header=False, box=None)
        table.add_column("Operation", style="cyan")
        table.add_column("Status", justify="center")

        for operation, success in results.items():
            status: str = "✅ Success" if success else "❌ Failed"
            style: str = "green" if success else "red"
            table.add_row(operation, Text(status, style=style))

        return Panel(table, title="🔍 Operation Results", style="bright_green")

    def error_panel(self, message: str, title: str = "Error") -> Panel:
        """Create an error panel with the given message."""
        return Panel(
            message,
            title=title,
            style="red",
        )

    def cancel_panel(
        self, message: str = "Operation cancelled by user."
    ) -> Panel:
        """Create a cancellation panel."""
        return Panel(
            message,
            title="Cancelled",
            style="yellow",
        )

    def success_panel(
        self, message: str, title: str = "✅ Success"
    ) -> Panel:
        """Create a success panel."""
        return Panel(
            message,
            title=title,
            style="bright_green",
        )

    def warning_panel(
        self, message: str, title: str = "⚠️ Partial Success"
    ) -> Panel:
        """Create a warning panel."""
        return Panel(
            message,
            title=title,
            style="yellow",
        )