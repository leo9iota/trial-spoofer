#!/usr/bin/env python3
"""
System utilities for hostname changes and boot configuration updates.
"""

from __future__ import annotations

import random
import subprocess as sp

from .helpers import run_cmd


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



def create_user(custom_username: str | None = None) -> bool:
    """Create throw-away user (custom name or 'vscode_sandbox')."""
    try:
        user: str = custom_username if custom_username else "vscode_sandbox"
        user_check_cmd: str = f"id -u {user}"
        user_check_result: int = sp.call(user_check_cmd, shell=True)
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
