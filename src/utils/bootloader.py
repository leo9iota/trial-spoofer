def update_boot_loader() -> bool:
    """
    Update boot loader configuration.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    try:
        run_cmd("update-grub", capture=False, timeout=60.0)
        run_cmd("update-initramfs -u", capture=False, timeout=120.0)
        return True
    except (CmdError, subprocess.TimeoutExpired):
        return False
