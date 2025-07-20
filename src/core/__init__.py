"""Core functionality for vscode-spoofer."""

from .config import Config, get_config, reload_config
from .helpers import check_root, check_system_requirements, get_identifiers
from .spoofer import (
    spoof_filesystem_uuid,
    spoof_mac_addr,
    spoof_machine_id,
    spoof_vscode,
)
from .system import change_hostname, create_new_user

__all__ = [
    # Config
    "Config",
    "get_config",
    "reload_config",
    # Helpers
    "check_root",
    "check_system_requirements",
    "get_identifiers",
    # Spoofer
    "spoof_filesystem_uuid",
    "spoof_mac_addr",
    "spoof_machine_id",
    "spoof_vscode",
    # System
    "change_hostname",
    "create_new_user",
]