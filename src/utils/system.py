#!/usr/bin/env python3
"""
System utilities for hostname changes and boot configuration updates.
"""

from __future__ import annotations

import random
import subprocess as sp
from pathlib import Path

from .helper import log, run_cmd


def change_hostname() -> bool:
    """Set a new random hostname."""
    try:
        random_number: int = random.randint(1000, 9999)
        new_host: str = f"sandbox-{random_number}"
        hostname_cmd: str = f"hostnamectl set-hostname {new_host}"
        log(hostname_cmd)
        run_cmd(hostname_cmd)
        return True
    except Exception as e:
        error_msg: str = str(e)
        log(f"Failed to change hostname: {error_msg}")
        return False


def update_boot_config() -> bool:
    """Update boot configuration after UUID changes."""
    try:
        # GRUB
        grub_cfg: Path = Path("/boot/grub/grub.cfg")
        grub_config_cmd: str = "grub-mkconfig -o /boot/grub/grub.cfg"
        if grub_cfg.exists():
            run_cmd(grub_config_cmd, check=False)
        # systemd-boot
        else:
            systemd_boot_conf: Path = Path("/boot/loader/loader.conf")
            bootctl_cmd: str = "bootctl update"
            if systemd_boot_conf.exists():
                run_cmd(bootctl_cmd, check=False)

        # Regenerate initramfs if crypttab was touched
        crypttab_path: Path = Path("/etc/crypttab")
        if crypttab_path.exists():
            arch_release: Path = Path("/etc/arch-release")
            if arch_release.exists():
                arch_initramfs_cmd: str = "mkinitcpio -P"
                run_cmd(arch_initramfs_cmd, check=False)
            else:  # Debian/Ubuntu
                debian_initramfs_cmd: str = "update-initramfs -u -k all"
                run_cmd(debian_initramfs_cmd, check=False)

        return True
    except Exception as e:
        error_msg: str = str(e)
        log(f"Failed to update boot config: {error_msg}")
        return False


def create_user() -> bool:
    """Create throw-away user 'vscode_sandbox'."""
    try:
        user: str = "vscode_sandbox"
        user_check_cmd: str = f"id -u {user}"
        user_check_result: int = sp.call(user_check_cmd, shell=True)
        if user_check_result != 0:
            random_number: int = random.randint(10000, 99999)
            pw: str = f"Vs@{random_number}"
            log(f"Adding user {user} (password: {pw})")
            useradd_cmd: str = f"useradd -m {user}"
            passwd_cmd: str = f"echo '{user}:{pw}' | chpasswd"
            run_cmd(useradd_cmd)
            run_cmd(passwd_cmd)
        else:
            log("User already exists - skipping.")
        return True
    except Exception as e:
        error_msg: str = str(e)
        log(f"Failed to create user: {error_msg}")
        return False
