"""Configuration management for vscode-spoofer."""

import os
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class Config:
    """Application configuration."""

    # Application settings
    debug: bool = field(
        default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true"
    )
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    # Default values
    default_hostname: str = field(
        default_factory=lambda: os.getenv("DEFAULT_HOSTNAME", "random")
    )
    default_username: str = field(
        default_factory=lambda: os.getenv("DEFAULT_USERNAME", "random")
    )

    # System paths
    home_path: Path = field(default_factory=lambda: Path.home())
    vscode_config_path: Path = field(default_factory=lambda: Path.home() / ".vscode")
    machine_id_path: Path = field(default_factory=lambda: Path("/etc/machine-id"))

    # Network settings
    default_interface: str = field(
        default_factory=lambda: os.getenv("DEFAULT_INTERFACE", "eth0")
    )

    # Feature toggles
    enable_mac_spoofing: bool = field(
        default_factory=lambda: os.getenv("ENABLE_MAC_SPOOFING", "true").lower()
        == "true"
    )
    enable_machine_id_spoofing: bool = field(
        default_factory=lambda: os.getenv("ENABLE_MACHINE_ID_SPOOFING", "true").lower()
        == "true"
    )
    enable_filesystem_spoofing: bool = field(
        default_factory=lambda: os.getenv("ENABLE_FILESYSTEM_SPOOFING", "true").lower()
        == "true"
    )
    enable_hostname_spoofing: bool = field(
        default_factory=lambda: os.getenv("ENABLE_HOSTNAME_SPOOFING", "true").lower()
        == "true"
    )
    enable_vscode_spoofing: bool = field(
        default_factory=lambda: os.getenv("ENABLE_VSCODE_SPOOFING", "true").lower()
        == "true"
    )
    enable_user_creation: bool = field(
        default_factory=lambda: os.getenv("ENABLE_USER_CREATION", "true").lower()
        == "true"
    )

    # Safety settings
    require_confirmation: bool = field(
        default_factory=lambda: os.getenv("REQUIRE_CONFIRMATION", "true").lower()
        == "true"
    )
    backup_configs: bool = field(
        default_factory=lambda: os.getenv("BACKUP_CONFIGS", "true").lower() == "true"
    )
    backup_path: Path = field(
        default_factory=lambda: Path.home() / ".vscode-spoofer-backups"
    )

    def __post_init__(self) -> None:
        """Post-initialization validation and setup."""
        # Ensure backup directory exists if backup is enabled
        if self.backup_configs:
            self.backup_path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        return cls()

    @classmethod
    def from_file(cls, config_file: Path) -> "Config":
        """Create configuration from a file (future implementation)."""
        # TODO: Implement file-based configuration
        return cls()

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            field.name: getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }

    def get_enabled_features(self) -> list[str]:
        """Get list of enabled features."""
        features = []
        if self.enable_mac_spoofing:
            features.append("MAC Address")
        if self.enable_machine_id_spoofing:
            features.append("Machine ID")
        if self.enable_filesystem_spoofing:
            features.append("Filesystem UUID")
        if self.enable_hostname_spoofing:
            features.append("Hostname")
        if self.enable_vscode_spoofing:
            features.append("VS Code Caches")
        if self.enable_user_creation:
            features.append("User Account")
        return features


# Global configuration instance
config = Config.from_env()


def get_config() -> Config:
    """Get the global configuration instance."""
    return config


def reload_config() -> Config:
    """Reload configuration from environment."""
    global config
    config = Config.from_env()
    return config
