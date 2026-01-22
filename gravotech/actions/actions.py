from enum import Enum

from gravotech.streamers.ip_streamer import IPStreamer
from gravotech.utils.errors import check_err


class LDMode(Enum):
    """Marking file execution mode for the LD command."""

    NORMAL = "N"
    SIMULATION = "S"
    AUTONOME = "A"


class GraveuseAction:
    """
    High-level command interface for controlling a Gravotech marking machine.

    This class provides methods to execute specific machine instructions via
    the TCP/IP streamer, abstracting the low-level protocol details.

    :param streamer: TCP/IP communication interface
    :type streamer: IPStreamer
    """

    def __init__(self, streamer: IPStreamer):
        self.streamer = streamer

    def ad(self) -> str:
        resp = self.streamer.write("AD\r")
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def am(self) -> str:
        resp = self.streamer.write("AM\r")
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def go(self) -> str:
        unlock = self.streamer.lock()
        try:
            self.streamer.unsafe_write("GO")
            resp = self.streamer.unsafe_read()
            if resp.startswith("ER"):
                return check_err(resp)
            if "GO M" not in resp:
                raise RuntimeError(f"Expected 'GO M', got '{resp}'")
            while True:
                resp = self.streamer.unsafe_read()
                if resp in ["GO P", "GO S", "GO F"] :
                    return resp
                if resp.startswith("ER"):
                    return check_err(resp)
        finally:
            unlock()

    def gp(self) -> str:
        resp = self.streamer.write('GP "MASTER"\r')
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def ld(self, filename: str, nb_marking: int, mode: LDMode) -> str:
        resp = self.streamer.write(f'LD "{filename}" {nb_marking} {mode.value}\r')
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def ls(self, mask: str = None) -> str:
        cmd = f"LS {mask}" if mask else "LS"
        resp = self.streamer.write(cmd)
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def pf(self, filename: str, data: bytes) -> str:
        resp = self.streamer.write(f'PF "{filename}" {data}\r')
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def rm(self, mask: str) -> str:
        cmd = f"RM {mask}" if mask else "RM"
        resp = self.streamer.write(cmd)
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def sp(self, value: bool) -> str:
        resp = self.streamer.write(f'SP "MASTER":"{int(value)}"\r')
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def st(self) -> str:
        resp = self.streamer.write(f"ST\r")
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def vg(self, index: int) -> str:
        resp = self.streamer.write(f"VG {index}\r")
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def vs(self, index: int, text: str) -> str:
        resp = self.streamer.write(f'VS {index} "{text}"\r')
        if resp.startswith("ER"):
            return check_err(resp)
        return resp
