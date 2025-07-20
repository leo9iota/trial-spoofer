#!/usr/bin/env python3
"""
Spoofer module

Responsible for spoofing indentifiers, such as MAC address,
filesystem UUID, VS Code, and the machine ID.
"""

from __future__ import annotations

import re
import shutil
from collections.abc import Iterator
from pathlib import Path

from .helpers import rand_mac
from .system import run_cmd


def spoof_vscode(home: Path) -> bool:
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
    try:
        iface: str | None = run_cmd(
            "ip -o link show | awk -F': ' '!/lo/ {print $2; exit}'",
            capture=True,
        )
        if iface:
            new_mac: str = rand_mac()
            run_cmd(f"ip link set dev {iface} down")
            run_cmd(f"ip link set dev {iface} address {new_mac}")
            run_cmd(f"ip link set dev {iface} up")
            return True
        else:
            return False
    except Exception:
        return False


def spoof_machine_id() -> bool:
    try:
        run_cmd("rm -f /etc/machine-id")
        run_cmd("systemd-machine-id-setup")
        return True
    except Exception:
        return False


def spoof_filesystem_uuid() -> bool:
    try:
        root_dev: str | None = run_cmd("findmnt -no SOURCE /", capture=True)
        fstype: str | None = run_cmd("findmnt -no FSTYPE /", capture=True)

        if not root_dev:
            return False

        if fstype == "ext4":
            run_cmd(f"tune2fs -U random {root_dev}")
        elif fstype == "btrfs":
            run_cmd(f"btrfstune -u {root_dev}")
        else:
            return False

        # Update fstab
        new_uuid: str | None = run_cmd(
            f"blkid -s UUID -o value {root_dev}", capture=True
        )
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
    except Exception:
        return False
