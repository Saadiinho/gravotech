import threading
import socket
import time


class IPStreamer:
    def __init__(self, ip:str, port: int, timeout: float = 5.0):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.max_attempts = 10
        self.sock = None
        self.mu = threading.RLock()
        self.file = None

    def connect(self):
        """Ouvre la connexion TCP/IP"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10)
            self.sock.connect((self.ip, self.port))
            self.sock.settimeout(self.timeout)
            self.file = self.sock.makefile("r", encoding="ascii")
            print("Connected to {}:{}".format(self.ip, self.port))
        except Exception as e:
            self.close()
            raise RuntimeError(f"Connection to {self.ip}:{self.port} failed") from e

    def close(self):
        if self.file:
            try:
                self.file.close()
            except Exception:
                pass
            self.file = None

        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None
        print("Closing connection to {}:{}".format(self.ip, self.port))

    def retry(self):
        """Permet de réessayer de se connecter à la connexion TCP/IP"""
        self.close()
        for attempt in range(1, self.max_attempts + 1):
            try:
                self.connect()
                return True
            except Exception as e:
                if attempt < self.max_attempts:
                    delay = 1
                    time.sleep(delay)
                    delay *= 2
                else:
                    raise RuntimeError(f"Connection to {self.ip}:{self.port} failed") from e
        return None

    def write(self, cmd: str) -> str:
        if not cmd.endswith("\r"):
            cmd += "\r"
        with self.mu:
            try:
                self.sock.sendall(cmd.encode("ascii"))
            except (socket.timeout, ConnectionResetError) as e:
                raise RuntimeError("Network error during write") from e
        if cmd.startswith("LS"):
            return self.read_ls()
        return self.read()

    def read(self):
        with self.mu:
            buffer = b""
            while True:
                char = self.sock.recv(1)
                if char == b"\r":
                    continue
                if char == b"\n":
                    break
                buffer += char
            return buffer.decode("ascii")

    def read_ls(self) -> str:
        with self.mu:
            nb_files_str = self.read()
            try:
                nb_files = int(nb_files_str)
            except ValueError:
                raise RuntimeError(f"Invalid LS response: expected number, got '{nb_files_str}'")
            files = [nb_files_str]
            for _ in range(nb_files):
                filename = self.read()
                files.append(filename)

            return "\n".join(files)