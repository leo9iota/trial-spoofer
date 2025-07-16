#!/usr/bin/env python3
"""
Spoofing utilities for MAC address, machine ID, and filesystem UUID.
"""

from __future__ import annotations

import re
from pathlib import Path

from .helper import log, rand_mac, run


def spoof_mac_addr() -> bool:
    """Spoof MAC address of the first active, non-loopback NIC."""
    try:
        iface: str | None = run(
            "ip -o link show | awk -F': ' '!/lo/ {print $2; exit}'",
            capture=True,
        )
        if iface:
            new_mac: str = rand_mac()
            log(f"Setting {iface} MAC → {new_mac}")
            run(f"ip link set dev {iface} down")
            run(f"ip link set dev {iface} address {new_mac}")
            run(f"ip link set dev {iface} up")
            return True
        else:
            log("No active non-loopback NIC found - skipping MAC spoof.")
            return False
    except Exception as e:
        error_msg: str = str(e)
        log(f"Failed to spoof MAC address: {error_msg}")
        return False


def spoof_machine_id() -> bool:
    """Regenerate /etc/machine-id."""
    try:
        log("Regenerating machine‑id …")
        run("rm -f /etc/machine-id")
        run("systemd-machine-id-setup")
        return True
    except Exception as e:
        error_msg: str = str(e)
        log(f"Failed to regenerate machine ID: {error_msg}")
        return False


def spoof_filesystem_uuid() -> bool:
    """Randomize root-filesystem UUID."""
    try:
        root_dev: str | None = run("findmnt -no SOURCE /", capture=True)
        fstype: str | None = run("findmnt -no FSTYPE /", capture=True)

        if not root_dev:
            log("Could not determine root device")
            return False

        if fstype == "ext4":
            log("tune2fs -U random …")
            run(f"tune2fs -U random {root_dev}")
        elif fstype == "btrfs":
            log("btrfstune -u …")
            run(f"btrfstune -u {root_dev}")
        else:
            log(f"Filesystem {fstype} not supported - skipping UUID change.")
            return False

        # Update fstab
        new_uuid: str | None = run(
            f"blkid -s UUID -o value {root_dev}", capture=True
        )
        if new_uuid:
            log(f"Updating /etc/fstab with {new_uuid}")
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
    except Exception as e:
        error_msg: str = str(e)
        log(f"Failed to spoof filesystem UUID: {error_msg}")
        return False
