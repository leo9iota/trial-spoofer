#!/usr/bin/env python3

"""
Command Class

Run Linux shell commands.
"""

import shlex
import subprocess


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
        check: bool = True,
        capture_output: bool = True,
        silent: bool = False,
        unchecked: bool = False,
    ) -> str | bool | tuple[int, str, str]:
        """
        Execute a shell command with configurable behavior.

        Args:
            command: The shell command to execute
            check: Whether to raise CommandError on non-zero exit codes
            (ignored if silent or unchecked)
            capture_output: Whether to capture stdout/stderr
            silent: If True, return boolean success/failure instead of output
            unchecked: If True, return (return_code, stdout, stderr) tuple without
            exceptions

        Returns:
            - str: stdout output (default behavior)
            - bool: success status (if silent=True)
            - tuple[int, str, str]: (return_code, stdout, stderr) (if unchecked=True)

        Raises:
            CommandError: If the command fails and check=True (unless silent or unchecked)
            subprocess.TimeoutExpired: If the command times out
            (unless silent or unchecked)
        """
        try:
            if self.shell:
                # Run through shell for complex commands with pipes, etc.
                result: subprocess.CompletedProcess[str] = subprocess.run(
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
            if unchecked:
                # Return all information without exceptions
                return result.returncode, result.stdout, result.stderr

            if silent:
                # Return boolean success/failure
                return result.returncode == 0

            # Default behavior: check for errors and return stdout
            if check and result.returncode != 0:
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
            if unchecked:
                return -1, "", "Command timed out"
            if silent:
                return False
            # Re-raise timeout exceptions with additional context for default behavior
            raise subprocess.TimeoutExpired(
                cmd=command,
                timeout=float(self.timeout or 30),
                output=e.output,
                stderr=e.stderr,
            ) from e
        except FileNotFoundError as e:
            if unchecked:
                return -1, "", f"Command not found: {str(e)}"
            if silent:
                return False
            # Handle cases where the command/executable doesn't exist
            raise CommandError(
                failed_command=command,
                return_code=-1,
                stdout="",
                stderr=f"Command not found: {str(e)}",
            ) from e
