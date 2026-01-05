"""Tests for network utilities."""

from unittest.mock import patch, MagicMock

import pytest

from cindergrace_netman.net import (
    NetmanError,
    list_interfaces,
    get_default_interface,
    get_interface_state,
    get_interface_speed,
    list_interfaces_with_info,
)


class TestListInterfaces:
    """Tests for list_interfaces function."""

    def test_returns_list(self):
        """Test that list_interfaces returns a list."""
        result = list_interfaces()
        assert isinstance(result, list)

    def test_contains_interface_names(self):
        """Test that list_interfaces returns interface name strings."""
        result = list_interfaces()
        # All entries should be non-empty strings
        for iface in result:
            assert isinstance(iface, str)
            assert len(iface) > 0


class TestGetDefaultInterface:
    """Tests for get_default_interface function."""

    def test_returns_string_or_none(self):
        """Test that get_default_interface returns string or None."""
        result = get_default_interface()
        assert result is None or isinstance(result, str)


class TestGetInterfaceState:
    """Tests for get_interface_state function."""

    def test_returns_valid_state(self):
        """Test that get_interface_state returns valid state."""
        # Use an existing interface if possible
        interfaces = list_interfaces()
        if interfaces:
            state = get_interface_state(interfaces[0])
            assert state in ["up", "down", "unknown"]

    def test_unknown_interface_returns_unknown(self):
        """Test that unknown interface returns 'unknown'."""
        state = get_interface_state("nonexistent_iface_xyz")
        assert state == "unknown"


class TestGetInterfaceSpeed:
    """Tests for get_interface_speed function."""

    def test_returns_int_or_none(self):
        """Test that get_interface_speed returns int or None."""
        interfaces = list_interfaces()
        if interfaces:
            speed = get_interface_speed(interfaces[0])
            assert speed is None or isinstance(speed, int)

    def test_unknown_interface_returns_none(self):
        """Test that unknown interface returns None."""
        speed = get_interface_speed("nonexistent_iface_xyz")
        assert speed is None


class TestListInterfacesWithInfo:
    """Tests for list_interfaces_with_info function."""

    def test_returns_list_of_dicts(self):
        """Test that list_interfaces_with_info returns list of dicts."""
        result = list_interfaces_with_info()
        assert isinstance(result, list)
        for iface in result:
            assert isinstance(iface, dict)
            assert "name" in iface
            assert "state" in iface
            assert "speed_mbit" in iface
            assert "is_default" in iface

    def test_interface_info_structure(self):
        """Test that interface info has correct structure."""
        result = list_interfaces_with_info()
        if result:
            iface = result[0]
            assert isinstance(iface["name"], str)
            assert iface["state"] in ["up", "down", "unknown"]
            assert iface["speed_mbit"] is None or isinstance(iface["speed_mbit"], int)
            assert isinstance(iface["is_default"], bool)


class TestNetmanError:
    """Tests for NetmanError exception."""

    def test_netman_error_is_exception(self):
        """Test that NetmanError is an Exception."""
        error = NetmanError("test error")
        assert isinstance(error, Exception)
        assert str(error) == "test error"

    def test_can_raise_and_catch(self):
        """Test that NetmanError can be raised and caught."""
        with pytest.raises(NetmanError):
            raise NetmanError("test")
