"""Tests for configuration module."""

import os
import pytest
from pathlib import Path
from unittest.mock import patch

from core.config import Config, get_config, reload_config


class TestConfig:
    """Test configuration management."""

    def test_default_config(self):
        """Test default configuration values."""
        config = Config()
        
        assert config.debug is False
        assert config.log_level == "INFO"
        assert config.default_hostname == "random"
        assert config.default_username == "random"
        assert config.require_confirmation is True
        assert config.backup_configs is True

    def test_config_from_env(self):
        """Test configuration from environment variables."""
        env_vars = {
            "DEBUG": "true",
            "LOG_LEVEL": "DEBUG",
            "DEFAULT_HOSTNAME": "test-host",
            "DEFAULT_USERNAME": "test-user",
            "ENABLE_MAC_SPOOFING": "false",
            "REQUIRE_CONFIRMATION": "false"
        }
        
        with patch.dict(os.environ, env_vars):
            config = Config.from_env()
            
            assert config.debug is True
            assert config.log_level == "DEBUG"
            assert config.default_hostname == "test-host"
            assert config.default_username == "test-user"
            assert config.enable_mac_spoofing is False
            assert config.require_confirmation is False

    def test_get_enabled_features(self):
        """Test getting enabled features."""
        config = Config(
            enable_mac_spoofing=True,
            enable_machine_id_spoofing=False,
            enable_filesystem_spoofing=True,
            enable_hostname_spoofing=False,
            enable_vscode_spoofing=True,
            enable_user_creation=False
        )
        
        enabled_features = config.get_enabled_features()
        
        assert "MAC Address" in enabled_features
        assert "Machine ID" not in enabled_features
        assert "Filesystem UUID" in enabled_features
        assert "Hostname" not in enabled_features
        assert "VS Code Caches" in enabled_features
        assert "User Account" not in enabled_features

    def test_config_to_dict(self):
        """Test configuration to dictionary conversion."""
        config = Config()
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert "debug" in config_dict
        assert "log_level" in config_dict
        assert "default_hostname" in config_dict

    def test_global_config_functions(self):
        """Test global configuration functions."""
        config = get_config()
        assert isinstance(config, Config)
        
        reloaded_config = reload_config()
        assert isinstance(reloaded_config, Config)