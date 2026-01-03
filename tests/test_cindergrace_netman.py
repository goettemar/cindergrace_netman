"""Tests für cindergrace_netman."""


def test_import():
    """Test ob Import funktioniert."""
    from cindergrace_netman import __version__
    assert __version__ == "0.1.0"
