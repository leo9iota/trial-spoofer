"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile
import os


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def mock_console():
    """Mock Rich console for UI tests."""
    return Mock()


@pytest.fixture
def mock_root_check():
    """Mock root permission check."""
    with patch('utils.check_root', return_value=True):
        yield


@pytest.fixture
def mock_system_requirements():
    """Mock system requirements check."""
    with patch('utils.check_system_requirements', return_value=True):
        yield


@pytest.fixture
def sample_identifiers():
    """Sample system identifiers for testing."""
    return {
        "MAC Address": "00:11:22:33:44:55",
        "Machine ID": "abcd1234efgh5678",
        "Filesystem UUID": "12345678-1234-1234-1234-123456789abc",
        "Hostname": "test-hostname"
    }


@pytest.fixture
def mock_run_cmd():
    """Mock command execution."""
    with patch('core.command.run_cmd') as mock_run:
        mock_run.return_value = ""
        yield mock_run


@pytest.fixture  
def mock_subprocess():
    """Mock subprocess calls for legacy code."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        yield mock_run