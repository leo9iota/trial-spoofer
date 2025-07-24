#!/usr/bin/env python3

"""
Command Class

Run Linux shell commands.
"""


class CommandError(RuntimeError):
    """
    Exception for shell command failures.

    Parameters
        str   failed_command   Command that failed.
        int   return_code      Return code of the failed command.
        str   stdout           Output from stdout.
        str   stderr           Output from stderr.

    Return
        void
    """

    def __init__(self, failed_command: str, return_code: int, stdout: str, stderr: str):
        self.failed_command = failed_command
        self.return_code = return_code
        self.stdout = stdout
        self.stderr = stderr

class Command:

    
    """
    Run shell commands with error handling.

    Parameters
        str                      command     Shell command to run.
        bool, default=True       capture     Capture output stdout and stderr and return stdout.
        bool, default=True       check       Raise CommandError if return code is not 0.
        bytes | None, optional   input       Data to be passed to stdin.
        str | None, optional     directory   Directory to run command from.
        float | None, optional   timeout     Timeout in seconds for command execution.

    Return
        str   stdout   Command stdout if capture=True

    Raise
        CommandError                If check=True and the command returns a non-zero exit code.
        subprocess.TimeoutExpired   If timeout is exceeded.
    """
    Linux shell command execution utilities.

    Provides specialized methods for common Linux operations and shell command patterns.
    Optimized for Linux environments with bash/sh compatibility.
    """

    @staticmethod
    def run(cmd: str, **kwargs) -> str:
        """Execute a shell command with Linux-optimized defaults."""
        # Default to shell=True for Linux since we want full shell features
        kwargs.setdefault("shell", True)
        return run_cmd(cmd, **kwargs)

    @staticmethod
    def pipe(*commands: str, **kwargs) -> str:
        """
        Execute a pipeline of commands connected with pipes.

        Examples
        --------
        >>> LinuxShell.pipe("ps aux", "grep python", "wc -l")
        >>> LinuxShell.pipe("cat /proc/cpuinfo", "grep processor", "wc -l")
        """
        pipeline = " | ".join(commands)
        return LinuxShell.run(pipeline, **kwargs)

    @staticmethod
    def sudo(cmd: str, **kwargs) -> str:
        """Execute a command with sudo privileges."""
        return LinuxShell.run(f"sudo {cmd}", **kwargs)

    @staticmethod
    def which(program: str) -> Optional[str]:
        """
        Find the path to an executable program.

        Returns None if program is not found in PATH.
        """
        try:
            result = LinuxShell.run(f"which {shlex.quote(program)}")
            return result.strip() if result else None
        except CmdError:
            return None

    @staticmethod
    def exists(path: str) -> bool:
        """Check if a file or directory exists."""
        try:
            LinuxShell.run(f"test -e {shlex.quote(path)}")
            return True
        except CmdError:
            return False

    @staticmethod
    def is_file(path: str) -> bool:
        """Check if path is a regular file."""
        try:
            LinuxShell.run(f"test -f {shlex.quote(path)}")
            return True
        except CmdError:
            return False

    @staticmethod
    def is_dir(path: str) -> bool:
        """Check if path is a directory."""
        try:
            LinuxShell.run(f"test -d {shlex.quote(path)}")
            return True
        except CmdError:
            return False

    @staticmethod
    def get_env(var: str, default: Optional[str] = None) -> Optional[str]:
        """Get an environment variable value."""
        try:
            result = LinuxShell.run(f"echo ${{{shlex.quote(var)}}}")
            return result if result else default
        except CmdError:
            return default

    @staticmethod
    def ps_grep(pattern: str) -> str:
        """Find processes matching a pattern."""
        return LinuxShell.pipe("ps aux", f"grep '{pattern}'", "grep -v grep")

    @staticmethod
    def kill_by_name(process_name: str, signal: str = "TERM") -> str:
        """Kill processes by name using pkill."""
        return LinuxShell.run(f"pkill -{signal} {shlex.quote(process_name)}")

    @staticmethod
    def disk_usage(path: str = ".") -> str:
        """Get disk usage for a path."""
        return LinuxShell.run(f"du -sh {shlex.quote(path)}")

    @staticmethod
    def free_space(path: str = ".") -> str:
        """Get free disk space for filesystem containing path."""
        return LinuxShell.run(f"df -h {shlex.quote(path)}")

    @staticmethod
    def find_files(pattern: str, path: str = ".", type_filter: str = "f") -> str:
        """
        Find files matching a pattern.

        Parameters
        ----------
        pattern : str
            Filename pattern (supports wildcards)
        path : str, default="."
            Directory to search in
        type_filter : str, default="f"
            File type: 'f' for files, 'd' for directories, 'l' for links
        """
        return LinuxShell.run(
            f"find {shlex.quote(path)} -type {type_filter} -name {shlex.quote(pattern)}"
        )

    @staticmethod
    def grep_files(pattern: str, path: str = ".", file_pattern: str = "*") -> str:
        """Search for text pattern in files."""
        return LinuxShell.run(
            f"grep -r {shlex.quote(pattern)} {shlex.quote(path)} --include={shlex.quote(file_pattern)}"
        )

    @staticmethod
    def tail_follow(file_path: str, lines: int = 10) -> None:
        """
        Follow a log file (like tail -f).

        Note: This runs indefinitely until interrupted.
        """
        LinuxShell.run(f"tail -f -n {lines} {shlex.quote(file_path)}", capture=False)

    @staticmethod
    def systemctl(action: str, service: str) -> str:
        """Control systemd services."""
        return LinuxShell.run(f"systemctl {action} {shlex.quote(service)}")

    @staticmethod
    def service_status(service: str) -> str:
        """Get systemd service status."""
        return LinuxShell.systemctl("status", service)

    @staticmethod
    def start_service(service: str) -> str:
        """Start a systemd service."""
        return LinuxShell.systemctl("start", service)

    @staticmethod
    def stop_service(service: str) -> str:
        """Stop a systemd service."""
        return LinuxShell.systemctl("stop", service)

    @staticmethod
    def restart_service(service: str) -> str:
        """Restart a systemd service."""
        return LinuxShell.systemctl("restart", service)


def run_cmd(
    cmd: str,
    *,
    capture: bool = True,
    check: bool = True,
    shell: bool = False,
    env: dict | None = None,
    input: bytes | None = None,
    timeout: float | None = None,
    cwd: str | None = None,
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
