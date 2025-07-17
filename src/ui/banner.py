#!/usr/bin/env python3
"""
Banner display for VS Code Spoofer
"""

from rich.console import Console
from rich.text import Text


def print_banner() -> None:
    """Print the VS Code Spoofer banner."""
    console = Console()

    banner_text = """
██╗   ██╗███████╗     ██████╗ ██████╗ ██████╗ ███████╗    ███████╗██████╗  ██████╗  ██████╗ ███████╗███████╗██████╗
██║   ██║██╔════╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝    ██╔════╝██╔══██╗██╔═══██╗██╔═══██╗██╔════╝██╔════╝██╔══██╗
██║   ██║███████╗    ██║     ██║   ██║██║  ██║█████╗      ███████╗██████╔╝██║   ██║██║   ██║█████╗  █████╗  ██████╔╝
╚██╗ ██╔╝╚════██║    ██║     ██║   ██║██║  ██║██╔══╝      ╚════██║██╔═══╝ ██║   ██║██║   ██║██╔══╝  ██╔══╝  ██╔══██╗
 ╚████╔╝ ███████║    ╚██████╗╚██████╔╝██████╔╝███████╗    ███████║██║     ╚██████╔╝╚██████╔╝██║     ███████╗██║  ██║
  ╚═══╝  ╚══════╝     ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝    ╚══════╝╚═╝      ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝
"""

    # Print banner in cyan
    console.print(banner_text, style="bold cyan")

    # Print subtitle
    subtitle = Text()
    subtitle.append("Linux System Identifier Spoofing Utility", style="white")
    subtitle.append(" v0.1.0", style="dim white")
    console.print(subtitle, justify="center")
    console.print()
