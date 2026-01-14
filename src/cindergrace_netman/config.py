"""
Configuration for Cindergrace NetMan.

Uses cindergrace_common for shared patterns.
"""

from pathlib import Path

from cindergrace_common import (
    BaseConfig,
    BrandingMixin,
    SecurityMixin,
    env_int,
)


class Config(BaseConfig, SecurityMixin, BrandingMixin):
    """Application configuration."""

    APP_PREFIX = "NETMAN"

    # Gradio settings
    # Port configurable via NETMAN_PORT env var
    PORT = env_int("NETMAN_PORT", 7863)

    # Default speed settings
    DEFAULT_BASE_MBIT = 100
    DEFAULT_PERCENT = 100

    # Ping defaults
    DEFAULT_PING_HOST = "8.8.8.8"
    DEFAULT_PING_COUNT = 4
    DEFAULT_PING_INTERVAL = 0.2

    # Download test defaults
    DEFAULT_DOWNLOAD_URL = "https://ash-speed.hetzner.com/100MB.bin"
    DEFAULT_DOWNLOAD_MAX_MB = 10

    # Paths
    PACKAGE_ROOT = Path(__file__).parent
    TRANSLATIONS_PATH = PACKAGE_ROOT / "translations" / "ui.yaml"

    @classmethod
    def get_env_docs(cls) -> dict[str, str]:
        """Document available environment variables."""
        docs = cls.get_security_docs()
        docs.update({
            "NETMAN_PORT": "Server port (default: 7863)",
        })
        return docs
