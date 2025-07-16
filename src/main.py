#!/usr/bin/env python3
"""
Linux VS Code Spoofer - Beautiful Rich TUI

Script to wipe every host-side identifier that intrusive VS Code
extensions or forks, such as Augment Code and Cursor, tend to log.

Features:
1. MAC:               Spoof MAC of the first active, non-loopback NIC.
2. Machine ID:        Regenerate machine-id.
3. Filesystem UUID:   Randomize root-filesystem UUID.
4. Hostname:          Set a fresh hostname.
5. VS Code Cache:     Purge VS Code, Cursor, and Augment Code caches.
6. New User:          Create a throw-away user.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable

from tui import create_tui
from utils.cleaner import clean_vscode_caches
from utils.helper import parse_args, root_check
from utils.spoofer import spoof_filesystem_uuid, spoof_mac_addr, spoof_machine_id
from utils.system import change_hostname, create_user, update_boot_config


def main() -> None:
    """Main application entry point."""
    args: argparse.Namespace = parse_args()
    assume_yes: bool = args.non_interactive
    skip_uuid: bool = args.no_uuid

    # Initialize TUI
    tui = create_tui()

    # Check root privileges
    try:
        _inv_user, home = root_check()
    except SystemExit:
        error_message: str = (
            "❌ This script requires root privileges.\nPlease run with sudo."
        )
        error_panel = tui.create_error_panel(error_message, "Permission Error")
        tui.print(error_panel)
        sys.exit(1)

    # Display header
    tui.print(tui.create_header())
    tui.print()

    # Display features table
    tui.print(tui.create_features_table())
    tui.print()

    # Confirmation prompt
    if not assume_yes:
        proceed: bool = tui.ask_confirmation(
            "🚀 [bold cyan]Proceed with spoofing operations?[/bold cyan]",
            default=True,
        )
        if not proceed:
            cancel_panel = tui.create_cancel_panel()
            tui.print(cancel_panel)
            return

    # Progress tracking
    operations: list[tuple[str, Callable[[], bool]]] = [
        ("MAC Address", lambda: spoof_mac_addr()),
        ("Machine ID", lambda: spoof_machine_id()),
        ("Filesystem UUID", lambda: spoof_filesystem_uuid() if not skip_uuid else True),
        ("Hostname", lambda: change_hostname()),
        ("VS Code Caches", lambda: clean_vscode_caches(home)),
        ("Boot Config", lambda: update_boot_config()),
    ]

    # Add user creation if requested
    user_prompt: str = "👤 Create throw-away user 'vscode_sandbox'?"
    create_user_confirmed: bool = assume_yes or tui.ask_confirmation(
        user_prompt, default=False
    )
    if create_user_confirmed:
        user_operation: tuple[str, Callable[[], bool]] = (
            "New User",
            lambda: create_user(),
        )
        operations.append(user_operation)

    # Run operations with progress display
    results: dict[str, bool] = tui.run_operations_with_progress(operations)

    tui.print()
    tui.print(tui.create_status_panel(results))

    # Final message
    tui.display_final_results(results)


if __name__ == "__main__":
    main()
