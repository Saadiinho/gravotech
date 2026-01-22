from libs.actions.actions import GraveuseAction
from libs.streamers.ip_streamer import IPStreamer


class Gravotech:
    Streamer: IPStreamer
    Actions: GraveuseAction

    def __init__(self, ip: str, port: int, timeout: float = 5.0):
        self.Streamer = IPStreamer(ip, port, timeout)
        self.Actions = GraveuseAction(self.Streamer)
