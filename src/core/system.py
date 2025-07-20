#!/usr/bin/env python3
"""
System utilities for hostname changes and boot configuration updates.
"""

from __future__ import annotations

import os
import platform
import random
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path


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


def root_check() -> tuple[str, Path]:
    if os.geteuid() != 0:
        sys.exit("Run this script with sudo.")

    inv_user: str = os.environ.get("SUDO_USER") or os.environ.get("USER") or "root"
    home: Path = Path("/root") if inv_user == "root" else Path(f"/home/{inv_user}")
    return inv_user, home


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


def check_system_requirements(self) -> bool:
    try:
        if platform.system() != "Linux":
            self.user_input.display_error("This tool only works on Linux systems.")
            return False

        required_commands = ["ip", "systemctl", "hostnamectl"]
        missing_commands = []

        for cmd in required_commands:
            try:
                run_cmd(f"which {cmd}", capture=True)
            except Exception:
                missing_commands.append(cmd)

        if missing_commands:
            self.user_input.display_error(
                f"Missing required commands: {', '.join(missing_commands)}"
            )
            return False

        return True

    except Exception as e:
        self.user_input.display_error(f"System validation failed: {e}")
        return False


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