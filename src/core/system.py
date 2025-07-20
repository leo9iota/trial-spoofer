#!/usr/bin/env python3
"""
System module

Responsible executing system commands, that change the filesystem UUID,
user accounts, hostname, etc.

Also executes shell commands.
"""

from __future__ import annotations

import random
import subprocess


# Thin wrapper around "subprocess.run()" function
def run_cmd(cmd: str, capture: bool = False, check: bool = True) -> str | None:
    res: subprocess.CompletedProcess[str] = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if check and res.returncode != 0:
        stdout_output: str = res.stdout or ""
        error_message: str = (
            f"Command failed ({res.returncode}): {cmd}\n{stdout_output}"
        )
        raise RuntimeError(error_message)
    return res.stdout.strip() if capture and res.stdout else None


def change_hostname(custom_hostname: str | None = None) -> bool:
    """Set a new hostname (custom or random)."""
    try:
        if custom_hostname:
            new_host: str = custom_hostname
        else:
            random_number: int = random.randint(1000, 9999)
            new_host = f"sandbox-{random_number}"

        hostname_cmd: str = f"hostnamectl set-hostname {new_host}"
        run_cmd(hostname_cmd)
        return True
    except Exception:
        return False


def create_new_user(custom_username: str | None = None) -> bool:
    """Create throw-away user (custom name or 'vscode_sandbox')."""
    try:
        user: str = custom_username if custom_username else "vscode_sandbox"
        user_check_cmd: str = f"id -u {user}"
        user_check_result: int = subprocess.call(user_check_cmd, shell=True)
        if user_check_result != 0:
            random_number: int = random.randint(10000, 99999)
            pw: str = f"Vs@{random_number}"
            useradd_cmd: str = f"useradd -m {user}"
            passwd_cmd: str = f"echo '{user}:{pw}' | chpasswd"
            run_cmd(useradd_cmd)
            run_cmd(passwd_cmd)
        return True
    except Exception:
        return False


def update_boot_loader() -> bool:
    """Update GRUB and initramfs."""
    try:
        run_cmd("update-grub")
        run_cmd("update-initramfs -u")
        return True
    except Exception:
        return False
