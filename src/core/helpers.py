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


# Generate random MAC address
def rand_mac() -> str:
    mac_parts: list[str] = [f"{random.randint(0, 255):02x}" for _ in range(5)]
    return "02:" + ":".join(mac_parts)


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
