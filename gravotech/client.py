from .actions.actions import GraveuseAction
from .streamers.ip_streamer import IPStreamer


class Gravotech:
    """
    Main controller class for the Gravotech marking system.

    This class serves as the primary entry point for communicating with a Gravotech
    marking machine. It orchestrates the connection via an IP streamer and provides
    access to high-level machine actions.

    :ivar Streamer: The low-level TCP/IP communication interface.
    :vartype Streamer: IPStreamer
    :ivar Actions: The high-level command interface to execute machine instructions.
    :vartype Actions: GraveuseAction
    """

    Streamer: IPStreamer
    Actions: GraveuseAction

    def __init__(self, ip: str, port: int, timeout: float = 5.0):
        """
        Initialize the Gravotech controller and its communication components.

        Setting up this class will automatically instantiate the IPStreamer and
        the GraveuseAction handler.

        :param ip: The IP address of the marking machine (e.g., "192.168.0.211").
        :type ip: str
        :param port: The TCP port for the telnet session (default is 55555 on Gravotech units).
        :type port: int
        :param timeout: Maximum time in seconds to wait for a network response, defaults to 5.0.
        :type timeout: float, optional
        """
        self.Streamer = IPStreamer(ip, port, timeout)
        self.Actions = GraveuseAction(self.Streamer)

    def connect(self):
        self.Streamer.connect()
        return self

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.Streamer.close()
