from enum import Enum

from gravotech.streamers.ip_streamer import IPStreamer


class LDMode(Enum):
    NORMAL = "N"
    SIMULATION = "S"
    AUTONOME = "A"


class GraveuseAction:
    def __init__(self, streamer: IPStreamer):
        self.streamer = streamer

    def go(self):
        resp = self.streamer.write("GO\r")
        while not (
            resp.startswith("ER") or resp == "GO P" or resp == "GO S" or resp == "GO F"
        ):
            resp = self.streamer.read()
        return resp

    def ld(self, filename: str, nb_marking: int, mode: LDMode) -> str:
        return self.streamer.write(f"LD {filename} {nb_marking} {mode}\r")

    def ls(self, mask: str = None) -> str:
        return self.streamer.write(f"LS {mask}\r")

    def st(self) -> str:
        return self.streamer.write(f"ST\r")

    def vg(self, index: int) -> str:
        return self.streamer.write(f"VG {index}\r")

    def vs(self, index: int, text: str) -> str:
        return self.streamer.write(f"VS {index} {text}\r")
