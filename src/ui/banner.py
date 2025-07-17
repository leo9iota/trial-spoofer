"""
Banner display for VS Code Spoofer
"""

from rich.console import Console
from rich.text import Text


banner = """
 ██▒   █▓  ██████  ▄████▄   ▒█████  ▓█████▄ ▓█████      ██████  ██▓███   ▒█████   ▒█████    █████▒▓█████  ██▀███  
▓██░   █▒▒██    ▒ ▒██▀ ▀█  ▒██▒  ██▒▒██▀ ██▌▓█   ▀    ▒██    ▒ ▓██░  ██▒▒██▒  ██▒▒██▒  ██▒▓██   ▒ ▓█   ▀ ▓██ ▒ ██▒
 ▓██  █▒░░ ▓██▄   ▒▓█    ▄ ▒██░  ██▒░██   █▌▒███      ░ ▓██▄   ▓██░ ██▓▒▒██░  ██▒▒██░  ██▒▒████ ░ ▒███   ▓██ ░▄█ ▒
  ▒██ █░░  ▒   ██▒▒▓▓▄ ▄██▒▒██   ██░░▓█▄   ▌▒▓█  ▄      ▒   ██▒▒██▄█▓▒ ▒▒██   ██░▒██   ██░░▓█▒  ░ ▒▓█  ▄ ▒██▀▀█▄  
   ▒▀█░  ▒██████▒▒▒ ▓███▀ ░░ ████▓▒░░▒████▓ ░▒████▒   ▒██████▒▒▒██▒ ░  ░░ ████▓▒░░ ████▓▒░░▒█░    ░▒████▒░██▓ ▒██▒
   ░ ▐░  ▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒░▒░▒░  ▒▒▓  ▒ ░░ ▒░ ░   ▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ▒░▒░▒░  ▒ ░    ░░ ▒░ ░░ ▒▓ ░▒▓░
   ░ ░░  ░ ░▒  ░ ░  ░  ▒     ░ ▒ ▒░  ░ ▒  ▒  ░ ░  ░   ░ ░▒  ░ ░░▒ ░       ░ ▒ ▒░   ░ ▒ ▒░  ░       ░ ░  ░  ░▒ ░ ▒░
     ░░  ░  ░  ░  ░        ░ ░ ░ ▒   ░ ░  ░    ░      ░  ░  ░  ░░       ░ ░ ░ ▒  ░ ░ ░ ▒   ░ ░       ░     ░░   ░ 
      ░        ░  ░ ░          ░ ░     ░       ░  ░         ░               ░ ░      ░ ░             ░  ░   ░     
     ░            ░                  ░                                                                            
"""


def print_banner() -> None:
    """Print the VS Code Spoofer banner."""
    console = Console()

    console.print(banner, style="bold red")

    subtitle = Text()
    subtitle.append("VSCode Spoofer", style="white")
    subtitle.append(" v0.1.0", style="dim white")
    console.print(subtitle)
    console.print()
