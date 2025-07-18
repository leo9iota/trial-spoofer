#!/usr/bin/env python3
"""
Tests for the main application functionality.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from main import VSCodeSpoofer


class TestVSCodeSpoofer:
    """Test cases for the VSCodeSpoofer class."""

    def test_init(self):
        """Test that VSCodeSpoofer initializes correctly."""
        with patch("main.root_check"):
            spoofer = VSCodeSpoofer()
            assert spoofer.console is not None
            assert spoofer.feature_table is not None
            assert spoofer.user_input is not None
            assert spoofer.progress is not None
            assert len(spoofer.feature_functions) == 6

    def test_feature_functions_mapping(self):
        """Test that all expected features are mapped to functions."""
        with patch("main.root_check"):
            spoofer = VSCodeSpoofer()
            expected_features = [
                "MAC Address",
                "Machine ID",
                "Filesystem UUID",
                "Hostname",
                "VS Code Caches",
                "New User",
            ]

            for feature in expected_features:
                assert feature in spoofer.feature_functions
                assert callable(spoofer.feature_functions[feature])

    @patch("main.root_check")
    def test_validate_system_requirements_linux(self, mock_root_check):
        """Test system validation on Linux."""
        mock_root_check.return_value = ("test_user", "/home/test_user")

        with (
            patch("platform.system", return_value="Linux"),
            patch("main.run_cmd") as mock_run_cmd,
        ):
            spoofer = VSCodeSpoofer()
            result = spoofer.validate_system_requirements()
            assert result is True

            # Check that required commands were validated
            expected_calls = 3  # ip, systemctl, hostnamectl
            assert mock_run_cmd.call_count == expected_calls

    @patch("main.root_check")
    def test_validate_system_requirements_non_linux(self, mock_root_check):
        """Test system validation on non-Linux systems."""
        mock_root_check.return_value = ("test_user", "/home/test_user")

        with patch("platform.system", return_value="Windows"):
            spoofer = VSCodeSpoofer()
            result = spoofer.validate_system_requirements()
            assert result is False

    @patch("main.root_check")
    def test_run_selected_features(self, mock_root_check):
        """Test running selected features."""
        mock_root_check.return_value = ("test_user", "/home/test_user")

        spoofer = VSCodeSpoofer()

        # Mock the feature functions
        mock_func = MagicMock(return_value=True)
        spoofer.feature_functions = {"Test Feature": mock_func}

        # Mock the progress display
        with (
            patch.object(spoofer.progress, "start_task"),
            patch.object(spoofer.progress, "complete_task"),
            patch.object(spoofer.progress, "create_progress_display"),
        ):
            results = spoofer.run_selected_features(["Test Feature"])

            assert results == {"Test Feature": True}
            mock_func.assert_called_once()

    def test_display_header(self):
        """Test header display creation."""
        with patch("main.root_check"):
            spoofer = VSCodeSpoofer()
            header = spoofer.display_header()

            assert header is not None
            # Check that it's a Panel object
            from rich.panel import Panel

            assert isinstance(header, Panel)


def test_main_function_import():
    """Test that the main function can be imported."""
    from main import main

    assert callable(main)


def test_imports():
    """Test that all required modules can be imported."""
    try:
        import main
        from ui.input import UserInput
        from ui.progress_bar import SpoofingProgress
        from ui.tables import FeatureTable, identifiers_table
        from utils.helpers import delete_vscode_caches, root_check
        from utils.spoofer import (
            spoof_filesystem_uuid,
            spoof_mac_addr,
            spoof_machine_id,
        )
        from utils.system import change_hostname, create_user, update_boot_config

        # If we get here, all imports succeeded
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
