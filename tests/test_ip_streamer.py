import socket
from unittest.mock import Mock, patch, call

import pytest

from gravotech.streamers.ip_streamer import IPStreamer

# ============================================================================
# CONNECT / CLOSE
# ============================================================================


@patch("socket.socket")
def test_connect_success(mock_socket_cls):
    mock_socket = Mock()
    mock_socket_cls.return_value = mock_socket

    streamer = IPStreamer("127.0.0.1", 3000)
    streamer.connect()

    mock_socket.connect.assert_called_once_with(("127.0.0.1", 3000))
    assert streamer.sock is mock_socket


@patch("socket.socket")
def test_connect_failure(mock_socket_cls):
    mock_socket = Mock()
    mock_socket.connect.side_effect = OSError("boom")
    mock_socket_cls.return_value = mock_socket

    streamer = IPStreamer("127.0.0.1", 3000)

    with pytest.raises(RuntimeError):
        streamer.connect()

    assert streamer.sock is None


def test_close_success():
    streamer = IPStreamer("127.0.0.1", 3000)
    mock_sock = Mock()
    streamer.sock = mock_sock
    streamer.close()
    mock_sock.close.assert_called_once()
    assert streamer.sock is None


# ============================================================================
# LOCK
# ============================================================================


def test_lock_returns_unlock_function():
    streamer = IPStreamer("127.0.0.1", 3000)

    unlock = streamer.lock()
    assert callable(unlock)

    # Should not raise
    unlock()


# ============================================================================
# _READ_LINE
# ============================================================================


def test_read_line_ok():
    streamer = IPStreamer("127.0.0.1", 3000)
    streamer.sock = Mock()

    streamer.sock.recv.side_effect = [b"H", b"E", b"L", b"L", b"O", b"\n"]

    resp = streamer._read_line()
    assert resp == "HELLO"


def test_read_line_strips_cr():
    streamer = IPStreamer("127.0.0.1", 3000)
    streamer.sock = Mock()

    streamer.sock.recv.side_effect = [b"H", b"I", b"\r", b"\n"]

    resp = streamer._read_line()
    assert resp == "HI"


def test_read_line_connection_closed():
    streamer = IPStreamer("127.0.0.1", 3000)
    streamer.sock = Mock()
    streamer.sock.recv.return_value = b""

    with pytest.raises(RuntimeError):
        streamer._read_line()


# ============================================================================
# _WRITE_CMD
# ============================================================================


def test_write_cmd_appends_cr():
    streamer = IPStreamer("127.0.0.1", 3000)
    streamer.sock = Mock()

    streamer._write_cmd("ST")

    streamer.sock.sendall.assert_called_once_with(b"ST\r")


def test_write_cmd_already_has_cr():
    streamer = IPStreamer("127.0.0.1", 3000)
    streamer.sock = Mock()

    streamer._write_cmd("ST\r")

    streamer.sock.sendall.assert_called_once_with(b"ST\r")


def test_write_cmd_not_connected():
    streamer = IPStreamer("127.0.0.1", 3000)

    with pytest.raises(RuntimeError):
        streamer._write_cmd("ST")


def test_write_cmd_network_error():
    streamer = IPStreamer("127.0.0.1", 3000)
    streamer.sock = Mock()
    streamer.sock.sendall.side_effect = BrokenPipeError()

    with pytest.raises(RuntimeError):
        streamer._write_cmd("ST")


# ============================================================================
# _READ_LS_RESPONSE
# ============================================================================


def test_read_ls_response_ok():
    streamer = IPStreamer("127.0.0.1", 3000)
    streamer._read_line = Mock(
        side_effect=[
            "3",
            "FILE1.T2L",
            "FILE2.T2L",
            "TEST.T2L",
        ]
    )

    resp = streamer._read_ls_response()
    assert resp == "3\nFILE1.T2L\nFILE2.T2L\nTEST.T2L"


def test_read_ls_response_invalid_header():
    streamer = IPStreamer("127.0.0.1", 3000)
    streamer._read_line = Mock(return_value="ER 12")

    resp = streamer._read_ls_response()
    assert resp == "ER 12"


# ============================================================================
# UNSAFE READ
# ============================================================================


def test_unsafe_read_with_timeout():
    streamer = IPStreamer("127.0.0.1", 3000)
    streamer.sock = Mock()
    streamer.sock.gettimeout.return_value = 5.0
    streamer._read_line = Mock(return_value="OK")

    resp = streamer.unsafe_read(timeout=1.0)

    assert resp == "OK"
    streamer.sock.settimeout.assert_has_calls(
        [
            call(1.0),
            call(5.0),
        ]
    )


# ============================================================================
# THREAD SAFE READ
# ============================================================================


def test_read_thread_safe():
    streamer = IPStreamer("127.0.0.1", 3000)
    streamer._read_line = Mock(return_value="ST 4 0 0")

    resp = streamer.read()

    assert resp == "ST 4 0 0"


# ============================================================================
# WRITE / RETRY
# ============================================================================


@patch.object(IPStreamer, "retry")
def test_write_retry_success(mock_retry):
    streamer = IPStreamer("127.0.0.1", 3000)

    streamer._write_and_read = Mock(
        side_effect=[
            socket.timeout(),
            "ST 4 0 0",
        ]
    )

    resp = streamer.write("ST")

    assert resp == "ST 4 0 0"
    mock_retry.assert_called_once()


def test_write_no_retry_needed():
    streamer = IPStreamer("127.0.0.1", 3000)
    streamer._write_and_read = Mock(return_value="OK")

    resp = streamer.write("ST")

    assert resp == "OK"


# ============================================================================
# _WRITE_AND_READ
# ============================================================================


def test_write_and_read_standard_command():
    streamer = IPStreamer("127.0.0.1", 3000)

    streamer._write_cmd = Mock()
    streamer._read_line = Mock(return_value="ST 4 0 0")

    resp = streamer._write_and_read("ST")

    assert resp == "ST 4 0 0"


def test_write_and_read_ls_command():
    streamer = IPStreamer("127.0.0.1", 3000)

    streamer._write_cmd = Mock()
    streamer._read_ls_response = Mock(return_value="2\nA\nB")

    resp = streamer._write_and_read("LS")

    assert resp == "2\nA\nB"


# ============================================================================
# RETRY
# ============================================================================


@patch.object(IPStreamer, "connect")
@patch.object(IPStreamer, "close")
def test_retry_success(mock_close, mock_connect):
    streamer = IPStreamer("127.0.0.1", 3000)

    result = streamer.retry(max_attempts=1)

    assert result is True
    mock_connect.assert_called_once()


@patch.object(IPStreamer, "connect")
@patch.object(IPStreamer, "close")
def test_retry_failure(mock_close, mock_connect):
    mock_connect.side_effect = RuntimeError("fail")

    streamer = IPStreamer("127.0.0.1", 3000)

    with pytest.raises(RuntimeError):
        streamer.retry(max_attempts=2, delay=0)
