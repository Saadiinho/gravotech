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
        """
        Query the current connection type (master or slave).

        Only the master connection can execute control commands. Up to 5 clients
        can connect simultaneously, but only one can be the master.

        :return: Connection status (e.g., 'GP "MASTER":"1"' if master)
        :rtype: str
        """
        resp = self.streamer.write('GP "MASTER"\r')
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def ld(self, filename: str, nb_marking: int, mode: LDMode) -> str:
        """
        Load a marking file into the machine's memory.

        This command prepares the machine for marking by loading the specified
        T2L file with the desired execution parameters.

        :param filename: Name of the T2L file (extension optional)
        :type filename: str
        :param nb_marking: Number of markings to perform (0 for infinite)
        :type nb_marking: int
        :param mode: Execution mode (NORMAL, SIMULATION, or AUTONOME)
        :type mode: LDMode
        :return: Machine response (typically "LD 1" on success)
        :rtype: str
        :raises RuntimeError: If the file doesn't exist or is invalid
        """
        resp = self.streamer.write(f'LD "{filename}" {nb_marking} {mode.value}\r')
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def ls(self, mask: str = None) -> str:
        """
        List files stored in the machine's memory.

        Returns a multi-line response with the number of files followed by
        each filename on a separate line.

        :param mask: File filter pattern (e.g., "*.t2l", "*.lo3").
                     None lists all files.
        :type mask: str, optional
        :return: Multi-line response with file count and filenames
        :rtype: str
        """
        cmd = f"LS {mask}" if mask else "LS"
        resp = self.streamer.write(cmd)
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def pf(self, filename: str, data: bytes) -> str:
        """
        Upload a file to the machine's memory.

        Sends a file (T2L, LO3, PO3) to the machine using hexadecimal encoding.

        :param filename: Target filename on the machine
        :type filename: str
        :param data: File content as hexadecimal bytes (no spaces)
        :type data: bytes
        :return: Machine response (typically "PF 1" on success)
        :rtype: str
        :raises RuntimeError: If the file is too large or invalid
        """
        resp = self.streamer.write(f'PF "{filename}" {data}\r')
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def rm(self, mask: str) -> str:
        """
        Delete files from the machine's memory.

        Removes files matching the specified pattern. Use with caution as this
        operation is irreversible.

        :param mask: File pattern to delete (e.g., "test.t2l", "*.t2l")
        :type mask: str
        :return: Machine response (typically "RM 1" on success)
        :rtype: str
        """
        cmd = f"RM {mask}" if mask else "RM"
        resp = self.streamer.write(cmd)
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def sp(self, value: bool) -> str:
        """
        Set the connection type to master or slave.

        Allows a client to request or release master control. Only one client
        can be master at a time.

        :param value: True to become master, False to become slave
        :type value: bool
        :return: Machine response (typically "SP 1" on success)
        :rtype: str
        :raises RuntimeError: If another client already holds master control
        """
        resp = self.streamer.write(f'SP "MASTER":"{int(value)}"\r')
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def st(self) -> str:
        """
        Query the current machine status.

        Returns the machine state, safety status, and marking mode.
        Response format: "ST state rearm markmode"

        :return: Status string (e.g., "ST 4 0 1")
            - state: 1=Init, 2=Alive, 4=Ready, 8=Marking, 16=Pause, 32=Fault
            - rearm: 0=OK, 1=E-stop, 2=Interlock, 3=Shutter error
            - markmode: 0=Normal, 1=Autonomous, 2=Simulation
        :rtype: str
        """
        resp = self.streamer.write(f"ST\r")
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def vg(self, index: int) -> str:
        """
        Get the value of a variable.

        Variables (V0-V9) can be used to pass dynamic data to marking files.

        :param index: Variable number (0-9)
        :type index: int
        :return: Variable content (text)
        :rtype: str
        :raises RuntimeError: If index is out of range
        """
        resp = self.streamer.write(f"VG {index}\r")
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def vs(self, index: int, text: str) -> str:
        """
        Set the value of a variable.

        Variables are used to inject dynamic text into marking files at runtime.

        :param index: Variable number (0-9)
        :type index: int
        :param text: UTF-8 text to assign to the variable
        :type text: str
        :return: Machine response (e.g., "VS 1 0" = success, variable 0)
        :rtype: str
        :raises RuntimeError: If index is out of range
        """
        resp = self.streamer.write(f'VS {index} "{text}"\r')
        if resp.startswith("ER"):
            return check_err(resp)
        return resp
