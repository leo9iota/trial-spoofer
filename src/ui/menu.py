def draw_main_menu(self) -> str:
    self.console.print("[bold cyan]Options[/bold cyan]")
    self.console.print("1. List identifiers")
    self.console.print("2. Spoof identifiers")
    self.console.print("3. Exit")

    while True:
        choice = input("\nSelect option (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        self.console.print("[red]Invalid choice. Please enter 1, 2, or 3.[/red]")
