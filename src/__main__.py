#!/usr/bin/env python3

"""Entry point for running Trial Spoofer as a module."""

import sys

from src.core.app import App

if __name__ == "__main__":
    app: App = App()
    app.run()
    sys.exit(0)
