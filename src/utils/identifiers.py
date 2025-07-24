from ..core.command import CmdError, run_cmd


def get_system_identifiers() -> dict[str, str]:
    """Get current system identifiers.

    Returns
    -------
    dict[str, str]
        Dictionary mapping identifier names to their current values.
    """
    identifiers = {}

    try:
        # MAC Address (first active interface)
        result = run_cmd("ip link show", timeout=5)
        lines = result.split("\n")
        for line in lines:
            if "link/ether" in line and "state UP" in lines[lines.index(line) - 1]:
                mac = line.split("link/ether")[1].split()[0]
                identifiers["MAC Address"] = mac
                break
        if "MAC Address" not in identifiers:
            identifiers["MAC Address"] = "Not found"
    except (CmdError, Exception):
        identifiers["MAC Address"] = "Not found"

    try:
        # Machine ID
        with open("/etc/machine-id") as f:
            identifiers["Machine ID"] = f.read().strip()
    except Exception:
        identifiers["Machine ID"] = "Not found"

    try:
        # Filesystem UUID (root partition)
        result = run_cmd("findmnt -n -o UUID /", timeout=5)
        identifiers["Filesystem UUID"] = result
    except (CmdError, Exception):
        identifiers["Filesystem UUID"] = "Not found"

    try:
        # Hostname
        with open("/etc/hostname") as f:
            identifiers["Hostname"] = f.read().strip()
    except Exception:
        try:
            result = run_cmd("hostname", timeout=5)
            identifiers["Hostname"] = result
        except (CmdError, Exception):
            identifiers["Hostname"] = "Not found"

    return identifiers


def get_mac_address() -> str:
    """Get MAC address of the first active interface.

    Returns
    -------
    str
        MAC address or "Not found" if unavailable.
    """
    identifiers = get_system_identifiers()
    return identifiers.get("MAC Address", "Not found")


def get_machine_id() -> str:
    """Get system machine ID.

    Returns
    -------
    str
        Machine ID or "Not found" if unavailable.
    """
    identifiers = get_system_identifiers()
    return identifiers.get("Machine ID", "Not found")


def get_filesystem_uuid() -> str:
    """Get root filesystem UUID.

    Returns
    -------
    str
        Filesystem UUID or "Not found" if unavailable.
    """
    identifiers = get_system_identifiers()
    return identifiers.get("Filesystem UUID", "Not found")


def get_hostname() -> str:
    """Get system hostname.

    Returns
    -------
    str
        Hostname or "Not found" if unavailable.
    """
    identifiers = get_system_identifiers()
    return identifiers.get("Hostname", "Not found")
