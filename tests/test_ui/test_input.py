"""Tests for UI input module."""

import pytest
from unittest.mock import patch, MagicMock

from ui.input import Input


class TestInput:
    """Test input handling."""

    def test_input_initialization(self):
        """Test Input class initialization."""
        input_handler = Input()
        assert hasattr(input_handler, 'console')

    @patch('ui.input.Confirm.ask')
    def test_get_feature_selection_all_yes(self, mock_confirm):
        """Test feature selection with all features selected."""
        mock_confirm.return_value = True
        
        input_handler = Input()
        features = [
            {"name": "MAC Address", "description": "Test MAC"},
            {"name": "Machine ID", "description": "Test Machine ID"}
        ]
        
        selected = input_handler.get_feature_selection(features)
        
        expected_features = [
            "MAC Address", "Machine ID", "Filesystem UUID", 
            "Hostname", "VS Code Caches", "New User"
        ]
        
        for feature in expected_features:
            assert feature in selected

    @patch('ui.input.Confirm.ask')
    def test_get_feature_selection_all_no(self, mock_confirm):
        """Test feature selection with no features selected."""
        mock_confirm.return_value = False
        
        input_handler = Input()
        features = [
            {"name": "MAC Address", "description": "Test MAC"}
        ]
        
        selected = input_handler.get_feature_selection(features)
        
        assert selected == []

    @patch('ui.input.Prompt.ask')
    @patch('ui.input.Confirm.ask')
    def test_custom_hostname_input(self, mock_confirm, mock_prompt):
        """Test custom hostname input."""
        # First confirm for hostname feature, then no for random hostname
        mock_confirm.side_effect = [True, False]
        mock_prompt.return_value = "custom-hostname"
        
        input_handler = Input()
        features = []
        
        selected = input_handler.get_feature_selection(features)
        
        assert "Hostname" in selected
        assert input_handler.get_custom_hostname() == "custom-hostname"

    @patch('ui.input.Prompt.ask')
    @patch('ui.input.Confirm.ask')
    def test_custom_username_input(self, mock_confirm, mock_prompt):
        """Test custom username input."""
        # Mock confirmations: skip to user creation, then yes for user, no for random
        mock_confirm.side_effect = [False, False, False, False, False, True, False]
        mock_prompt.return_value = "custom-user"
        
        input_handler = Input()
        features = []
        
        selected = input_handler.get_feature_selection(features)
        
        assert "New User" in selected
        assert input_handler.get_custom_username() == "custom-user"

    def test_display_methods(self):
        """Test display methods don't raise errors."""
        input_handler = Input()
        
        # These should not raise exceptions
        input_handler.display_warning("Test warning")
        input_handler.display_error("Test error")
        input_handler.display_success("Test success")