"""Utility functions organized by category."""

from .account import create_user_account, delete_user, user_exists
from .bootloader import update_boot_loader
from .check import (
    check_root,
    check_system_requirements,
    get_current_user,
    get_missing_commands,
    is_linux,
)
from .hostname import change_hostname
from .identifiers import (
    get_filesystem_uuid,
    get_hostname,
    get_mac_address,
    get_machine_id,
    get_system_identifiers,
)
from .mac import get_random_mac_address, normalize_mac_address, validate_mac_address
from .network import (
    get_eligible_network_interfaces,
    get_interface_info,
    get_network_interfaces,
    is_interface_up,
)

__all__ = [
    # System checks
    "check_root",
    "check_system_requirements",
    "get_missing_commands",
    "is_linux",
    "get_current_user",
    # Identifiers
    "get_system_identifiers",
    "get_mac_address",
    "get_machine_id",
    "get_filesystem_uuid",
    "get_hostname",
    # MAC utilities
    "get_random_mac_address",
    "validate_mac_address",
    "normalize_mac_address",
    # Network utilities
    "get_network_interfaces",
    "get_eligible_network_interfaces",
    "get_interface_info",
    "is_interface_up",
    # System management
    "change_hostname",
    "update_boot_loader",
    "create_user_account",
    "delete_user",
    "user_exists",
]
