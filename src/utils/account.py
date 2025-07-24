import random
import subprocess

from ..core.command import CmdError, run_cmd


def create_user_account(custom_username: str | None = None) -> bool:
    """
    Create a new user account.

    Parameters
    ----------
    custom_username : str | None
        Custom username to create. If None, uses 'vscode_sandbox'.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    try:
        user: str = custom_username if custom_username else "vscode_sandbox"

        # Check if user already exists using our improved run_cmd
        try:
            run_cmd(f"id -u {user}", capture=False)
            # User exists, no need to create
            return True
        except CmdError:
            # User doesn't exist, create it
            random_number: int = random.randint(10000, 99999)
            pw: str = f"Vs@{random_number}"

            run_cmd(f"useradd -m {user}", capture=False)
            # Use stdin input for password instead of shell command for security
            run_cmd("chpasswd", input=f"{user}:{pw}".encode(), capture=False)
            return True
    except (CmdError, subprocess.TimeoutExpired):
        return False


def create_user_password():
    print("user password")

def delete_user_account(username: str, remove_home: bool = True) -> bool:
    """
    Delete a user account.

    Parameters
    ----------
    username : str
        Username to delete.
    remove_home : bool, optional
        Whether to remove the user's home directory.

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    try:
        if remove_home:
            run_cmd(f"userdel -r {username}", capture=False)
        else:
            run_cmd(f"userdel {username}", capture=False)
        return True
    except (CmdError, subprocess.TimeoutExpired):
        return False


def user_exists(username: str) -> bool:
    """
    Check if a user exists.

    Parameters
    ----------
    username : str
        Username to check.

    Returns
    -------
    bool
        True if user exists, False otherwise.
    """
    try:
        run_cmd(f"id {username}")
        return True
    except CmdError:
        return False
