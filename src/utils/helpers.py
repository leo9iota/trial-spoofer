#!/usr/bin/env python3
"""
Helper utilities for the VS Code Spoofer.
"""

from __future__ import annotations


import os
import random
import shutil
import subprocess as sp
import sys
from collections.abc import Iterator
from pathlib import Path


def root_check() -> tuple[str, Path]:
    """Check if running as root and return invoking user and home path."""
    if os.geteuid() != 0:
        sys.exit("Run this script with sudo.")

    inv_user: str = os.environ.get("SUDO_USER") or os.environ.get("USER") or "root"
    home: Path = Path("/root") if inv_user == "root" else Path(f"/home/{inv_user}")
    return inv_user, home


def run_cmd(cmd: str, capture: bool = False, check: bool = True) -> str | None:
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
        error_message: str = (
            f"Command failed ({res.returncode}): {cmd}\n{stdout_output}"
        )
        raise RuntimeError(error_message)
    return res.stdout.strip() if capture and res.stdout else None



def rand_mac() -> str:
    """Generate a random MAC address."""
    mac_parts: list[str] = [f"{random.randint(0, 255):02x}" for _ in range(5)]
    return "02:" + ":".join(mac_parts)


def log(msg: str) -> None:
    """Log a message with [+] prefix."""
    print(f"[+] {msg}")





def clean_vscode_caches(home: Path) -> bool:
    """Purge VS Code / Cursor / Augment caches under $HOME."""
    try:
        purge_globs: list[str] = [
            ".config/Code*",
            ".vscode*",
            ".config/cursor",
            ".cursor",
            ".cache/augment*",
        ]

        cleaned_any: bool = False
        for glob_pattern in purge_globs:
            cache_paths: Iterator[Path] = home.glob(glob_pattern)
            for cache_path in cache_paths:
                if cache_path.exists():
                    log_message: str = f"Removing {cache_path}"
                    log(log_message)
                    shutil.rmtree(cache_path, ignore_errors=True)
                    cleaned_any = True

        if not cleaned_any:
            no_cache_message: str = "No VS Code caches found to clean"
            log(no_cache_message)

        return True
    except Exception as e:
        error_msg: str = str(e)
        log(f"Failed to clean VS Code caches: {error_msg}")
        return False
