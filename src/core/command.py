#!/usr/bin/env python3
"""
Command execution utilities.

This module provides robust command execution functionality with enhanced
error handling, security features, and process management capabilities.
"""

from __future__ import annotations

import shlex
import subprocess
from typing import Optional


class CmdError(RuntimeError):
    """
    Custom exception for command execution failures.

    Attributes
    ----------
    cmd : str
        The command that failed.
    rc : int
        The return code of the failed command.
    out : str
        The stdout output from the command.
    err : str
        The stderr output from the command.
    """

    def __init__(self, cmd: str, rc: int, out: str, err: str):
        self.cmd = cmd
        self.rc = rc
        self.out = out
        self.err = err
        super().__init__(f"Command failed ({rc}): {cmd}\nSTDOUT: {out}\nSTDERR: {err}")


def run_cmd(
    cmd: str,
    *,
    capture: bool = True,
    check: bool = True,
    shell: bool = False,
    env: Optional[dict] = None,
    input: Optional[bytes] = None,
    timeout: Optional[float] = None,
    cwd: Optional[str] = None,
) -> str:
    """
    Run a shell command with enhanced features and error handling.

    Parameters
    ----------
    cmd : str
        The command to run. If *shell* is False (default), the string will be
        split via shlex.split for better security.
    capture : bool, default=True
        If True, capture stdout+stderr and return stdout.
    check : bool, default=True
        If True, raise CmdError on non-zero exit.
    shell : bool, default=False
        Pass through to subprocess.run. Use with caution for security.
    env : dict | None, optional
        Extra environment variables to merge with current environment.
    input : bytes | None, optional
        Data to pass on stdin.
    timeout : float | None, optional
        Timeout in seconds for command execution.
    cwd : str | None, optional
        Working directory for command execution.

    Returns
    -------
    str
        Command stdout if capture=True, empty string otherwise.

    Raises
    ------
    CmdError
        If check=True and command returns non-zero exit code.
    subprocess.TimeoutExpired
        If timeout is exceeded.

    Examples
    --------
    >>> # Basic usage
    >>> output = run_cmd("echo hello")
    >>> print(output)  # "hello"

    >>> # With environment variables
    >>> output = run_cmd("echo $MY_VAR", env={"MY_VAR": "test"}, shell=True)

    >>> # With timeout
    >>> run_cmd("sleep 1", timeout=0.5)  # Raises TimeoutExpired

    >>> # With stdin input
    >>> output = run_cmd("cat", input=b"hello world")
    """
    if shell:
        args = cmd
    else:
        args = shlex.split(cmd)

    # Merge environment variables if provided
    final_env = None
    if env:
        import os

        final_env = {**os.environ, **env}

    try:
        proc = subprocess.run(
            args,
            input=input,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.PIPE if capture else None,
            env=final_env,
            shell=shell,
            text=True,
            check=False,
            timeout=timeout,
            cwd=cwd,
        )
    except subprocess.TimeoutExpired as e:
        # Re-raise timeout with more context
        raise subprocess.TimeoutExpired(
            cmd=cmd,
            timeout=timeout,
            output=getattr(e, "output", None),
            stderr=getattr(e, "stderr", None),
        ) from e

    out = proc.stdout or ""
    err = proc.stderr or ""

    if check and proc.returncode != 0:
        raise CmdError(cmd, proc.returncode, out, err)

    return out.strip() if capture else ""
