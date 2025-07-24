"""Core functionality for vscode-spoofer."""

from .command import CmdError, run_cmd
from .config import Config, get_config, reload_config
from .spoof import (
    spoof_filesystem_uuid,
    spoof_mac_address,
    spoof_machine_id,
    spoof_vscode,
)

__all__ = [
    # Command
    "CmdError",
    "run_cmd",
    # Config
    "Config",
    "get_config",
    "reload_config",
    # Spoof
    "spoof_filesystem_uuid",
    "spoof_mac_address",
    "spoof_machine_id",
    "spoof_vscode",
]
