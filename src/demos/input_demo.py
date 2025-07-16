#!/usr/bin/env python3
"""
Rich Input Examples - Practical patterns for VSCode Spoofer
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table


def main():
    """Show practical Rich input examples."""
    console = Console()

    # Header
    header = Panel(
        "🎯 Rich Input - Practical Examples",
        style="bold blue",
        padding=(1, 2),
    )
    console.print(header)
    console.print()

    # 1. Basic text input with default
    console.print("[bold yellow]1. Basic Text Input[/bold yellow]")
    hostname = Prompt.ask("Enter new hostname", default="vscode-dev")
    console.print(f"Hostname: [green]{hostname}[/green]")
    console.print()

    # 2. Password input (hidden)
    console.print("[bold yellow]2. Password Input[/bold yellow]")
    password = Prompt.ask("Enter user password", password=True)
    console.print(f"Password set ([dim]{len(password)} characters[/dim])")
    console.print()

    # 3. Integer input with validation
    console.print("[bold yellow]3. Integer Input[/bold yellow]")
    port = IntPrompt.ask("Enter port number", default=8080)
    console.print(f"Port: [cyan]{port}[/cyan]")
    console.print()

    # 4. Confirmation prompts
    console.print("[bold yellow]4. Confirmation Prompts[/bold yellow]")
    spoof_mac = Confirm.ask("Spoof MAC address?", default=True)
    spoof_uuid = Confirm.ask("Change filesystem UUID?", default=False)
    create_user = Confirm.ask("Create new user?", default=False)

    # Show selections
    table = Table(title="Selected Operations")
    table.add_column("Operation", style="cyan")
    table.add_column("Selected", justify="center")

    table.add_row("MAC Address", "✅" if spoof_mac else "❌")
    table.add_row("Filesystem UUID", "✅" if spoof_uuid else "❌")
    table.add_row("Create User", "✅" if create_user else "❌")

    console.print(table)
    console.print()

    # 5. Choice-based input
    console.print("[bold yellow]5. Choice-Based Input[/bold yellow]")
    interface = Prompt.ask(
        "Select network interface",
        choices=["eth0", "wlan0", "auto"],
        default="auto",
    )
    console.print(f"Interface: [green]{interface}[/green]")
    console.print()

    # 6. Manual validation loop
    console.print("[bold yellow]6. Input Validation[/bold yellow]")
    while True:
        username = Prompt.ask("Enter username (3-20 chars)")
        if 3 <= len(username) <= 20 and username.isalnum():
            console.print(f"Username: [green]{username}[/green]")
            break
        else:
            console.print("[red]Username must be 3-20 alphanumeric characters[/red]")

    console.print()

    # Final confirmation
    console.print("[bold yellow]7. Final Confirmation[/bold yellow]")
    proceed = Confirm.ask(
        "[bold red]⚠️  Proceed with system modifications?[/bold red]",
        default=False,
    )

    if proceed:
        console.print("[bold green]✅ Operations would proceed[/bold green]")
    else:
        console.print("[yellow]❌ Operations cancelled[/yellow]")


if __name__ == "__main__":
    main()
