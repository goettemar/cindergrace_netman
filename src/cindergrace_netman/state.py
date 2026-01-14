"""State management for Cindergrace NetMan.

Uses cindergrace_common.XDGStateStore for persistence.
"""

import shutil
from pathlib import Path

from cindergrace_common import XDGStateStore

# App-specific defaults
DEFAULT_STATE = {
    "enabled": False,
    "percent": 100,
    "base_mbit": 100,  # DSL speed in Mbit/s
    "iface": None,
    "download_url": "https://ash-speed.hetzner.com/100MB.bin",
    "ping_host": "8.8.8.8",
    "language": "en",  # Default language (en/de)
    "autostart": False,  # Start on login
}

# XDG autostart desktop entry template
DESKTOP_ENTRY = """[Desktop Entry]
Type=Application
Name=CinderGrace NetMan
Comment=Network bandwidth limiter
Exec="{exec_path}"
TryExec="{exec_path}"
Icon=network-transmit-receive
Terminal=false
Categories=Network;System;
X-GNOME-Autostart-enabled=true
"""

# Shared store instance
_store = XDGStateStore(
    app_name="cindergrace_netman",
    defaults=DEFAULT_STATE,
)


def state_path() -> Path:
    """Get path to state file."""
    return _store.get_path()


def load_state() -> dict:
    """Load state from disk, merged with defaults."""
    return _store.load()


def save_state(state: dict) -> None:
    """Save state to disk."""
    _store.save(state)


# === Autostart functionality (Linux XDG) ===


def autostart_path() -> Path:
    """Path to XDG autostart desktop entry."""
    from cindergrace_common.state import get_xdg_config_home

    return get_xdg_config_home() / "autostart" / "cindergrace-netman.desktop"


def get_start_script_path() -> Path:
    """Find the start.sh script in the project directory."""
    # Try to find start.sh relative to this module
    module_dir = Path(__file__).parent
    # Go up to project root (src/cindergrace_netman -> project root)
    project_root = module_dir.parent.parent
    start_sh = project_root / "start.sh"
    if start_sh.exists():
        return start_sh
    # Fallback: check if installed via pip, use the entry point
    entry_point = shutil.which("cindergrace-netman")
    if entry_point:
        return Path(entry_point)
    return start_sh  # Return anyway, will show error if missing


def is_autostart_enabled() -> bool:
    """Check if autostart is currently enabled."""
    return autostart_path().exists()


def enable_autostart() -> bool:
    """Enable autostart by creating desktop entry. Returns success."""
    desktop_path = autostart_path()
    desktop_path.parent.mkdir(parents=True, exist_ok=True)

    start_script = get_start_script_path()
    content = DESKTOP_ENTRY.format(exec_path=start_script)

    try:
        desktop_path.write_text(content, encoding="utf-8")
        return True
    except OSError:
        return False


def disable_autostart() -> bool:
    """Disable autostart by removing desktop entry. Returns success."""
    desktop_path = autostart_path()
    if desktop_path.exists():
        try:
            desktop_path.unlink()
            return True
        except OSError:
            return False
    return True  # Already disabled
