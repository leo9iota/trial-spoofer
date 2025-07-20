"""Integration tests for CLI."""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

from cli import main, create_parser, show_config, check_prerequisites


class TestCLI:
    """Test CLI functionality."""

    def test_create_parser(self):
        """Test argument parser creation."""
        parser = create_parser()
        
        assert parser.prog == "vscode-spoofer"
        
        # Test parsing various arguments
        args = parser.parse_args(["--debug"])
        assert args.debug is True
        
        args = parser.parse_args(["--check"])
        assert args.check is True
        
        args = parser.parse_args(["--config"])
        assert args.config is True

    @patch('cli.Console')
    @patch('cli.get_config')
    def test_show_config(self, mock_get_config, mock_console_class):
        """Test configuration display."""
        mock_config = MagicMock()
        mock_config.debug = True
        mock_config.log_level = "DEBUG"
        mock_config.get_enabled_features.return_value = ["MAC Address", "Machine ID"]
        mock_get_config.return_value = mock_config
        
        mock_console = MagicMock()
        mock_console_class.return_value = mock_console
        
        show_config()
        
        # Verify console.print was called
        assert mock_console.print.called

    @patch('cli.check_system_requirements')
    @patch('cli.check_root')
    @patch('cli.Console')
    def test_check_prerequisites_success(self, mock_console_class, mock_check_root, mock_check_system):
        """Test successful prerequisites check."""
        mock_check_root.return_value = True
        mock_check_system.return_value = True
        
        result = check_prerequisites()
        assert result is True

    @patch('cli.check_system_requirements')
    @patch('cli.check_root')
    @patch('cli.Console')
    def test_check_prerequisites_no_root(self, mock_console_class, mock_check_root, mock_check_system):
        """Test prerequisites check without root."""
        mock_check_root.return_value = False
        mock_check_system.return_value = True
        
        result = check_prerequisites()
        assert result is False

    @patch('cli.show_config')
    def test_main_config_option(self, mock_show_config):
        """Test main function with --config option."""
        result = main(["--config"])
        
        assert result == 0
        mock_show_config.assert_called_once()

    @patch('cli.check_prerequisites')
    def test_main_check_option_success(self, mock_check_prerequisites):
        """Test main function with --check option (success)."""
        mock_check_prerequisites.return_value = True
        
        result = main(["--check"])
        
        assert result == 0

    @patch('cli.check_prerequisites')
    def test_main_check_option_failure(self, mock_check_prerequisites):
        """Test main function with --check option (failure)."""
        mock_check_prerequisites.return_value = False
        
        result = main(["--check"])
        
        assert result == 1