#!/usr/bin/env python3

# System
#
# Responsible for executing system commands that change the filesystem UUID,
# user accounts, hostname, etc.

from __future__ import annotations

import random
import subprocess

from .command import CmdError, run_cmd


def change_hostname(custom_hostname: str | None = None) -> bool:
    """
    Change system hostname.

    Parameters
    ----------
    custom_hostname : str | None
        Custom hostname to set. If None, generates a random sandbox hostname.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    try:
        if custom_hostname:
            new_host: str = custom_hostname
        else:
            random_number: int = random.randint(1000, 9999)
            new_host = f"sandbox-{random_number}"

        run_cmd(f"hostnamectl set-hostname {new_host}", capture=False)
        return True
    except (CmdError, subprocess.TimeoutExpired):
        return False


def create_new_user(custom_username: str | None = None) -> bool:
    """
    Create a new user account.

    Parameters
    ----------
    custom_username : str | None
        Custom username to create. If None, uses 'vscode_sandbox'.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    try:
        user: str = custom_username if custom_username else "vscode_sandbox"

        # Check if user already exists using our improved run_cmd
        try:
            run_cmd(f"id -u {user}", capture=False)
            # User exists, no need to create
            return True
        except CmdError:
            # User doesn't exist, create it
            random_number: int = random.randint(10000, 99999)
            pw: str = f"Vs@{random_number}"

            run_cmd(f"useradd -m {user}", capture=False)
            # Use stdin input for password instead of shell command for security
            run_cmd("chpasswd", input=f"{user}:{pw}".encode(), capture=False)
            return True
    except (CmdError, subprocess.TimeoutExpired):
        return False


def update_boot_loader() -> bool:
    """
    Update boot loader configuration.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    try:
        run_cmd("update-grub", capture=False, timeout=60.0)
        run_cmd("update-initramfs -u", capture=False, timeout=120.0)
        return True
    except (CmdError, subprocess.TimeoutExpired):
        return False
