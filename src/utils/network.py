import sys

from ..core.command import CmdError, run_cmd
from .mac import validate_mac_address


def get_network_interfaces() -> dict[str, dict[str, str]]:
    """Get information about available network interfaces.

    Returns
    -------
    dict[str, dict[str, str]]
        Dictionary mapping interface names to their properties.
        Each interface dict contains: 'mac', 'state', 'type'
    """
    interfaces = {}

    try:
        # Get interface information
        result = run_cmd("ip -o link show", timeout=10)
        lines = result.strip().split("\n")

        for line in lines:
            if ":" not in line:
                continue

            parts = line.split(":")
            if len(parts) < 3:
                continue

            # Extract interface name (remove @ suffix if present)
            iface_name = parts[1].strip().split("@")[0]

            # Skip loopback
            if iface_name == "lo" or "LOOPBACK" in line:
                continue

            # Extract MAC address
            mac = "Unknown"
            if "link/ether" in line:
                mac_part = line.split("link/ether")[1].split()[0]
                if validate_mac_address(mac_part):
                    mac = mac_part

            # Extract state
            state = "DOWN"
            if "state UP" in line:
                state = "UP"
            elif "state DOWN" in line:
                state = "DOWN"
            elif "state UNKNOWN" in line:
                state = "UNKNOWN"

            # Determine interface type
            iface_type = "ethernet"
            if "link/ether" in line:
                iface_type = "ethernet"
            elif "link/none" in line:
                iface_type = "virtual"
            elif "link/sit" in line:
                iface_type = "tunnel"

            interfaces[iface_name] = {"mac": mac, "state": state, "type": iface_type}

    except (CmdError, Exception) as e:
        print(f"Error getting network interfaces: {e}", file=sys.stderr)

    return interfaces


def get_eligible_network_interfaces() -> list[str]:
    """
    Get list of interfaces eligible for MAC spoofing.

    Returns
    -------
    list[str]
        List of interface names that can be used for MAC spoofing.
        Excludes loopback and virtual interfaces.
    """
    interfaces = get_network_interfaces()
    eligible = []

    for name, info in interfaces.items():
        # Skip virtual interfaces and those without proper MAC addresses
        if (
            info["type"] == "ethernet"
            and info["mac"] != "Unknown"
            and validate_mac_address(info["mac"])
        ):
            eligible.append(name)

    return eligible


def get_interface_info(interface_name: str) -> dict[str, str] | None:
    """Get detailed information about a specific network interface.
    
    Parameters
    ----------
    interface_name : str
        Name of the interface to query.
        
    Returns
    -------
    dict[str, str] | None
        Interface information dict or None if not found.
    """
    interfaces = get_network_interfaces()
    return interfaces.get(interface_name)


def is_interface_up(interface_name: str) -> bool:
    """Check if a network interface is UP.
    
    Parameters
    ----------
    interface_name : str
        Name of the interface to check.
        
    Returns
    -------
    bool
        True if interface is UP, False otherwise.
    """
    info = get_interface_info(interface_name)
    return info is not None and info.get("state") == "UP"
