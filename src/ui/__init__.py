"""User interface components for vscode-spoofer."""

from .banner import print_banner
from .input import Input
from .menu import draw_main_menu
# from .panel import Panel  # Panel class not implemented yet
from .progress import ProgressBar
from .table import (
    FEATURES,
    draw_comparison_table,
    draw_features_table,
    draw_identifiers_table,
)

__all__ = [
    # Banner
    "print_banner",
    # Input
    "Input",
    # Menu
    "draw_main_menu",
    # Panel
    # "Panel",  # Panel class not implemented yet
    # Progress
    "ProgressBar",
    # Table
    "FEATURES",
    "draw_comparison_table",
    "draw_features_table",
    "draw_identifiers_table",
]