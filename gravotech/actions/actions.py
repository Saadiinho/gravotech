from enum import Enum

from gravotech.streamers.ip_streamer import IPStreamer
from gravotech.utils.errors import check_err


class LDMode(str, Enum):
    """Marking file execution mode for the LD command."""

    NORMAL = "N"
    SIMULATION = "S"
    AUTONOME = "A"


class GraveuseAction:
    """
    High-level command interface for controlling a Gravotech marking machine.

    This class provides methods to execute specific machine instructions via
    the TCP/IP streamer, abstracting the low-level protocol details.

    :param streamer: TCP/IP communication interface.
    :type streamer: IPStreamer
    """

    def __init__(self, streamer: IPStreamer):
        self.streamer = streamer

    def ad(self) -> str:
        """
        Fault acknowledgment (Acquittement défaut).

        This command is used to acknowledge a fault once the cause has been resolved.

        :return: "AD 1" if the execution is successful.
        :rtype: str
        :raises ValueError: If the machine returns an error code (ER).
        """
        resp = self.streamer.write("AD\r")
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def am(self) -> str:
        """
        Stop marking (Arrêt marquage).

        Stopping a marking process puts the machine into a "Fault" state.
        The fault must then be acknowledged using the AD command.

        :return: "AM 1" if successful.
        :rtype: str
        :raises ValueError: If the machine returns an error code (ER).
        """
        resp = self.streamer.write("AM\r")
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def go(self) -> str:
        """
        Start marking cycle.

        Launches the marking of the file previously loaded with the LD command.
        This method is blocking and monitors the marking status until it pauses (GO P),
        stops due to a fault (GO S), or finishes successfully (GO F).

        :return: The final status of the marking cycle ("GO P", "GO S", or "GO F").
        :rtype: str
        :raises RuntimeError: If the initial marking start confirmation ("GO M") is not received.
        :raises ValueError: If the machine returns an error code (ER).
        """
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
                if resp in ["GO P", "GO S", "GO F"]:
                    return resp
                if resp.startswith("ER"):
                    return check_err(resp)
        finally:
            unlock()

    def gp(self) -> str:
        """
        Get connection type (Master/Slave).

        Checks if the current connection has master or slave privileges.

        :return: A string indicating master status (e.g., 'GP "MASTER":"1"') or slave status ('GP "MASTER":"0"').
        :rtype: str
        :raises ValueError: If the machine returns an error code (ER).
        """
        resp = self.streamer.write('GP "MASTER"\r')
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def ld(self, filename: str, nb_marking: int, mode: LDMode) -> str:
        """
        Load a marking file.

        Loads a T2L file with a specified number of markings and execution mode.

        :param filename: The name of the file to load (case sensitive, .t21 extension optional).
        :type filename: str
        :param nb_marking: Number of markings to perform (0 to 4294967295; 0 for infinite/autonomous).
        :type nb_marking: int
        :param mode: Execution mode (NORMAL, SIMULATION, or AUTONOME).
        :type mode: LDMode
        :return: "LD 1" if the file is loaded successfully.
        :rtype: str
        :raises ValueError: If the machine returns an error code (ER).
        """
        resp = self.streamer.write(f'LD "{filename}" {nb_marking} {mode.value}\r')
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def ls(self, mask: str = None) -> str:
        """
        List files present in the machine.

        Lists files based on an optional mask (using '*' or '?').

        :param mask: Optional filter (e.g., "*.t21" or "CE.103").
        :type mask: str, optional
        :return: The number of files found followed by the list of filenames.
        :rtype: str
        :raises ValueError: If the machine returns an error code (ER).
        """
        cmd = f"LS {mask}\r" if mask else "LS\r"
        resp = self.streamer.write(cmd)
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def pf(self, filename: str, data: bytes) -> str:
        """
        Push a file to the machine's memory.

        Uploads a file (in supported formats) to the machine.

        :param filename: Target filename on the machine.
        :type filename: str
        :param data: Byte list of the file content in hexadecimal representation.
        :type data: bytes
        :return: "PF 1" if the upload is successful.
        :rtype: str
        :raises ValueError: If the machine returns an error code (ER).
        """
        resp = self.streamer.write(f'PF "{filename}" {data}\r')
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def rm(self, mask: str) -> str:
        """
        Remove files from the machine.

        Deletes files matching the specified name or mask.

        :param mask: The filename or mask (e.g., "example.t21" or "*.t21") to delete.
        :type mask: str
        :return: "RM 1" if successful.
        :rtype: str
        :raises ValueError: If the machine returns an error code (ER).
        """
        cmd = f"RM {mask}\r" if mask else "RM\r"
        resp = self.streamer.write(cmd)
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def sp(self, value: bool) -> str:
        """
        Set connection type (Master/Slave).

        Changes the connection type to Master (True) or Slave (False).
        This command is only executable in 'CONTROL UNIT OK' or 'FAULT' states.

        :param value: True to request master status ("1"), False for slave status ("0").
        :type value: bool
        :return: "SP 1" if the change is successful.
        :rtype: str
        :raises ValueError: If the machine returns an error code (ER).
        """
        resp = self.streamer.write(f'SP "MASTER":"{int(value)}"\r')
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def st(self) -> str:
        """
        Get current machine status.

        Returns the state, safety status (rearm), and marking mode.

        :return: A status string (e.g., "ST 4 0 1") where:
                 - State: 1 (Init), 2 (Alive), 4 (Ready), 8 (Marking), 16 (Paused), 32 (Fault).
                 - Rearm: Safety/shutter status.
                 - Markmode: Normal (0), Autonomous (1), or Simulation (2).
        :rtype: str
        :raises ValueError: If the machine returns an error code (ER).
        """
        resp = self.streamer.write(f"ST\r")
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def vg(self, index: int) -> str:
        """
        Get variable value.

        Returns the text contained in the specified variable index.

        :param index: The variable number (0 to 9).
        :type index: int
        :return: The value of the requested variable.
        :rtype: str
        :raises ValueError: If the machine returns an error code (ER).
        """
        resp = self.streamer.write(f"VG {index}\r")
        if resp.startswith("ER"):
            return check_err(resp)
        return resp

    def vs(self, index: int, text: str) -> str:
        """
        Set variable value.

        Assigns text to a specific variable index.

        :param index: The variable number (0 to 9).
        :type index: int
        :param text: The UTF-8 text to store in the variable.
        :type text: str
        :return: "VS 1" followed by the variable number if successful.
        :rtype: str
        :raises ValueError: If the machine returns an error code (ER).
        """
        resp = self.streamer.write(f'VS {index} "{text}"\r')
        if resp.startswith("ER"):
            return check_err(resp)
        return resp
