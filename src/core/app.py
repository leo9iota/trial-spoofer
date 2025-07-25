#!/usr/bin/env python3

"""
App Class (app.py)
"""

from src.ui.message import Message


class App:
    """Application class."""

    def __init__(self) -> None:
        """Initialize the App class."""
        self.message: Message = Message()
