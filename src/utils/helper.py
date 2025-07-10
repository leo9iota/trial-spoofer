#!/usr/bin/env python3
"""
Helper utilities for the VS Code Spoofer.
"""

from __future__ import annotations

import argparse
import os
import random
import subprocess as sp
import sys
from pathlib import Path



def run(cmd: str, capture: bool = False, check: bool = True) -> str | None:
    """Thin wrapper around subprocess.run("cmd", shell=True …)."""
    res: sp.CompletedProcess[str] = sp.run(
        cmd,
        shell=True,
        stdout=sp.PIPE if capture else None,
        stderr=sp.STDOUT,
        text=True,
    )
    if check and res.returncode != 0:
        stdout_output: str = res.stdout or ""
        error_message: str = f"Command failed ({res.returncode}): {cmd}\n{stdout_output}"
        raise RuntimeError(error_message)
    return res.stdout.strip() if capture and res.stdout else None


def ask(msg: str, default_yes: bool, assume_yes: bool) -> bool:
    """Ask user for confirmation with yes/no prompt."""
    if assume_yes:
        return True
    yes: set[str] = {"y", "yes"}
    no: set[str] = {"n", "no"}
    prompt: str = "[Y/n]" if default_yes else "[y/N]"
    while True:
        prompt_text: str = f"{msg} {prompt}: "
        ans: str = input(prompt_text).strip().lower()
        if ans == "":
            return default_yes
        if ans in yes:
            return True
        if ans in no:
            return False


def rand_mac() -> str:
    """Generate a random MAC address."""
    mac_parts: list[str] = [f"{random.randint(0, 255):02x}" for _ in range(5)]
    return "02:" + ":".join(mac_parts)


def log(msg: str) -> None:
    """Log a message with [+] prefix."""
    print(f"[+] {msg}")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Reset most host fingerprints for VS Code extensions"
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="non-interactive: assume 'yes' for all safe steps",
    )
    parser.add_argument(
        "--no-uuid", action="store_true", help="skip filesystem UUID rewrite"
    )
    return parser.parse_args()


def root_check() -> tuple[str, Path]:
    """Check if running as root and return invoking user and home path."""
    if os.geteuid() != 0:
        sys.exit("Run this script with sudo.")

    inv_user: str = os.environ.get("SUDO_USER") or os.environ.get("USER") or "root"
    home: Path = Path("/root") if inv_user == "root" else Path(f"/home/{inv_user}")
    return inv_user, home
