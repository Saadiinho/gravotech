import threading
import socket


class IPStreamer:
    def __init__(self, ip:str, port: int, timeout: float = 2.0):
        self.ip = ip
        self.port = port
        self.timeout = timeout

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
        pass

    def write(self, cmd: str) -> str:
        if not cmd.endswith("\r"):
            cmd += "\r"
        with self.mu:
            try:
                self.sock.sendall(cmd.encode("ascii"))
                print(f"Message sent: {cmd}")
                resp = self.file.readline()
                print(f"Message received: {resp.strip()}")
            except (socket.timeout, ConnectionResetError) as e:
                raise RuntimeError("Network error during write") from e

    def read(self):
        pass
