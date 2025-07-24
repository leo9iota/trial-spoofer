#!/usr/bin/env python3

"""
Helpers

Responsible for providing helper functions, such as a random MAC address generator,
root privileges check, etc.
"""

from __future__ import annotations

import os
import platform
import random
import sys
from pathlib import Path

from .command import CmdError, run_cmd


def check_root() -> tuple[str, Path]:
    """
    Check if user is running script as root and return user info.

    Returns
    -------
    tuple[str, Path]
        Tuple of (username, home_directory)

    Raises
    ------
    SystemExit
        If not running as root.
    """
    if os.geteuid() != 0:
        sys.exit("Run this script with sudo.")

    inv_user: str = os.environ.get("SUDO_USER") or os.environ.get("USER") or "root"
    home: Path = Path("/root") if inv_user == "root" else Path(f"/home/{inv_user}")
    return inv_user, home


def check_system_requirements() -> bool:
    """Check if all required system commands are available.

    Returns
    -------
    bool
        True if all requirements are met, False otherwise.
    """
    try:
        if platform.system() != "Linux":
            return False

        required_commands = ["ip", "systemctl", "hostnamectl"]
        missing_commands = []

        for cmd in required_commands:
            try:
                run_cmd(f"which {cmd}")
            except CmdError:
                missing_commands.append(cmd)

        return len(missing_commands) == 0

    except Exception as e:
        print(f"Error checking system requirements: {e}")
        return False


def rand_mac(*, locally_admin: bool = True, unicast: bool = True) -> str:
    """Return a random MAC address.

    Parameters
    ----------
    locally_admin : bool, optional
        If True (default), set the locally administered bit (LAA).
        This indicates the MAC address is locally assigned rather than
        globally unique from the manufacturer.
    unicast : bool, optional
        If True (default), clear the multicast bit to ensure unicast addressing.

    Returns
    -------
    str
        A randomly generated MAC address in the format "xx:xx:xx:xx:xx:xx".

    Notes
    -----
    - Setting locally_admin=True sets bit 1 of the first octet (0x02)
    - Setting unicast=True clears bit 0 of the first octet (0xFE mask)
    - This ensures the generated MAC follows proper addressing conventions
    """
    first = random.randint(0, 255)

    if locally_admin:
        first |= 0x02  # Set LAA (Locally Administered Address) bit
    else:
        first &= ~0x02  # Clear LAA bit for globally unique addresses

    if unicast:
        first &= 0xFE  # Clear multicast bit for unicast addressing

    # Generate remaining 5 octets
    parts = [first] + [random.randint(0, 255) for _ in range(5)]

    return ":".join(f"{p:02x}" for p in parts)


def validate_mac_address(mac: str) -> bool:
    """Validate MAC address format.

    Parameters
    ----------
    mac : str
        MAC address string to validate.

    Returns
    -------
    bool
        True if valid MAC address format, False otherwise.
    """
    import re

    # Match standard MAC address formats: xx:xx:xx:xx:xx:xx or xx-xx-xx-xx-xx-xx
    pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    return bool(re.match(pattern, mac))


def get_network_interfaces() -> dict[str, dict[str, str]]:
    """Get information about available network interfaces.

    Returns
    -------
    dict[str, dict[str, str]]
        Dictionary mapping interface names to their properties.
        Each interface dict contains: 'mac', 'state', 'type'
    """
    interfaces = {}

    try:
        # Get interface information
        result = run_cmd("ip -o link show", timeout=10)
        lines = result.strip().split("\n")

        for line in lines:
            if ":" not in line:
                continue

            parts = line.split(":")
            if len(parts) < 3:
                continue

            # Extract interface name (remove @ suffix if present)
            iface_name = parts[1].strip().split("@")[0]

            # Skip loopback
            if iface_name == "lo" or "LOOPBACK" in line:
                continue

            # Extract MAC address
            mac = "Unknown"
            if "link/ether" in line:
                mac_part = line.split("link/ether")[1].split()[0]
                if validate_mac_address(mac_part):
                    mac = mac_part

            # Extract state
            state = "DOWN"
            if "state UP" in line:
                state = "UP"
            elif "state DOWN" in line:
                state = "DOWN"
            elif "state UNKNOWN" in line:
                state = "UNKNOWN"

            # Determine interface type
            iface_type = "ethernet"
            if "link/ether" in line:
                iface_type = "ethernet"
            elif "link/none" in line:
                iface_type = "virtual"
            elif "link/sit" in line:
                iface_type = "tunnel"

            interfaces[iface_name] = {"mac": mac, "state": state, "type": iface_type}

    except (CmdError, Exception) as e:
        print(f"Error getting network interfaces: {e}", file=sys.stderr)

    return interfaces


def get_identifiers() -> dict[str, str]:
    identifiers = {}

    try:
        # MAC Address (first active interface)
        import subprocess

        result = subprocess.run(
            ["ip", "link", "show"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.split("\n")
            for line in lines:
                if "link/ether" in line and "state UP" in lines[lines.index(line) - 1]:
                    mac = line.split("link/ether")[1].split()[0]
                    identifiers["MAC Address"] = mac
                    break
            if "MAC Address" not in identifiers:
                identifiers["MAC Address"] = "Not found"
        else:
            identifiers["MAC Address"] = "Not found"
    except Exception:
        identifiers["MAC Address"] = "Not found"

    try:
        # Machine ID
        with open("/etc/machine-id") as f:
            identifiers["Machine ID"] = f.read().strip()
    except Exception:
        identifiers["Machine ID"] = "Not found"

    try:
        # Filesystem UUID (root partition)
        result = subprocess.run(
            ["findmnt", "-n", "-o", "UUID", "/"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            identifiers["Filesystem UUID"] = result.stdout.strip()
        else:
            identifiers["Filesystem UUID"] = "Not found"
    except Exception:
        identifiers["Filesystem UUID"] = "Not found"

    try:
        # Hostname
        with open("/etc/hostname") as f:
            identifiers["Hostname"] = f.read().strip()
    except Exception:
        try:
            result = subprocess.run(
                ["hostname"], capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                identifiers["Hostname"] = result.stdout.strip()
            else:
                identifiers["Hostname"] = "Not found"
        except Exception:
            identifiers["Hostname"] = "Not found"

    return identifiers
