import socket
import threading
import time

import logging

HOST = "0.0.0.0"
PORT = 3000


def handle_client(conn, addr):
    logger.logger.info()
    with conn:
        while True:
            buffer = b""
            while True:
                try:
                    byte = conn.recv(1)
                    if not byte:
                        logger.logger.debug(f"Client disconnect: {addr}")
                        return
                    buffer += byte
                    if byte == b"\r":
                        break
                except Exception:
                    logger.error(f"reading error")
                    return
            try:
                cmd_str = buffer.decode("ascii").rstrip("\r")
            except UnicodeDecodeError:
                conn.sendall(b"ERR INVALID ENCODING\r\n")
                continue

            logger.logger.info(f"Receive: {repr(cmd_str)}")

            if cmd_str == "ST":
                resp = "ST 4 0 0\r\n"
            elif cmd_str.startswith("LS"):
                resp = "3\r\nFILE1.T2L\r\nFILE2.T2L\r\nTEST.T2L\r\n"
            elif cmd_str == "GO":
                conn.sendall(b"GO M\r\n")
                time.sleep(2)
                conn.sendall(b"GO F\r\n")
                continue
            else:
                resp = "ERR UNKNOWN COMMAND\r\n"

            logger.logger.info(f"Send: {repr(resp.strip())}")
            conn.sendall(resp.encode("ascii"))


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        logger.logger.info(f"Fake Gravotech Server launch on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(
                target=handle_client, args=(conn, addr), daemon=True
            ).start()



if __name__ == "__main__":
    main()
