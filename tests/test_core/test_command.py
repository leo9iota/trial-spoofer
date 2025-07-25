#!/usr/bin/env python3

"""
Tests for the Command class.
"""

import tempfile
from pathlib import Path

# Import the Command class from our core module
from src.core.command import Command, ReturnMode


class TestCommand:
    """Test class for Command functionality."""

    def test_mkdir_command(self) -> None:
        """
        Test that the mkdir command creates a directory successfully.

        This is a simple test that:
        1. Creates a Command instance
        2. Uses it to run 'mkdir' to create a directory
        3. Verifies the directory was created
        4. Cleans up by removing the directory
        """
        # Create a Command instance
        cmd = Command()

        # Create a temporary directory name for testing
        # Using tempfile.gettempdir() to get the system's temp directory
        test_dir = Path(tempfile.gettempdir()) / "test_mkdir_example"

        try:
            # Run the mkdir command
            # The command will create the directory specified by test_dir
            cmd.run(f"mkdir {test_dir}")

            # Check that the directory was actually created
            assert test_dir.exists(), f"Directory {test_dir} was not created"
            assert test_dir.is_dir(), f"{test_dir} exists but is not a directory"

            # If we get here, the test passed!
            print(f"✓ Successfully created directory: {test_dir}")

        finally:
            # Clean up: remove the test directory if it exists
            # This runs even if the test fails, ensuring we don't leave test files around
            if test_dir.exists():
                test_dir.rmdir()  # Remove the empty directory
                print(f"✓ Cleaned up test directory: {test_dir}")

    def test_mkdir_command_silent_mode(self) -> None:
        """
        Test mkdir command using SILENT mode
        (returns True/False instead of raising exceptions).

        This shows how to use different return modes from the Command class.
        """
        cmd = Command()
        test_dir = Path(tempfile.gettempdir()) / "test_mkdir_silent"

        try:
            # Use SILENT mode - returns True on success, False on failure
            success = cmd.run(f"mkdir {test_dir}", mode=ReturnMode.SILENT)

            # Check that the command was successful
            assert success is True, "mkdir command failed"

            # Verify the directory exists
            assert test_dir.exists(), "Directory was not created despite success=True"

        finally:
            # Clean up
            if test_dir.exists():
                test_dir.rmdir()
