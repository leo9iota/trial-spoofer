#!/usr/bin/env python3
"""
Linux VS Code Spoofer

Script to wipe every host-side identifier that intrusive VS Code
extensions or forks, such as Augment Code and Cursor, tend to log.

Features
~~~~~~~~
1. MAC:               Spoof MAC of the first active, non-loopback NIC.
2. Machine ID:        Regenerate machine-id.
3. Filesystem UUID:   Randomize root-filesystem UUID.
4. Hostname:          Set a fresh hostname.
5. VS Code Cache:     Purge VS Code, Cursor, and Augment Code caches.
6. New User:          Create a throw-away user.

Usage
~~~~~
    sudo python linux_vscode_spoofer_v4.py <OPTIONS>

Options
~~~~~~~
    --non-interactive  Run non-interactive mode and auto-confirm all safe steps.
    --no-uuid          Skip the UUID rewrite if you don't want to touch fstab.
"""

from __future__ import annotations

import argparse
import os
import random
import re
import shutil
import subprocess as sp
import sys
from pathlib import Path


# ─────── #
# Helpers #
# ─────── #
def run(cmd: str, capture: bool = False, check: bool = True) -> str | None:
    """Thin wrapper around subprocess.run("cmd", shell=True …)."""
    res = sp.run(
        cmd,
        shell=True,
        stdout=sp.PIPE if capture else None,
        stderr=sp.STDOUT,
        text=True,
    )
    if check and res.returncode != 0:
        raise RuntimeError(
            f"Command failed ({res.returncode}): {cmd}\n{res.stdout}"
        )
    return res.stdout.strip() if capture else None


def ask(msg: str, default_yes: bool, assume_yes: bool) -> bool:
    if assume_yes:
        return True
    yes, no = {"y", "yes"}, {"n", "no"}
    prompt = "[Y/n]" if default_yes else "[y/N]"
    while True:
        ans = input(f"{msg} {prompt}: ").strip().lower()
        if ans == "":
            return default_yes
        if ans in yes:
            return True
        if ans in no:
            return False


def rand_mac() -> str:
    return "02:" + ":".join(f"{random.randint(0, 255):02x}" for _ in range(5))


def log(msg: str):
    print(f"[+] {msg}")


# ──────────────── #
# Argument Parsing #
# ──────────────── #
parser = argparse.ArgumentParser(
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
args = parser.parse_args()

ASSUME_YES = args.non_interactive
SKIP_UUID = args.no_uuid

# ────────── #
# Root Check #
# ────────── #
if os.geteuid() != 0:
    sys.exit("Run this script with sudo.")

INV_USER = os.environ.get("SUDO_USER") or os.environ.get("USER")
HOME = Path("/root") if INV_USER == "root" else Path(f"/home/{INV_USER}")

print("\n++++++++++++ Linux VS Code Spoofer ++++++++++++\n")

# ──────────── #
# 1. Spoof MAC #
# ──────────── #
if ask("Spoof MAC address?", True, ASSUME_YES):
    iface = run(
        "ip -o link show | awk -F': ' '!/lo/ {print $2; exit}'", capture=True
    )
    if iface:
        new_mac = rand_mac()
        log(f"Setting {iface} MAC → {new_mac}")
        run(f"ip link set dev {iface} down")
        run(f"ip link set dev {iface} address {new_mac}")
        run(f"ip link set dev {iface} up")
    else:
        log("No active non-loopback NIC found - skipping MAC spoof.")

# ──────────────────────── #
# 2. Regenerate Machine ID #
# ──────────────────────── #
if ask("Regenerate /etc/machine-id?", True, ASSUME_YES):
    log("Regenerating machine‑id …")
    run("rm -f /etc/machine-id")
    run("systemd-machine-id-setup")

# ──────────────────────── #
# 3. Spoof Filesystem UUID #
# ──────────────────────── #
root_dev = run("findmnt -no SOURCE /", capture=True)
fstype = run("findmnt -no FSTYPE /", capture=True)
if (
    not SKIP_UUID
    and root_dev
    and ask(
        f"Randomize root-fs UUID on {root_dev} ({fstype})?", True, ASSUME_YES
    )
):
    if fstype == "ext4":
        log("tune2fs -U random …")
        run(f"tune2fs -U random {root_dev}")
    elif fstype == "btrfs":
        log("btrfstune -u …")
        run(f"btrfstune -u {root_dev}")
    else:
        log(f"Filesystem {fstype} not supported - skipping UUID change.")
        root_dev = None

    if root_dev:
        new_uuid = run(f"blkid -s UUID -o value {root_dev}", capture=True)
        log(f"Updating /etc/fstab with {new_uuid}")
        fstab = Path("/etc/fstab").read_text()
        fstab = re.sub(
            r"UUID=[A-Fa-f0-9-]+", f"UUID={new_uuid}", fstab, count=1
        )
        Path("/etc/fstab").write_text(fstab)
        # crypttab if present
        crypttab = Path("/etc/crypttab")
        if crypttab.exists():
            txt = crypttab.read_text()
            txt = re.sub(r"UUID=[A-Fa-f0-9-]+", f"UUID={new_uuid}", txt)
            crypttab.write_text(txt)


# ──────────────── #
# 3b. Boot refresh #
# ──────────────── #
if root_dev:
    # GRUB
    if Path("/boot/grub/grub.cfg").exists():
        run("grub-mkconfig -o /boot/grub/grub.cfg", check=False)
    # systemd-boot
    elif Path("/boot/loader/loader.conf").exists():
        run("bootctl update", check=False)

    # Regenerate initramfs if crypttab was touched
    if Path("/etc/crypttab").exists():
        if Path("/etc/arch-release").exists():
            run("mkinitcpio -P", check=False)
        else:  # Debian/Ubuntu
            run("update-initramfs -u -k all", check=False)


# ────────────────── #
# 4. Change Hostname #
# ────────────────── #
if ask("Set a new random hostname?", True, ASSUME_YES):
    new_host = f"sandbox-{random.randint(1000, 9999)}"
    log(f"hostnamectl set-hostname {new_host}")
    run(f"hostnamectl set-hostname {new_host}")

# ─────────────────────── #
# 5. Purge VS Code Caches #
# ─────────────────────── #
if ask(
    "Purge VS Code / Cursor / Augment caches under $HOME?", True, ASSUME_YES
):
    purge_globs = [
        ".config/Code*",
        ".vscode*",
        ".config/cursor",
        ".cursor",
        ".cache/augment*",
    ]
    for g in purge_globs:
        for p in HOME.glob(g):
            if p.exists():
                log(f"Removing {p}")
                shutil.rmtree(p, ignore_errors=True)

# ────────────────── #
# 6. Create New User #
# ────────────────── #
if ask("Create throw-away user 'vscode_sandbox'?", False, ASSUME_YES):
    user = "vscode_sandbox"
    if sp.call(f"id -u {user}", shell=True) != 0:
        pw = f"Vs@{random.randint(10000, 99999)}"
        log(f"Adding user {user} (password: {pw})")
        run(f"useradd -m {user}")
        run(f"echo '{user}:{pw}' | chpasswd")
    else:
        log("User already exists - skipping.")

print(
    "\nDone.\nReboot now so MAC, hostname and new machine-id take full effect.\n"
)
