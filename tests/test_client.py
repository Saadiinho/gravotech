import pytest
from unittest.mock import Mock, patch

from gravotech.client import Gravotech

# ============================================================================
# INIT
# ============================================================================


@patch("gravotech.client.IPStreamer")
@patch("gravotech.client.GraveuseAction")
def test_gravotech_init(mock_action_cls, mock_streamer_cls):
    mock_streamer = Mock()
    mock_streamer_cls.return_value = mock_streamer

    mock_action = Mock()
    mock_action_cls.return_value = mock_action

    g = Gravotech("127.0.0.1", 3000, timeout=3.0)

    mock_streamer_cls.assert_called_once_with("127.0.0.1", 3000, 3.0)
    mock_action_cls.assert_called_once_with(mock_streamer)

    assert g.Streamer is mock_streamer
    assert g.Actions is mock_action


# ============================================================================
# CONNECT
# ============================================================================


@patch("gravotech.client.IPStreamer")
@patch("gravotech.client.GraveuseAction")
def test_gravotech_connect(mock_action_cls, mock_streamer_cls):
    mock_streamer = Mock()
    mock_streamer_cls.return_value = mock_streamer

    g = Gravotech("127.0.0.1", 3000)

    result = g.connect()

    mock_streamer.connect.assert_called_once()
    assert result is g


# ============================================================================
# CONTEXT MANAGER
# ============================================================================


@patch("gravotech.client.IPStreamer")
@patch("gravotech.client.GraveuseAction")
def test_gravotech_context_manager(mock_action_cls, mock_streamer_cls):
    mock_streamer = Mock()
    mock_streamer_cls.return_value = mock_streamer

    with Gravotech("127.0.0.1", 3000) as g:
        mock_streamer.connect.assert_called_once()
        assert g.Streamer is mock_streamer

    mock_streamer.close.assert_called_once()


# ============================================================================
# CONTEXT MANAGER WITH EXCEPTION
# ============================================================================


@patch("gravotech.client.IPStreamer")
@patch("gravotech.client.GraveuseAction")
def test_gravotech_context_manager_exception(mock_action_cls, mock_streamer_cls):
    mock_streamer = Mock()
    mock_streamer_cls.return_value = mock_streamer

    with pytest.raises(RuntimeError):
        with Gravotech("127.0.0.1", 3000):
            raise RuntimeError("boom")

    mock_streamer.close.assert_called_once()
