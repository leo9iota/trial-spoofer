import argparse
from pathlib import Path

ARGS_DESCRIPTION = """
Examples:
    vscode-spoofer                    # Interactive mode
    vscode-spoofer --check            # Check system requirements only
    vscode-spoofer --config           # Show current configuration
    vscode-spoofer --debug            # Run in debug mode
"""


def parse_args() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="vscode-spoofer",
        description="VS Code spoofer for Linux - Modify system identifiers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=ARGS_DESCRIPTION,
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
