import os
import platform
import sys
from pathlib import Path

from core.command import CmdError, run_cmd


def get_current_username() -> str:
    """Get current username.

    Returns
    -------
    str
        Current username.
    """
    return os.environ.get("SUDO_USER") or os.environ.get("USER") or "root"


def get_missing_commands() -> list[str]:
    """Get list of missing required system commands.

    Returns
    -------
    list[str]
        List of missing command names.
    """
    required_commands = ["ip", "systemctl", "hostnamectl"]
    missing_commands = []

    for cmd in required_commands:
        try:
            run_cmd(f"which {cmd}")
        except CmdError:
            missing_commands.append(cmd)

    return missing_commands


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

        missing_commands = get_missing_commands()
        return len(missing_commands) == 0

    except Exception as e:
        print(f"Error checking system requirements: {e}", file=sys.stderr)
        return False


def is_linux() -> bool:
    """Check if running on Linux.

    Returns
    -------
    bool
        True if running on Linux, False otherwise.
    """
    return platform.system() == "Linux"
