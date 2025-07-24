"""Core functionality for vscode-spoofer."""

from .config import Config, get_config, reload_config
from ..utils import (
    check_root,
    check_system_requirements,
    get_system_identifiers,
    get_network_interfaces,
    rand_mac,
    validate_mac_address,
)
from .spoof import (
    get_eligible_interfaces,
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
    "get_system_identifiers",
    "get_network_interfaces",
    "rand_mac",
    "validate_mac_address",
    # Spoofer
    "get_eligible_interfaces",
    "spoof_filesystem_uuid",
    "spoof_mac_addr",
    "spoof_machine_id",
    "spoof_vscode",
    # System
    "change_hostname",
    "create_new_user",
]