#!/usr/bin/env python3
"""Command-line interface for vscode-spoofer."""

import sys

from rich.console import Console

from .core.config import get_config, reload_config
from .main import Main
from .utils import check_root, check_system_requirements


def show_config() -> None:
    """Display current configuration."""
    console = Console()
    config = get_config()

    console.print("\n[bold cyan]Current Configuration:[/bold cyan]")
    console.print(f"Debug: {config.debug}")
    console.print(f"Log Level: {config.log_level}")
    console.print(f"Default Hostname: {config.default_hostname}")
    console.print(f"Default Username: {config.default_username}")
    console.print(f"Require Confirmation: {config.require_confirmation}")
    console.print(f"Backup Configs: {config.backup_configs}")
    console.print(f"Backup Path: {config.backup_path}")

    console.print("\n[bold cyan]Enabled Features:[/bold cyan]")
    enabled_features = config.get_enabled_options()
    if enabled_features:
        for feature in enabled_features:
            console.print(f"  ✓ {feature}")
    else:
        console.print("  [dim]No features enabled[/dim]")


def check_prerequisites() -> bool:
    """Check system prerequisites."""
    console = Console()

    # Check root permissions
    try:
        check_root()  # This function exits if not root, so if we get here, we're root
    except SystemExit:
        console.print(
            "[bold red]Error:[/bold red] This application requires root privileges."
        )
        console.print("Please run with sudo or as root user.")
        return False

    # Check system requirements
    if not check_system_requirements():
        console.print("[bold red]Error:[/bold red] System requirements not met.")
        console.print("Please ensure all required system tools are installed.")
        return False

    return True


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point."""
    parser = parse_args()
    args = parser.parse_args(argv)

    console = Console()

    # Handle debug mode
    if args.debug:
        import os

        os.environ["DEBUG"] = "true"
        os.environ["LOG_LEVEL"] = "DEBUG"
        reload_config()
        console.print("[dim]Debug mode enabled[/dim]")

    # Handle configuration display
    if args.config:
        show_config()
        return 0

    # Handle system check only
    if args.check:
        console.print("Checking system requirements...")
        if check_prerequisites():
            console.print("[bold green]✓[/bold green] All system requirements met.")
            return 0
        else:
            return 1

    # Update config based on CLI args
    config = get_config()
    if args.no_confirm:
        import os

        os.environ["REQUIRE_CONFIRMATION"] = "false"
        reload_config()

    if args.backup_path:
        import os

        os.environ["BACKUP_PATH"] = str(args.backup_path)
        reload_config()

    # Check prerequisites before running main application
    if not check_prerequisites():
        return 1

    # Run main application
    try:
        app = Main()
        app.run()
        return 0
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
        return 130
    except Exception as e:
        if config.debug:
            console.print_exception()
        else:
            console.print(f"[bold red]Error:[/bold red] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
