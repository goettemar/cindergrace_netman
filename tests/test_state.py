"""Tests for state management."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from cindergrace_netman.state import (
    DEFAULT_STATE,
    load_state,
    save_state,
    state_path,
)


@pytest.fixture
def temp_config_dir(tmp_path):
    """Create a temporary config directory."""
    config_dir = tmp_path / ".config" / "cindergrace_netman"
    config_dir.mkdir(parents=True)
    return config_dir


@pytest.fixture
def mock_state_path(temp_config_dir):
    """Mock state_path to use temp directory."""
    state_file = temp_config_dir / "state.json"
    with patch("cindergrace_netman.state.state_path", return_value=state_file):
        yield state_file


def test_state_path_returns_path():
    """Test that state_path returns a Path object."""
    result = state_path()
    assert isinstance(result, Path)
    assert result.name == "state.json"


def test_load_state_returns_defaults_when_no_file(mock_state_path):
    """Test that load_state returns defaults when file doesn't exist."""
    state = load_state()
    assert state["percent"] == DEFAULT_STATE["percent"]
    assert state["base_mbit"] == DEFAULT_STATE["base_mbit"]
    assert state["enabled"] == DEFAULT_STATE["enabled"]


def test_load_state_reads_existing_file(mock_state_path):
    """Test that load_state reads existing state file."""
    custom_state = {
        "percent": 75,
        "base_mbit": 250,
        "enabled": True,
        "iface": "eth0",
    }
    mock_state_path.write_text(json.dumps(custom_state))

    state = load_state()
    assert state["percent"] == 75
    assert state["base_mbit"] == 250
    assert state["enabled"] is True
    assert state["iface"] == "eth0"


def test_load_state_merges_with_defaults(mock_state_path):
    """Test that load_state merges partial state with defaults."""
    partial_state = {"percent": 50}
    mock_state_path.write_text(json.dumps(partial_state))

    state = load_state()
    assert state["percent"] == 50
    assert state["base_mbit"] == DEFAULT_STATE["base_mbit"]


def test_save_state_creates_file(mock_state_path):
    """Test that save_state creates state file."""
    state = {"percent": 80, "base_mbit": 100}
    save_state(state)

    assert mock_state_path.exists()
    saved = json.loads(mock_state_path.read_text())
    assert saved["percent"] == 80


def test_save_state_overwrites_existing(mock_state_path):
    """Test that save_state overwrites existing file."""
    mock_state_path.write_text(json.dumps({"percent": 10}))

    save_state({"percent": 90})

    saved = json.loads(mock_state_path.read_text())
    assert saved["percent"] == 90


def test_load_state_handles_invalid_json(mock_state_path):
    """Test that load_state handles corrupted JSON gracefully."""
    mock_state_path.write_text("not valid json {{{")

    state = load_state()
    # Should return defaults on error
    assert state["percent"] == DEFAULT_STATE["percent"]
