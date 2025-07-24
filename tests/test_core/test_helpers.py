"""Tests for core helpers module."""

import pytest
from unittest.mock import patch, mock_open, MagicMock
import subprocess
from pathlib import Path

from utils import check_root, check_system_requirements, get_identifiers
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

    @patch('utils.check.run_cmd')
    def test_check_system_requirements_success(self, mock_run_cmd):
        """Test system requirements check when all tools are available."""
        mock_run_cmd.return_value = "/usr/bin/tool"
        
        result = check_system_requirements()
        assert result is True

    @patch('utils.check.run_cmd')
    def test_check_system_requirements_failure(self, mock_run_cmd):
        """Test system requirements check when tools are missing."""
        mock_run_cmd.side_effect = CmdError("which ip", 1, "", "command not found")
        
        result = check_system_requirements()
        assert result is False

    @patch('builtins.open', new_callable=mock_open, read_data='test-machine-id')
    @patch('utils.identifiers.run_cmd')
    def test_get_identifiers(self, mock_run_cmd, mock_file):
        """Test getting system identifiers."""
        # Mock run_cmd calls for different commands
        def mock_command(cmd, **kwargs):
            if 'ip link show' in cmd:
                return '2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP\n    link/ether 00:11:22:33:44:55 brd ff:ff:ff:ff:ff:ff'
            elif 'findmnt' in cmd:
                return '12345678-1234-1234-1234-123456789abc'
            elif 'hostname' in cmd:
                return 'test-hostname'
            else:
                raise CmdError(cmd, 1, "", "command not found")
        
        mock_run_cmd.side_effect = mock_command
        
        identifiers = get_identifiers()
        
        assert isinstance(identifiers, dict)
        assert 'MAC Address' in identifiers
        assert 'Machine ID' in identifiers
        assert 'Filesystem UUID' in identifiers
        assert 'Hostname' in identifiers