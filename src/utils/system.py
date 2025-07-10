#!/usr/bin/env python3
"""
System utilities for hostname changes and boot configuration updates.
"""

from __future__ import annotations

import random
import subprocess as sp
from pathlib import Path

from .helper import log, run


def change_hostname() -> bool:
    """Set a new random hostname."""
    try:
        new_host: str = f"sandbox-{random.randint(1000, 9999)}"
        log(f"hostnamectl set-hostname {new_host}")
        run(f"hostnamectl set-hostname {new_host}")
        return True
    except Exception as e:
        log(f"Failed to change hostname: {e}")
        return False


def update_boot_config() -> bool:
    """Update boot configuration after UUID changes."""
    try:
        # GRUB
        grub_cfg: Path = Path("/boot/grub/grub.cfg")
        if grub_cfg.exists():
            run("grub-mkconfig -o /boot/grub/grub.cfg", check=False)
        # systemd-boot
        else:
            systemd_boot_conf: Path = Path("/boot/loader/loader.conf")
            if systemd_boot_conf.exists():
                run("bootctl update", check=False)

        # Regenerate initramfs if crypttab was touched
        crypttab_path: Path = Path("/etc/crypttab")
        if crypttab_path.exists():
            arch_release: Path = Path("/etc/arch-release")
            if arch_release.exists():
                run("mkinitcpio -P", check=False)
            else:  # Debian/Ubuntu
                run("update-initramfs -u -k all", check=False)

        return True
    except Exception as e:
        log(f"Failed to update boot config: {e}")
        return False


def create_user() -> bool:
    """Create throw-away user 'vscode_sandbox'."""
    try:
        user: str = "vscode_sandbox"
        user_check_result: int = sp.call(f"id -u {user}", shell=True)
        if user_check_result != 0:
            pw: str = f"Vs@{random.randint(10000, 99999)}"
            log(f"Adding user {user} (password: {pw})")
            run(f"useradd -m {user}")
            run(f"echo '{user}:{pw}' | chpasswd")
        else:
            log("User already exists - skipping.")
        return True
    except Exception as e:
        log(f"Failed to create user: {e}")
        return False
