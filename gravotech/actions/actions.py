from enum import Enum

from gravotech.streamers.ip_streamer import IPStreamer


class LDMode(Enum):
    NORMAL = "N"
    SIMULATION = "S"
    AUTONOME = "A"


class GraveuseAction:
    def __init__(self, streamer: IPStreamer):
        self.streamer = streamer

    def go(self) -> str:
        unlock = self.streamer.lock()
        try:
            self.streamer.unsafe_write("GO")
            resp = self.streamer.unsafe_read()
            if resp.startswith("ER"):
                return resp
            if "GO M" not in resp:
                raise RuntimeError(f"Expected 'GO M', got '{resp}'")
            while True:
                resp = self.streamer.unsafe_read()
                if resp in ["GO P", "GO S", "GO F"] or resp.startswith("ER"):
                    return resp
        finally:
            unlock()

    def ld(self, filename: str, nb_marking: int, mode: LDMode) -> str:
        return self.streamer.write(f'LD "{filename}" {nb_marking} {mode.value}\r')

    def ls(self, mask: str = None) -> str:
        cmd = f"LS {mask}" if mask else "LS"
        return self.streamer.write(cmd)

    def st(self) -> str:
        return self.streamer.write(f"ST\r")

    def vg(self, index: int) -> str:
        return self.streamer.write(f"VG {index}\r")

    def vs(self, index: int, text: str) -> str:
        return self.streamer.write(f'VS {index} "{text}"\r')
