#!/usr/bin/env python3

"""
App Class (app.py)
"""

from src.core.command import Command
from src.ui.message import Message


class App:
    """Application class."""

    def __init__(self) -> None:
        """Initialize the App class."""
        self.message: Message = Message()
        self.command: Command = Command()

    def create_directory(self, directory_path: str) -> None:
        """
        Create a directory using the mkdir command and display a success message.

        Args:
            directory_path: Path of the directory to create
        """
        try:
            # Run mkdir command
            self.command.run(f"mkdir -p '{directory_path}'")

            # Display success message
            self.message.success(
                f"Directory '{directory_path}' created successfully!",
                title="Directory Created",
            )
        except Exception as e:
            # Display error message if mkdir fails
            self.message.error(
                f"Failed to create directory '{directory_path}': {str(e)}",
                title="Directory Creation Failed",
            )

    def run(self) -> None:
        """
        Run the application - demonstrates creating a directory.
        """
        # Example usage: create a test directory
        test_directory = "test_spoofer_dir"
        self.create_directory(test_directory)
