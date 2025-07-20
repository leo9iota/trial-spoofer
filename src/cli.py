#!/usr/bin/env python3
"""Command-line interface for vscode-spoofer."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console

from core.config import get_config, reload_config
from core.helpers import check_root, check_system_requirements
from main import Main


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="vscode-spoofer",
        description="VS Code spoofer for Linux - Modify system identifiers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  vscode-spoofer                    # Interactive mode
  vscode-spoofer --check            # Check system requirements only
  vscode-spoofer --config           # Show current configuration
  vscode-spoofer --debug            # Run in debug mode
        """,
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="Check system requirements and exit",
    )

    parser.add_argument(
        "--config",
        action="store_true",
        help="Show current configuration and exit",
    )

    parser.add_argument(
        "--no-confirm",
        action="store_true",
        help="Skip confirmation prompts (use with caution)",
    )

    parser.add_argument(
        "--backup-path",
        type=Path,
        help="Custom backup directory path",
    )

    return parser


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
    enabled_features = config.get_enabled_features()
    if enabled_features:
        for feature in enabled_features:
            console.print(f"  ✓ {feature}")
    else:
        console.print("  [dim]No features enabled[/dim]")


def check_prerequisites() -> bool:
    """Check system prerequisites."""
    console = Console()

    # Check root permissions
    if not check_root():
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


def main(argv: Optional[list[str]] = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()
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
