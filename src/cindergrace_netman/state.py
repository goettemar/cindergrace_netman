import json
import os
from pathlib import Path


DEFAULT_STATE = {
    "enabled": False,
    "percent": 100,
    "base_mbit": 100,  # DSL-Geschwindigkeit in Mbit/s
    "iface": None,
    "download_url": "https://speed.hetzner.de/10MB.bin",
}


def state_path() -> Path:
    config_root = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))
    return config_root / "cindergrace_netman" / "state.json"


def load_state() -> dict:
    path = state_path()
    if not path.exists():
        return DEFAULT_STATE.copy()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return DEFAULT_STATE.copy()
    merged = DEFAULT_STATE.copy()
    merged.update({k: data.get(k, v) for k, v in DEFAULT_STATE.items()})
    return merged


def save_state(state: dict) -> None:
    path = state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
