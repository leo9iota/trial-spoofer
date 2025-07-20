from rich.console import Console

console = Console()

def draw_main_menu() -> str:
    console.print("[bold cyan]Options[/bold cyan]")
    console.print("1. List identifiers")
    console.print("2. Spoof identifiers")
    console.print("3. Exit")

    while True:
        choice = input("\nSelect option (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        console.print("[red]Invalid choice. Please enter 1, 2, or 3.[/red]")
