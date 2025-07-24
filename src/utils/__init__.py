"""Utility functions organized by category."""

from .account import (
    create_user_account,
    create_user_password,
    delete_user_account,
    user_exists,
)
from .bootloader import update_boot_loader
from .helpers import (
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
    get_network_interface_info,
    get_network_interfaces,
    is_interface_up,
)
from .parser import ARGS_DESCRIPTION, parse_args

__all__ = [
    # Account
    "create_user_account",
    "create_user_password",
    "delete_user_account",
    "user_exists",
    # Bootloader
    "update_boot_loader",
    # Helpers
    "check_root",
    "check_system_requirements",
    "get_current_user",
    "get_missing_commands",
    "is_linux",
    # Hostname
    "change_hostname",
    # Identifiers
    "get_filesystem_uuid",
    "get_hostname",
    "get_mac_address",
    "get_machine_id",
    "get_system_identifiers",
    # MAC Address
    "get_random_mac_address",
    "normalize_mac_address",
    "validate_mac_address",
    # Network
    "get_eligible_network_interfaces",
    "get_network_interface_info",
    "get_network_interfaces",
    "is_interface_up",
    # Args Parser
    "ARGS_DESCRIPTION",
    "parse_args",
]
