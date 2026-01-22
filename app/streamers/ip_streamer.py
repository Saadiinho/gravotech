import threading
import socket
import time
from typing import Optional, Callable


class IPStreamer:
    def __init__(self, ip: str, port: int, timeout: float = 5.0):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.max_attempts = 5
        self.sock: Optional[socket.socket] = None
        self.mu = threading.RLock()
        self.connect()

    def connect(self):
        """Ouvre la connexion TCP/IP"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10)
            self.sock.connect((self.ip, self.port))
            self.sock.settimeout(self.timeout)
            print(f"✅ Connected to {self.ip}:{self.port}")
        except Exception as e:
            self.close()
            raise RuntimeError(f"Connection to {self.ip}:{self.port} failed") from e

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None
        print(f"Closing connection to {self.ip}:{self.port}")

    def retry(self, max_attempts: int = 3, delay: float = 1.0) -> bool:
        """Tente de se reconnecter avec backoff exponentiel"""
        self.close()
        for attempt in range(1, max_attempts + 1):
            try:
                self.connect()
                return True
            except Exception as e:
                if attempt < max_attempts:
                    wait_time = delay * (2 ** (attempt - 1))
                    time.sleep(wait_time)
                else:
                    raise RuntimeError(
                        f"Unable to reconnect after {max_attempts} attempts"
                    ) from e
        return False

    def lock(self) -> Callable[[], None]:
        """
        Prend le lock et retourne une fonction pour le relâcher.
        Usage:
            unlock = streamer.lock()
            try:
                streamer.unsafe_write("GO")
                resp = streamer.unsafe_read()
            finally:
                unlock()
        """
        self.mu.acquire()
        return lambda: self.mu.release()

    # ========================================================================
    # MÉTHODES INTERNES (sans lock, sans retry)
    # ========================================================================

    def _read_line(self) -> str:
        """Lit une ligne en gérant \\r\\n correctement"""
        if self.sock is None:
            raise RuntimeError("Not connected")

        buffer = b""
        while True:
            char = self.sock.recv(1)
            if not char:  # Connexion fermée
                raise RuntimeError("Connection closed by remote host")
            if char == b"\n":
                break
            if char != b"\r":
                buffer += char
        return buffer.decode("ascii")

    def _write_cmd(self, cmd: str) -> None:
        """Envoie une commande (sans lire la réponse)"""
        if not cmd.endswith("\r"):
            cmd += "\r"

        if self.sock is None:
            raise RuntimeError("Not connected")

        try:
            self.sock.sendall(cmd.encode("ascii"))
        except (socket.timeout, ConnectionResetError, BrokenPipeError) as e:
            raise RuntimeError("Network error during write") from e

    def _read_ls_response(self) -> str:
        """Lit la réponse multi-ligne de LS"""
        nb_files_str = self._read_line()

        try:
            nb_files = int(nb_files_str)
        except ValueError:
            # Probablement une erreur, retourner telle quelle
            return nb_files_str

        lines = [nb_files_str]
        for _ in range(nb_files):
            filename = self._read_line()
            lines.append(filename)

        return "\n".join(lines)

    # ========================================================================
    # MÉTHODES UNSAFE (à utiliser avec lock())
    # ========================================================================

    def unsafe_write(self, cmd: str) -> None:
        """Envoie une commande SANS prendre le lock, SANS lire la réponse"""
        self._write_cmd(cmd)

    def unsafe_read(self, timeout: Optional[float] = None) -> str:
        """Lit une ligne SANS prendre le lock"""
        if timeout is not None:
            old_timeout = self.sock.gettimeout()
            self.sock.settimeout(timeout)

        try:
            return self._read_line()
        finally:
            if timeout is not None:
                self.sock.settimeout(old_timeout)

    # ========================================================================
    # MÉTHODES THREAD-SAFE (avec lock et retry)
    # ========================================================================

    def read(self) -> str:
        """Lit une ligne (thread-safe)"""
        with self.mu:
            return self._read_line()

    def write(self, cmd: str) -> str:
        """
        Envoie une commande et lit la réponse immédiate.
        Thread-safe avec retry automatique.
        """
        with self.mu:
            try:
                return self._write_and_read(cmd)
            except (socket.timeout, ConnectionResetError, BrokenPipeError) as e:
                print(f"⚠️ Network error: {e}, attempting retry...")
                self.retry()
                return self._write_and_read(cmd)

    def _write_and_read(self, cmd: str) -> str:
        """Envoie une commande et lit la réponse (interne, pas de lock)"""
        self._write_cmd(cmd)

        # Gestion spéciale pour LS
        if cmd.strip().upper().startswith("LS"):
            return self._read_ls_response()

        return self._read_line()

    def read_ls(self) -> str:
        """Lit une réponse LS (thread-safe) - DEPRECATED, utiliser write("LS")"""
        with self.mu:
            return self._read_ls_response()
