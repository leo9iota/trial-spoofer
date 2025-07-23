#!/usr/bin/env python3
"""
Spoofer module

Responsible for spoofing identifiers, such as MAC address,
filesystem UUID, VS Code, and the machine ID.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from collections.abc import Iterator
from pathlib import Path

from .command import CmdError, run_cmd
from .helpers import rand_mac


def spoof_vscode(home: Path) -> bool:
    """
    Remove VS Code cache and configuration files.

    Parameters
    ----------
    home : Path
        User's home directory path.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    vscode_caches: list[str] = [
        ".config/Code*",
        ".vscode*",
        ".config/cursor",
        ".cursor",
        ".cache/augment*",
    ]

    try:
        for glob_pattern in vscode_caches:
            cache_paths: Iterator[Path] = home.glob(glob_pattern)
            for cache_path in cache_paths:
                if cache_path.exists():
                    shutil.rmtree(cache_path, ignore_errors=True)

        return True
    except Exception:
        return False


def spoof_mac_addr() -> bool:
    """
    Change MAC address of the first non-loopback network interface.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    try:
        # Use shell=True for this complex awk command, but be careful
        iface: str = run_cmd(
            "ip -o link show | awk -F': ' '!/lo/ {print $2; exit}'",
            shell=True,
        )
        if iface:
            new_mac: str = rand_mac()
            run_cmd(f"ip link set dev {iface} down", capture=False)
            run_cmd(f"ip link set dev {iface} address {new_mac}", capture=False)
            run_cmd(f"ip link set dev {iface} up", capture=False)
            return True
        else:
            return False
    except (CmdError, subprocess.TimeoutExpired):
        return False


def spoof_machine_id() -> bool:
    """
    Generate a new machine ID.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    try:
        run_cmd("rm -f /etc/machine-id", capture=False)
        run_cmd("systemd-machine-id-setup", capture=False)
        return True
    except (CmdError, subprocess.TimeoutExpired):
        return False


def spoof_filesystem_uuid() -> bool:
    """
    Change filesystem UUID and update system configuration files.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    try:
        root_dev: str = run_cmd("findmnt -no SOURCE /")
        fstype: str = run_cmd("findmnt -no FSTYPE /")

        if not root_dev:
            return False

        if fstype == "ext4":
            run_cmd(f"tune2fs -U random {root_dev}", capture=False, timeout=30.0)
        elif fstype == "btrfs":
            run_cmd(f"btrfstune -u {root_dev}", capture=False, timeout=30.0)
        else:
            return False

        # Update fstab
        new_uuid: str = run_cmd(f"blkid -s UUID -o value {root_dev}")
        if new_uuid:
            fstab_path: Path = Path("/etc/fstab")
            fstab_content: str = fstab_path.read_text()
            uuid_pattern: str = r"UUID=[A-Fa-f0-9-]+"
            updated_fstab: str = re.sub(
                uuid_pattern, f"UUID={new_uuid}", fstab_content, count=1
            )
            fstab_path.write_text(updated_fstab)

            # Update crypttab if present
            crypttab_path: Path = Path("/etc/crypttab")
            if crypttab_path.exists():
                crypttab_content: str = crypttab_path.read_text()
                updated_crypttab: str = re.sub(
                    uuid_pattern, f"UUID={new_uuid}", crypttab_content
                )
                crypttab_path.write_text(updated_crypttab)

        return True
    except (CmdError, subprocess.TimeoutExpired):
        return False
