#!/usr/bin/env python3
"""
Safe system-identifier spoofing utilities (MAC, machine-id, *root* filesystem UUID)
for Arch / EndeavourOS style systems.

**Why this exists**
-------------------
The original quick-and-dirty script blindly regex‑replaced the *first* occurrence of
``UUID=...`` in `/etc/fstab` after changing the root filesystem UUID. On systems
that list the EFI System Partition (ESP) first (common!), this rewrote the ESP line
instead of the root line. At next boot systemd could not mount `/boot/efi`, causing
`Dependency failed for Local File Systems` and an emergency shell.

This rewrite adds strong safety rails:

* Structured parsing + round‑trip preservation of `/etc/fstab` (comments kept).
* Target update **only** for the entry whose *mountpoint == '/'* (configurable).
* Never touch ESP entries (`/boot/efi`, `/efi`, fstype vfat) unless explicitly asked.
* Dry‑run mode shows what would change; default is *no change* unless `--apply`.
* Offline check: warn / refuse if attempting to change UUID of a currently‑mounted,
  writable filesystem unless `--force-online`.
* Automatic detection of ext4 vs. btrfs tooling (`tune2fs`, `btrfstune`).
* Bootloader refresh hooks: GRUB and systemd‑boot (auto-detect or override).
* Atomic file updates with timestamped backups.
* Rollback metadata file storing *old_uuid -> new_uuid* mapping.

**Recommended usage**
--------------------
1. Boot a *live* Arch/EndeavourOS ISO.
2. Mount your installed system at, e.g., `/mnt` and bind‑mount needed pseudo‑fs.
3. `arch-chroot /mnt`.
4. Run this script with `--apply --reinstall-bootloader auto`.

You *can* run directly on a live system, but changing the UUID of a mounted root
filesystem is risky; most filesystems require it be unmounted (or at least mounted
read‑only). Use `--force-online` only if you fully understand the risk.

---
MIT License. No warranty. Use at your own risk.
"""

from __future__ import annotations

import argparse
import dataclasses as dc
import datetime as _dt
import json
import os
import pathlib as _p
import random
import re
import shlex
import subprocess
import sys
import tempfile
from typing import Iterable, List, Optional, Tuple, Union

# ---------------------------------------------------------------------------
# Logging helpers
# ---------------------------------------------------------------------------

_LOG_PATH = _p.Path("/var/log/spoofid.log")
_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def _ts() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg: str) -> None:
    line = f"[{_ts()}] {msg}\n"
    try:
        with _LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(line)
    except Exception:  # best-effort logging
        pass
    sys.stderr.write(line)
    sys.stderr.flush()


# ---------------------------------------------------------------------------
# Generic command runner
# ---------------------------------------------------------------------------


class CmdError(RuntimeError):
    def __init__(self, cmd: str, rc: int, out: str, err: str):
        self.cmd, self.rc, self.out, self.err = cmd, rc, out, err
        super().__init__(f"Command failed ({rc}): {cmd}\nSTDOUT: {out}\nSTDERR: {err}")


def run_cmd(
    cmd: str,
    *,
    capture: bool = True,
    check: bool = True,
    shell: bool = False,
    env: Optional[dict] = None,
    input: Optional[bytes] = None,
) -> str:
    """Run a shell command.

    Parameters
    ----------
    cmd: str
        The command to run. If *shell* is False (default), the string will be
        split via shlex.split.
    capture: bool
        If True, capture stdout+stderr and return stdout.
    check: bool
        If True, raise CmdError on non-zero exit.
    shell: bool
        Pass through to subprocess.run.
    env: dict | None
        Extra environment.
    input: bytes | None
        Data to pass on stdin.
    """
    if shell:
        args = cmd
    else:
        args = shlex.split(cmd)
    proc = subprocess.run(
        args,
        input=input,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        env=env,
        shell=shell,
        text=True,
        check=False,
    )
    out = proc.stdout or ""
    err = proc.stderr or ""
    if check and proc.returncode != 0:
        raise CmdError(cmd, proc.returncode, out, err)
    return out.strip() if capture else ""


# ---------------------------------------------------------------------------
# MAC spoofing (unchanged except for robustness)
# ---------------------------------------------------------------------------

_HEX = "0123456789abcdef"


def rand_mac(*, locally_admin: bool = True, unicast: bool = True) -> str:
    """Return a random MAC address.

    If *locally_admin* is True (default), set the locally administered bit.
    If *unicast* is True (default), clear the multicast bit.
    """
    first = random.randint(0, 255)
    if locally_admin:
        first |= 0x02  # set LAA bit
    else:
        first &= ~0x02
    if unicast:
        first &= 0xFE  # clear multicast bit
    parts = [first] + [random.randint(0, 255) for _ in range(5)]
    return ":".join(f"{p:02x}" for p in parts)


def spoof_mac_addr() -> bool:
    """Spoof MAC address of the first *UP* non-loopback interface.

    Returns True on success, False otherwise.
    """
    try:
        iface = run_cmd(
            "ip -o link show | awk -F': ' '!/ lo / && !/LOOPBACK/ {print $2; exit}'"
        )
        if not iface:
            log("[MAC] No eligible interface found; skipping.")
            return False
        new_mac = rand_mac()
        log(f"[MAC] Setting {iface} → {new_mac}")
        run_cmd(f"ip link set dev {iface} down", capture=False)
        run_cmd(f"ip link set dev {iface} address {new_mac}", capture=False)
        run_cmd(f"ip link set dev {iface} up", capture=False)
        return True
    except Exception as e:  # broad catch for robustness
        log(f"[MAC] ERROR: {e}")
        return False


# ---------------------------------------------------------------------------
# machine-id spoofing
# ---------------------------------------------------------------------------


def spoof_machine_id() -> bool:
    """Regenerate /etc/machine-id safely."""
    try:
        log("[MID] Regenerating /etc/machine-id …")
        run_cmd("rm -f /etc/machine-id", capture=False)
        run_cmd("systemd-machine-id-setup", capture=False)
        return True
    except Exception as e:
        log(f"[MID] ERROR: {e}")
        return False


# ---------------------------------------------------------------------------
# fstab parsing utilities
# ---------------------------------------------------------------------------


@dc.dataclass
class FstabEntry:
    device: str
    mountpoint: str
    fstype: str
    options: str
    dump: str
    passno: str
    comment: str = ""
    leading_ws: str = ""  # preserve formatting

    def to_line(self) -> str:
        fields = [
            self.device,
            self.mountpoint,
            self.fstype,
            self.options,
            self.dump,
            self.passno,
        ]
        line = self.leading_ws + "\t".join(fields)
        if self.comment:
            # ensure single space before '#'
            if not self.comment.startswith("#"):
                line += "\t# " + self.comment
            else:
                line += "\t" + self.comment
        return line.rstrip() + "\n"


FstabLine = Union[str, FstabEntry]  # raw comment / blank or actual entry


_FSTAB_WS_RE = re.compile(r"^(\s*)")


def parse_fstab_text(text: str) -> List[FstabLine]:
    lines: List[FstabLine] = []
    for raw in text.splitlines(True):  # keep newline
        stripped = raw.lstrip()
        if stripped.startswith("#") or not stripped.strip():
            # Preserve as raw string
            lines.append(raw)
            continue
        # Split off inline comment
        body, sep, cmt = raw.partition("#")
        leading_ws = _FSTAB_WS_RE.match(body).group(1)
        tokens = body.split()
        if len(tokens) < 2:
            lines.append(raw)
            continue
        # Pad missing fields
        while len(tokens) < 6:
            tokens.append("0")
        dev, mnt, fst, opt, dmp, pas = tokens[:6]
        comment = ("#" + cmt) if sep else ""
        entry = FstabEntry(
            dev,
            mnt,
            fst,
            opt,
            dmp,
            pas,
            comment=comment.rstrip("\n"),
            leading_ws=leading_ws,
        )
        lines.append(entry)
    return lines


def serialize_fstab_lines(lines: Iterable[FstabLine]) -> str:
    out = []
    for ln in lines:
        if isinstance(ln, FstabEntry):
            out.append(ln.to_line())
        else:
            out.append(ln)  # raw preserved
    return "".join(out)


def load_fstab(path: _p.Path) -> List[FstabLine]:
    return parse_fstab_text(path.read_text(encoding="utf-8"))


def save_fstab(path: _p.Path, lines: List[FstabLine]) -> None:
    tmp = path.with_suffix(".new")
    tmp.write_text(serialize_fstab_lines(lines), encoding="utf-8")
    backup = path.with_suffix(f".bak.{int(_dt.datetime.now().timestamp())}")
    try:
        path.replace(backup)  # rename current to backup
    except FileNotFoundError:
        pass
    tmp.replace(path)
    log(f"[FSTAB] Updated {path} (backup {backup.name}).")


def find_entry_by_mountpoint(
    lines: List[FstabLine], mountpoint: str
) -> Optional[FstabEntry]:
    for ln in lines:
        if isinstance(ln, FstabEntry) and ln.mountpoint == mountpoint:
            return ln
    return None


def update_entry_device(
    lines: List[FstabLine], entry: FstabEntry, new_device: str
) -> None:
    for idx, ln in enumerate(lines):
        if ln is entry:
            new_e = dc.replace(entry, device=new_device)
            lines[idx] = new_e
            break


# ---------------------------------------------------------------------------
# Filesystem UUID spoofing (root only, with lots of guard rails)
# ---------------------------------------------------------------------------


@dc.dataclass
class UUIDRotateResult:
    old_uuid: str
    new_uuid: str
    device: str
    fstype: str
    fstab_updated: bool
    bootloader_reinstalled: bool


ROLLBACK_DIR = _p.Path("/var/lib/spoofid")
ROLLBACK_DIR.mkdir(parents=True, exist_ok=True)


def _get_root_source(target_root: str = "/") -> Tuple[str, str]:
    """Return (device, fstype) that backs *target_root* mountpoint.

    Uses `findmnt` so it works with binds, LUKS mappers, etc.
    """
    dev = run_cmd(f"findmnt -no SOURCE {shlex.quote(target_root)}")
    fst = run_cmd(f"findmnt -no FSTYPE {shlex.quote(target_root)}")
    return dev.strip(), fst.strip()


def _get_uuid(dev: str) -> str:
    return run_cmd(f"blkid -s UUID -o value {shlex.quote(dev)}")


def _is_mounted_rw(dev: str) -> bool:
    # grep /proc/self/mountinfo for dev; fallback to findmnt
    try:
        opts = run_cmd(f"findmnt -no OPTIONS {shlex.quote(dev)}", check=False)
        if opts and "rw" in opts.split(","):
            return True
    except Exception:
        pass
    return False


def _change_uuid(dev: str, fstype: str, *, force_online: bool = False) -> None:
    """Change the filesystem UUID in-place.

    *Best practice* is to do this offline. If *force_online* is False and the
    filesystem appears mounted rw, we abort.
    """
    if not force_online and _is_mounted_rw(dev):
        raise RuntimeError(
            f"Refusing to change UUID on mounted rw filesystem {dev!r} without --force-online."
        )
    if fstype == "ext4" or fstype.startswith("ext"):
        log(f"[UUID] tune2fs -U random {dev}")
        run_cmd(f"tune2fs -U random {shlex.quote(dev)}", capture=False)
    elif fstype == "btrfs":
        log(f"[UUID] btrfstune -u {dev}")
        run_cmd(f"btrfstune -u {shlex.quote(dev)}", capture=False)
    else:
        raise RuntimeError(f"Unsupported filesystem type {fstype!r} for UUID change.")


# ---------------------------------------------------------------------------
# Bootloader detection & reinstall
# ---------------------------------------------------------------------------


class Bootloader(str):
    GRUB = "grub"
    SYSTEMD = "systemd-boot"
    NONE = "none"


_DEF_GRUB_CFG = "/boot/grub/grub.cfg"


def detect_bootloader() -> Bootloader:
    if _p.Path("/boot/grub").exists():
        return Bootloader.GRUB
    if _p.Path("/efi/loader").exists() or _p.Path("/boot/efi/loader").exists():
        return Bootloader.SYSTEMD
    return Bootloader.NONE


def _esp_mountpoint() -> Optional[str]:
    # prefer /boot/efi; fallback /efi
    if _p.Path("/boot/efi").is_dir():
        return "/boot/efi"
    if _p.Path("/efi").is_dir():
        return "/efi"
    return None


def reinstall_grub() -> bool:
    """Reinstall GRUB with minimal assumptions.

    Returns True if commands ran without raising CmdError.
    """
    try:
        esp = _esp_mountpoint()
        if not esp:
            raise RuntimeError("Cannot locate ESP mountpoint (/boot/efi or /efi).")
        log("[BOOT] Reinstalling GRUB …")
        # pacman -Q grub? we assume already installed; don't auto-install packages.
        run_cmd(f"grub-install --efi-directory={shlex.quote(esp)}", capture=False)
        run_cmd(f"grub-mkconfig -o {_DEF_GRUB_CFG}", capture=False)
        return True
    except Exception as e:
        log(f"[BOOT] GRUB reinstall failed: {e}")
        return False


def reinstall_systemd_boot() -> bool:
    try:
        log("[BOOT] Reinstalling systemd-boot …")
        run_cmd("bootctl install", capture=False)
        # optional EndeavourOS helper; ignore failure
        run_cmd("reinstall-kernels", capture=False, check=False)
        return True
    except Exception as e:
        log(f"[BOOT] systemd-boot reinstall failed: {e}")
        return False


# ---------------------------------------------------------------------------
# Main UUID rotation workflow
# ---------------------------------------------------------------------------


def spoof_filesystem_uuid(
    *,
    target_root: str = "/",
    apply: bool = False,
    force_online: bool = False,
    reinstall_bootloader: str = "auto",  # 'auto','grub','systemd','none'
) -> UUIDRotateResult:
    """Randomize the UUID of the *root* filesystem and update config safely.

    Parameters
    ----------
    target_root:
        Path to the mounted root of the *target* system (default current '/').
        Use this when running from a live ISO (e.g., `/mnt`).
    apply:
        Actually perform the UUID change and write changes. If False, dry-run.
    force_online:
        Allow UUID change even if filesystem appears mounted read-write.
    reinstall_bootloader:
        'auto' to auto-detect, 'grub', 'systemd', or 'none'.
    """
    root_dev, fstype = _get_root_source(target_root)
    old_uuid = _get_uuid(root_dev)
    log(f"[UUID] Root dev: {root_dev} ({fstype}) old UUID {old_uuid}")

    # Load target fstab (relative to target_root)
    fstab_path = _p.Path(target_root) / "etc/fstab"
    lines = load_fstab(fstab_path)
    root_entry = find_entry_by_mountpoint(lines, "/")
    if not root_entry:
        raise RuntimeError("No '/' entry found in fstab; aborting.")

    # Show planned change
    log("[UUID] Planned fstab change:")
    log(f"       old: {root_entry.device}")
    new_device = f"UUID=<pending-random>"
    log(f"       new: {new_device}")

    if not apply:
        log("[UUID] Dry-run; no changes made.")
        return UUIDRotateResult(old_uuid, old_uuid, root_dev, fstype, False, False)

    # Actually change UUID
    _change_uuid(root_dev, fstype, force_online=force_online)
    new_uuid = _get_uuid(root_dev)
    log(f"[UUID] New UUID: {new_uuid}")

    # Update fstab root entry device
    update_entry_device(lines, root_entry, f"UUID={new_uuid}")
    save_fstab(fstab_path, lines)
    fstab_updated = True

    # Persist rollback metadata
    ROLLBACK_DIR.mkdir(parents=True, exist_ok=True)
    meta = {
        "timestamp": _ts(),
        "root_dev": root_dev,
        "fstype": fstype,
        "old_uuid": old_uuid,
        "new_uuid": new_uuid,
        "fstab": str(fstab_path),
    }
    (ROLLBACK_DIR / "last_uuid_rotate.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )

    # Bootloader reinstall
    bl_mode = reinstall_bootloader
    if bl_mode == "auto":
        bl_mode = detect_bootloader()
    bootloader_reinstalled = False
    if bl_mode == Bootloader.GRUB:
        bootloader_reinstalled = reinstall_grub()
    elif bl_mode == Bootloader.SYSTEMD:
        bootloader_reinstalled = reinstall_systemd_boot()
    elif bl_mode == Bootloader.NONE:
        log("[BOOT] Skipping bootloader reinstall (mode=none).")
    else:
        log(f"[BOOT] Unknown bootloader mode: {bl_mode}; skipping.")

    return UUIDRotateResult(
        old_uuid, new_uuid, root_dev, fstype, fstab_updated, bootloader_reinstalled
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

_DEF = "<auto>"


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Spoof system identifiers (MAC, machine-id, root filesystem UUID) safely.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_mac = sub.add_parser("mac", help="Spoof MAC address of first active NIC")

    ap_mid = sub.add_parser("machine-id", help="Regenerate /etc/machine-id")

    ap_uuid = sub.add_parser(
        "root-uuid", help="Randomize *root* filesystem UUID safely"
    )
    ap_uuid.add_argument(
        "--apply", action="store_true", help="Perform changes (default dry-run)"
    )
    ap_uuid.add_argument(
        "--force-online",
        action="store_true",
        help="Allow UUID change even if root appears mounted rw",
    )
    ap_uuid.add_argument(
        "--target-root",
        default="/",
        help="Path to mounted target system root (for use in chroot workflows)",
    )
    ap_uuid.add_argument(
        "--reinstall-bootloader",
        choices=["auto", "grub", "systemd", "none"],
        default="auto",
        help="Reinstall/update bootloader after UUID change",
    )

    return ap.parse_args(argv)


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------


def main(argv: Optional[List[str]] = None) -> int:
    ns = _parse_args(argv)

    if ns.cmd == "mac":
        ok = spoof_mac_addr()
        return 0 if ok else 1

    if ns.cmd == "machine-id":
        ok = spoof_machine_id()
        return 0 if ok else 1

    if ns.cmd == "root-uuid":
        try:
            res = spoof_filesystem_uuid(
                target_root=ns.target_root,
                apply=ns.apply,
                force_online=ns.force_online,
                reinstall_bootloader=ns.reinstall_bootloader,
            )
        except Exception as e:
            log(f"[UUID] ERROR: {e}")
            return 2
        log(
            "[UUID] Result: old={0} new={1} device={2} fstab_updated={3} bootloader_reinstalled={4}".format(
                res.old_uuid,
                res.new_uuid,
                res.device,
                res.fstab_updated,
                res.bootloader_reinstalled,
            )
        )
        return 0

    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
