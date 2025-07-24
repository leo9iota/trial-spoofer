"""
MAC module (mac.py)

Generates random MAC address, normalizes it, and then validates it. This modules is used
within the Spoof module (spoof.py).
"""

import random


def get_random_mac_address(*, locally_admin: bool = True, unicast: bool = True) -> str:
    """
    Generate a random MAC address.

    Parameters
    ----------
    locally_admin : bool, optional
        If True (default), set the locally administered bit (LAA).
        This indicates the MAC address is locally assigned rather than
        globally unique from the manufacturer.
    unicast : bool, optional
        If True (default), clear the multicast bit to ensure unicast addressing.

    Returns
    -------
    str
        A randomly generated MAC address in the format "xx:xx:xx:xx:xx:xx".

    Notes
    -----
    - Setting locally_admin=True sets bit 1 of the first octet (0x02)
    - Setting unicast=True clears bit 0 of the first octet (0xFE mask)
    - This ensures the generated MAC follows proper addressing conventions
    """
    first = random.randint(0, 255)

    if locally_admin:
        first |= 0x02  # Set LAA (Locally Administered Address) bit
    else:
        first &= ~0x02  # Clear LAA bit for globally unique addresses

    if unicast:
        first &= 0xFE  # Clear multicast bit for unicast addressing

    # Generate remaining 5 octets
    parts = [first] + [random.randint(0, 255) for _ in range(5)]

    return ":".join(f"{p:02x}" for p in parts)


def normalize_mac_address(mac: str) -> str:
    """
    Normalize MAC address to standard format.

    Parameters
    ----------
    mac : str
        MAC address string to normalize.

    Returns
    -------
    str
        Normalized MAC address in format "xx:xx:xx:xx:xx:xx".

    Raises
    ------
    ValueError
        If MAC address format is invalid.
    """
    if not validate_mac_address(mac):
        raise ValueError(f"Invalid MAC address format: {mac}")

    # Remove separators and convert to lowercase
    clean_mac = mac.replace(":", "").replace("-", "").lower()

    # Add colons every 2 characters
    return ":".join(clean_mac[i : i + 2] for i in range(0, 12, 2))


def validate_mac_address(mac: str) -> bool:
    """
    Validate MAC address format.

    Parameters
    ----------
    mac : str
        MAC address string to validate.

    Returns
    -------
    bool
        True if valid MAC address format, False otherwise.
    """
    import re

    # Match standard MAC address formats: xx:xx:xx:xx:xx:xx or xx-xx-xx-xx-xx-xx
    pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    return bool(re.match(pattern, mac))
