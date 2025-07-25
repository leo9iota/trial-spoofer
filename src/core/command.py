#!/usr/bin/env python3

"""
Command Class

Run Linux shell commands.
"""

import shlex
import subprocess
from enum import Enum


class ReturnMode(Enum):
    """Return mode for command execution."""

    RAISE_ON_ERROR = "raise"  # Default: raise exceptions on error
    SILENT = "silent"  # Return bool success/failure
    RAW = "raw"  # Return (code, stdout, stderr) tuple


class CommandError(RuntimeError):
    """
    Exception for shell command failures.

    Args:
        failed_command: Command that failed.
        return_code: Return code of the failed command.
        stdout: Output from stdout.
        stderr: Output from stderr.

    Returns:
        None
    """

    def __init__(
        self, failed_command: str, return_code: int, stdout: str, stderr: str
    ) -> None:
        self.failed_command = failed_command
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr
        super().__init__(
            f"Command '{failed_command}' failed with return code {return_code}"
        )


class Command:
    """
    Run Linux shell commands.
    """

    def __init__(self, timeout: float | None = 30.0, shell: bool = True) -> None:
        """
        Initialize the Command class.

        Args:
            timeout: Maximum time in seconds to wait for command completion
            shell: Whether to run commands through shell (enables pipes, redirects, etc.)
        """
        self.timeout = timeout
        self.shell = shell

    def run(
        self,
        command: str,
        mode: ReturnMode = ReturnMode.RAISE_ON_ERROR,
        capture_output: bool = True,
    ) -> str | bool | tuple[int, str, str]:
        """
        Execute a shell command with configurable behavior.

        Args:
            command: The shell command to execute
            mode: How to handle command results and errors:
                - RAISE_ON_ERROR: Raise CommandError on non-zero exit (default)
                - SILENT: Return boolean success/failure
                - RAW: Return (return_code, stdout, stderr) tuple
            capture_output: Whether to capture stdout/stderr

        Returns:
            - str: stdout output (if mode=RAISE_ON_ERROR)
            - bool: success status (if mode=SILENT)
            - tuple[int, str, str]: (return_code, stdout, stderr) (if mode=RAW)

        Raises:
            CommandError: If the command fails and mode=RAISE_ON_ERROR
            subprocess.TimeoutExpired: If the command times out and mode=RAISE_ON_ERROR
        """
        try:
            if self.shell:
                # Run through shell for complex commands with pipes, etc.
                result = subprocess.run(
                    command,
                    shell=True,
                    timeout=self.timeout,
                    capture_output=capture_output,
                    text=True,
                    check=False,  # We'll handle checking manually
                )
            else:
                # Parse command into arguments for safer execution
                args = shlex.split(command)
                result = subprocess.run(
                    args,
                    timeout=self.timeout,
                    capture_output=capture_output,
                    text=True,
                    check=False,  # We'll handle checking manually
                )

            # Handle different return modes
            if mode == ReturnMode.RAW:
                # Return all information without exceptions
                return result.returncode, result.stdout, result.stderr

            if mode == ReturnMode.SILENT:
                # Return boolean success/failure
                return result.returncode == 0

            # RAISE_ON_ERROR mode: check for errors and return stdout
            if result.returncode != 0:
                stdout = result.stdout if capture_output else ""
                stderr = result.stderr if capture_output else ""
                raise CommandError(
                    failed_command=command,
                    return_code=result.returncode,
                    stdout=stdout,
                    stderr=stderr,
                )

            return result.stdout if capture_output else ""

        except subprocess.TimeoutExpired as e:
            if mode == ReturnMode.RAW:
                return -1, "", "Command timed out"
            if mode == ReturnMode.SILENT:
                return False
            # Re-raise timeout exceptions for RAISE_ON_ERROR mode
            raise subprocess.TimeoutExpired(
                cmd=command,
                timeout=float(self.timeout or 30),
                output=e.output,
                stderr=e.stderr,
            ) from e
        except FileNotFoundError as e:
            if mode == ReturnMode.RAW:
                return -1, "", f"Command not found: {str(e)}"
            if mode == ReturnMode.SILENT:
                return False
            # Handle cases where the command/executable doesn't exist
            raise CommandError(
                failed_command=command,
                return_code=-1,
                stdout="",
                stderr=f"Command not found: {str(e)}",
            ) from e
