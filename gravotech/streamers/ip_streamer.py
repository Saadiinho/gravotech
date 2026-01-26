import socket
import threading
import time
from typing import Optional, Callable
import logging


class IPStreamer:
    """
    Low-level TCP/IP communication interface for Gravotech marking machines.

    This class manages a Telnet-like socket connection, handling command transmission,
    response reading, and thread-safe operations. It supports automatic retries
    and multi-line response parsing for specific commands like LS.

    :ivar ip: The IP address of the marking machine.
    :vartype ip: str
    :ivar port: The TCP port for the session (default 55555).
    :vartype port: int
    :ivar timeout: Socket timeout in seconds for network operations.
    :vartype timeout: float
    """

    def __init__(self, ip: str, port: int, timeout: float = 5.0):
        """
        Initialize the IPStreamer and establish a connection.

        :param ip: Target machine IP address.
        :param port: Target machine TCP port.
        :param timeout: Network timeout in seconds, defaults to 5.0.
        :raises RuntimeError: If the initial connection fails.
        """
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.max_attempts = 5
        self.sock: Optional[socket.socket] = None
        self.mu = threading.RLock()

    def connect(self):
        """
        Establishes a TCP connection to the marking machine.

        Configures the socket with an initial connection timeout of 10 seconds
        before switching to the operational .

        :raises RuntimeError: If the connection to the specified IP/Port fails.
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10)
            self.sock.connect((self.ip, self.port))
            self.sock.settimeout(self.timeout)
            logging.info(f"Established connection to {self.ip}:{self.port}")
        except Exception as e:
            self.close()
            raise RuntimeError(f"Connection to {self.ip}:{self.port} failed") from e

    def close(self):
        """
        Closes the current socket connection safely.

        :raises RuntimeError: If closing the socket encounters an error.
        """
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                raise RuntimeError(
                    f"Closing connection to {self.ip}:{self.port} failed"
                )
            self.sock = None
        logging.info(f"Closing connection to {self.ip}:{self.port}")

    def retry(self, max_attempts: int = 3, delay: float = 1.0) -> bool:
        """
        Attempts to reconnect to the machine using exponential backoff.

        :param max_attempts: Maximum number of reconnection attempts, defaults to 3.
        :param delay: Initial delay between attempts in seconds, defaults to 1.0.
        :return: True if reconnection is successful.
        :raises RuntimeError: If reconnection fails after all attempts.
        """
        self.close()
        for attempt in range(1, max_attempts + 1):
            try:
                self.connect()
                return True
            except Exception as e:
                if attempt < max_attempts:
                    logging.error(f"Retrying attempt {attempt}/{max_attempts}: {e}")
                    wait_time = delay * (2 ** (attempt - 1))
                    time.sleep(wait_time)
                else:
                    raise RuntimeError(
                        f"Unable to reconnect after {max_attempts} attempts"
                    ) from e
        return False

    def lock(self) -> Callable[[], None]:
        """
        Acquires the communication lock and returns a release function.

        Used for manually grouping multiple "unsafe" operations into a single
        atomic transaction.

        :return: A callable that releases the Reentrant Lock (mu).
        :rtype: Callable[[], None]
        """
        self.mu.acquire()
        return lambda: self.mu.release()

    # ========================================================================
    # INTERNAL METHODS
    # ========================================================================

    def _read_line(self) -> str:
        """
        Reads a single line from the socket.

        Lines are expected to be terminated by <CR><LF> (or just <LF>).
        The <CR> is stripped and the resulting bytes are decoded as ASCII.

        :return: The decoded string without trailing terminators.
        :raises RuntimeError: If not connected or the host closes the connection.
        """
        if self.sock is None:
            raise RuntimeError("Not connected")
        buffer = b""
        while True:
            char = self.sock.recv(1)
            if not char:
                raise RuntimeError("Connection closed by remote host")
            if char == b"\n":
                break
            if char != b"\r":
                buffer += char
        return buffer.decode("ascii")

    def _write_cmd(self, cmd: str) -> None:
        """
        Sends a command string to the socket.

        Ensures the command ends with a Carriage Return <CR> (code 13).

        :param cmd: The text command to send.
        :raises RuntimeError: If not connected or a network error occurs.
        """
        if not cmd.endswith("\r"):
            cmd += "\r"
        if self.sock is None:
            raise RuntimeError("Not connected")
        try:
            self.sock.sendall(cmd.encode("ascii"))
        except (socket.timeout, ConnectionResetError, BrokenPipeError) as e:
            raise RuntimeError("Network error during write") from e

    def _read_ls_response(self) -> str:
        """
        Parses a multi-line response specific to the LS command.

        The LS response starts with the number of files found, followed by each
        filename on a new line.

        :return: Newline-separated list of filenames.
        """
        nb_files_str = self._read_line()
        try:
            nb_files = int(nb_files_str)
        except ValueError:
            return nb_files_str
        lines = [nb_files_str]
        for _ in range(nb_files):
            filename = self._read_line()
            lines.append(filename)
        return "\n".join(lines)

    # ========================================================================
    # UNSAFE METHODS
    # ========================================================================

    def unsafe_write(self, cmd: str) -> None:
        """
        Sends a command without acquiring the lock.

        :param cmd: The command string.
        """
        self._write_cmd(cmd)

    def unsafe_read(self, timeout: Optional[float] = None) -> str:
        """
        Reads a line without acquiring the lock, with an optional temporary timeout.

        :param timeout: Optional temporary socket timeout.
        :return: The decoded string.
        """
        if timeout is not None:
            old_timeout = self.sock.gettimeout()
            self.sock.settimeout(timeout)
        try:
            return self._read_line()
        finally:
            if timeout is not None:
                self.sock.settimeout(old_timeout)

    # ========================================================================
    # THREAD-SAFE METHODS
    # ========================================================================

    def read(self) -> str:
        """
        Thread-safe read operation.

        :return: The decoded string.
        """
        with self.mu:
            return self._read_line()

    def write(self, cmd: str) -> str:
        """
        Thread-safe write and read operation with automatic retry on failure.

        This method sends a command and immediately waits for the expected
        response.

        :param cmd: The command string to send.
        :return: The machine's response.
        """
        with self.mu:
            try:
                return self._write_and_read(cmd)
            except (socket.timeout, ConnectionResetError, BrokenPipeError) as e:
                logging.error(f"Network error: {e}, attempting retry...")
                self.retry()
                return self._write_and_read(cmd)

    def _write_and_read(self, cmd: str) -> str:
        """
        Internal implementation of a write followed by a read.

        :param cmd: The command string.
        :return: The machine's response.
        """
        self._write_cmd(cmd)
        if cmd.strip().upper().startswith("LS"):
            return self._read_ls_response()
        return self._read_line()
