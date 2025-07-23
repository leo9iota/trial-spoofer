"""Tests for core helpers module."""

import pytest
from unittest.mock import patch, mock_open, MagicMock
import subprocess
from pathlib import Path

from core.helpers import check_root, check_system_requirements, get_identifiers
from core.command import CmdError


class TestHelpers:
    """Test helper functions."""

    @patch('os.environ.get')
    def test_check_root_as_root(self, mock_env_get):
        """Test root check when running as root."""
        mock_env_get.side_effect = lambda key, default=None: {
            'SUDO_USER': 'testuser',
            'USER': 'testuser'
        }.get(key, default)
        
        with patch('os.geteuid', return_value=0):
            user, home = check_root()
            assert user == 'testuser'
            assert home == Path('/home/testuser')

    def test_check_root_as_user(self):
        """Test root check when running as regular user."""
        with patch('os.geteuid', return_value=1000):
            with pytest.raises(SystemExit):
                check_root()

    @patch('core.helpers.run_cmd')
    def test_check_system_requirements_success(self, mock_run_cmd):
        """Test system requirements check when all tools are available."""
        mock_run_cmd.return_value = "/usr/bin/tool"
        
        result = check_system_requirements()
        assert result is True

    @patch('core.helpers.run_cmd')
    def test_check_system_requirements_failure(self, mock_run_cmd):
        """Test system requirements check when tools are missing."""
        mock_run_cmd.side_effect = CmdError("which ip", 1, "", "command not found")
        
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