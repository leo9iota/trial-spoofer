"""Utility functions organized by category."""

from .check import check_root, check_system_requirements
from .identifiers import get_system_identifiers
from .mac import rand_mac, validate_mac_address
from .network import get_network_interfaces

__all__ = [
    # System checks
    "check_root",
    "check_system_requirements",
    # Identifiers
    "get_system_identifiers",
    # MAC utilities
    "rand_mac", 
    "validate_mac_address",
    # Network utilities
    "get_network_interfaces",
]