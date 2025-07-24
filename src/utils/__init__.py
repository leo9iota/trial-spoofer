"""Utility functions organized by category."""

from .check import (
    check_root,
    check_system_requirements,
    get_missing_commands,
    is_linux,
    get_current_user,
)
from .identifiers import (
    get_identifiers,
    get_mac_address,
    get_machine_id,
    get_filesystem_uuid,
    get_hostname,
)
from .mac import get_random_mac_address, validate_mac_address, normalize_mac_address
from .network import (
    get_network_interfaces,
    get_eligible_network_interfaces,
    get_interface_info,
    is_interface_up,
)
from .hostname import change_hostname
from .bootloader import update_boot_loader
from .account import create_new_user, delete_user, user_exists

__all__ = [
    # System checks
    "check_root",
    "check_system_requirements",
    "get_missing_commands",
    "is_linux",
    "get_current_user",
    # Identifiers
    "get_identifiers",
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
    "create_new_user",
    "delete_user",
    "user_exists",
]