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
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Optional

from .command import CmdError, run_cmd
from .helpers import rand_mac, get_network_interfaces, validate_mac_address


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


def _log(message: str) -> None:
    """Simple logging function for spoofer operations.
    
    Parameters
    ----------
    message : str
        The message to log to stderr.
    """
    print(message, file=sys.stderr)


def get_eligible_interfaces() -> list[str]:
    """Get list of interfaces eligible for MAC spoofing.
    
    Returns
    -------
    list[str]
        List of interface names that can be used for MAC spoofing.
        Excludes loopback and virtual interfaces.
    """
    interfaces = get_network_interfaces()
    eligible = []
    
    for name, info in interfaces.items():
        # Skip virtual interfaces and those without proper MAC addresses
        if (info['type'] == 'ethernet' and 
            info['mac'] != 'Unknown' and 
            validate_mac_address(info['mac'])):
            eligible.append(name)
            
    return eligible


def spoof_mac_addr(interface: Optional[str] = None, custom_mac: Optional[str] = None) -> bool:
    """Spoof MAC address of a network interface.

    Parameters
    ----------
    interface : str, optional
        Specific interface to modify. If None, uses the first eligible
        non-loopback interface that is UP.
    custom_mac : str, optional
        Custom MAC address to set. If None, generates a random one.
        Must be in valid MAC address format (xx:xx:xx:xx:xx:xx).

    Returns
    -------
    bool
        True if successful, False otherwise.

    Notes
    -----
    - Only modifies interfaces that are not loopback devices
    - Temporarily brings the interface down during MAC change
    - Uses locally administered unicast MAC addresses by default
    - Validates custom MAC addresses before applying
    - Provides detailed logging for troubleshooting
    """
    try:
        if interface:
            # Use specified interface
            iface = interface.strip()
            _log(f"[MAC] Using specified interface: {iface}")
        else:
            # Find first eligible interface (UP, non-loopback)
            iface = run_cmd(
                "ip -o link show | awk -F': ' '!/ lo / && !/LOOPBACK/ {print $2; exit}'",
                shell=True,
            ).strip()
            
        if not iface:
            _log("[MAC] No eligible interface found; skipping.")
            return False
            
        # Validate interface exists and get current state
        try:
            current_state = run_cmd(f"ip link show {iface}")
            if "does not exist" in current_state.lower():
                _log(f"[MAC] Interface {iface} does not exist.")
                return False
        except CmdError:
            _log(f"[MAC] Interface {iface} not found or inaccessible.")
            return False
            
        # Use custom MAC or generate new one
        if custom_mac:
            if not validate_mac_address(custom_mac):
                _log(f"[MAC] ERROR: Invalid MAC address format: {custom_mac}")
                return False
            new_mac = custom_mac.lower()
            _log(f"[MAC] Using custom MAC address: {new_mac}")
        else:
            new_mac = rand_mac(locally_admin=True, unicast=True)
            _log(f"[MAC] Generated random MAC address: {new_mac}")
            
        _log(f"[MAC] Setting {iface} → {new_mac}")
        
        # Apply MAC address change
        run_cmd(f"ip link set dev {iface} down", capture=False)
        run_cmd(f"ip link set dev {iface} address {new_mac}", capture=False)
        run_cmd(f"ip link set dev {iface} up", capture=False)
        
        # Verify the change was successful
        try:
            verification = run_cmd(f"ip link show {iface}")
            if new_mac.lower() in verification.lower():
                _log(f"[MAC] Successfully changed {iface} MAC address to {new_mac}")
            else:
                _log(f"[MAC] Warning: MAC change may not have been applied correctly")
        except CmdError:
            _log(f"[MAC] Warning: Could not verify MAC address change")
            
        return True
        
    except (CmdError, subprocess.TimeoutExpired) as e:
        _log(f"[MAC] ERROR: Command failed - {e}")
        return False
    except Exception as e:
        _log(f"[MAC] ERROR: Unexpected error - {e}")
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
