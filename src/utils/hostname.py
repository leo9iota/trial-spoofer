def change_hostname(custom_hostname: str | None = None) -> bool:
    """
    Change system hostname.

    Parameters
    ----------
    custom_hostname : str | None
        Custom hostname to set. If None, generates a random sandbox hostname.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    try:
        if custom_hostname:
            new_host: str = custom_hostname
        else:
            random_number: int = random.randint(1000, 9999)
            new_host = f"sandbox-{random_number}"

        run_cmd(f"hostnamectl set-hostname {new_host}", capture=False)
        return True
    except (CmdError, subprocess.TimeoutExpired):
        return False
