"""Tests for core helpers module."""

import pytest
from unittest.mock import patch, mock_open, MagicMock
import subprocess

from core.helpers import check_root, check_system_requirements, get_identifiers


class TestHelpers:
    """Test helper functions."""

    def test_check_root_as_root(self):
        """Test root check when running as root."""
        with patch('os.geteuid', return_value=0):
            assert check_root() is True

    def test_check_root_as_user(self):
        """Test root check when running as regular user."""
        with patch('os.geteuid', return_value=1000):
            assert check_root() is False

    @patch('subprocess.run')
    def test_check_system_requirements_success(self, mock_run):
        """Test system requirements check when all tools are available."""
        mock_run.return_value.returncode = 0
        
        result = check_system_requirements()
        assert result is True

    @patch('subprocess.run')
    def test_check_system_requirements_failure(self, mock_run):
        """Test system requirements check when tools are missing."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'which')
        
        result = check_system_requirements()
        assert result is False

    @patch('builtins.open', new_callable=mock_open, read_data='test-machine-id')
    @patch('subprocess.run')
    @patch('socket.gethostname', return_value='test-hostname')
    def test_get_identifiers(self, mock_hostname, mock_run, mock_file):
        """Test getting system identifiers."""
        # Mock subprocess calls for different commands
        def mock_subprocess(*args, **kwargs):
            cmd = args[0]
            if 'ip link show' in ' '.join(cmd):
                mock_result = MagicMock()
                mock_result.stdout = 'link/ether 00:11:22:33:44:55'
                mock_result.returncode = 0
                return mock_result
            elif 'blkid' in ' '.join(cmd):
                mock_result = MagicMock()
                mock_result.stdout = 'UUID="12345678-1234-1234-1234-123456789abc"'
                mock_result.returncode = 0
                return mock_result
            else:
                mock_result = MagicMock()
                mock_result.returncode = 1
                return mock_result
        
        mock_run.side_effect = mock_subprocess
        
        identifiers = get_identifiers()
        
        assert isinstance(identifiers, dict)
        assert 'Hostname' in identifiers
        assert identifiers['Hostname'] == 'test-hostname'