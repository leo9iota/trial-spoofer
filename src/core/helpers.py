#!/usr/bin/env python3

from __future__ import annotations

import os
import random
import shutil
import subprocess as sp
import sys
from collections.abc import Iterator
from pathlib import Path


# Check if user is running script as root
def root_check() -> tuple[str, Path]:
    if os.geteuid() != 0:
        sys.exit("Run this script with sudo.")

    inv_user: str = os.environ.get("SUDO_USER") or os.environ.get("USER") or "root"
    home: Path = Path("/root") if inv_user == "root" else Path(f"/home/{inv_user}")
    return inv_user, home


# Thin wrapper around "subprocess.run()" function
def run_cmd(cmd: str, capture: bool = False, check: bool = True) -> str | None:
    res: sp.CompletedProcess[str] = sp.run(
        cmd,
        shell=True,
        stdout=sp.PIPE if capture else None,
        stderr=sp.STDOUT,
        text=True,
    )
    if check and res.returncode != 0:
        stdout_output: str = res.stdout or ""
        error_message: str = (
            f"Command failed ({res.returncode}): {cmd}\n{stdout_output}"
        )
        raise RuntimeError(error_message)
    return res.stdout.strip() if capture and res.stdout else None


# Generate random MAC address
def rand_mac() -> str:
    mac_parts: list[str] = [f"{random.randint(0, 255):02x}" for _ in range(5)]
    return "02:" + ":".join(mac_parts)


# Delete all VS Code caches
def delete_vscode_caches(home: Path) -> bool:
    try:
        purge_globs: list[str] = [
            ".config/Code*",
            ".vscode*",
            ".config/cursor",
            ".cursor",
            ".cache/augment*",
        ]

        for glob_pattern in purge_globs:
            cache_paths: Iterator[Path] = home.glob(glob_pattern)
            for cache_path in cache_paths:
                if cache_path.exists():
                    shutil.rmtree(cache_path, ignore_errors=True)

        return True
    except Exception:
        return False


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
