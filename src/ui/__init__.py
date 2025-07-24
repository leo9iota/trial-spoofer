"""User interface components for vscode-spoofer."""

from .banner import print_banner
from .input import Input
from .menu import draw_main_menu
from .panel import (
    Panel,
    draw_error_panel,
    draw_info_panel,
    draw_success_panel,
    draw_warning_panel,
)
from .progress import ProgressBar
from .table import (
    OPTIONS_DESCRIPTION,
    draw_comparison_table,
    draw_options_table,
    draw_system_identifiers_table,
)

__all__ = [
    # Banner
    "print_banner",
    # Input
    "Input",
    # Menu
    "draw_main_menu",
    # Panel
    "Panel",
    "draw_success_panel",
    "draw_error_panel",
    "draw_warning_panel",
    "draw_info_panel",
    # Progress
    "ProgressBar",
    # Table
    "OPTIONS_DESCRIPTION",
    "draw_comparison_table",
    "draw_options_table",
    "draw_system_identifiers_table",
]
