"""Tests for UI table module."""

import pytest
from unittest.mock import patch, MagicMock

from ui.table import (
    FEATURES,
    draw_features_table,
    draw_identifiers_table,
    draw_comparison_table,
)


class TestTable:
    """Test table drawing functions."""

    def test_features_constant(self):
        """Test FEATURES constant structure."""
        assert isinstance(FEATURES, list)
        assert len(FEATURES) > 0
        
        for feature in FEATURES:
            assert isinstance(feature, dict)
            assert "name" in feature
            assert "description" in feature
            assert isinstance(feature["name"], str)
            assert isinstance(feature["description"], str)

    def test_draw_features_table(self):
        """Test drawing features table."""
        table = draw_features_table()
        
        # Check that it returns a Rich Table object
        assert hasattr(table, 'add_row')
        assert hasattr(table, 'add_column')

    @patch('ui.table.get_identifiers')
    def test_draw_identifiers_table(self, mock_get_identifiers):
        """Test drawing identifiers table."""
        mock_get_identifiers.return_value = {
            "MAC Address": "00:11:22:33:44:55",
            "Machine ID": "test-machine-id",
            "Hostname": "test-hostname"
        }
        
        table = draw_identifiers_table()
        
        # Check that it returns a Rich Table object
        assert hasattr(table, 'add_row')
        assert hasattr(table, 'add_column')
        mock_get_identifiers.assert_called_once()

    def test_draw_comparison_table(self):
        """Test drawing comparison table."""
        before = {
            "MAC Address": "00:11:22:33:44:55",
            "Machine ID": "old-machine-id"
        }
        after = {
            "MAC Address": "aa:bb:cc:dd:ee:ff",
            "Machine ID": "new-machine-id"
        }
        
        table = draw_comparison_table(before, after)
        
        # Check that it returns a Rich Table object
        assert hasattr(table, 'add_row')
        assert hasattr(table, 'add_column')

    def test_draw_comparison_table_truncation(self):
        """Test comparison table with long values."""
        before = {
            "Long Value": "a" * 50  # Very long value
        }
        after = {
            "Long Value": "b" * 50  # Very long value
        }
        
        table = draw_comparison_table(before, after)
        
        # Should not raise any errors with long values
        assert hasattr(table, 'add_row')