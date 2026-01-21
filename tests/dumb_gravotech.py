import socket
import threading
import time


HOST = "127.0.0.1"
PORT = 3000


def handle_client(conn, addr):
    print(f"✅ Client connecté : {addr}")
    with conn:
        while True:
            # Lire caractère par caractère jusqu'à \r
            buffer = b""
            while True:
                try:
                    byte = conn.recv(1)
                    if not byte:
                        print("❌ Client déconnecté")
                        return
                    buffer += byte
                    if byte == b"\r":
                        break  # Fin de commande détectée
                except Exception:
                    print("❌ Erreur de lecture")
                    return

            # Décoder la commande (ASCII uniquement selon la doc)
            try:
                cmd_str = buffer.decode("ascii").rstrip("\r")
            except UnicodeDecodeError:
                conn.sendall(b"ERR INVALID ENCODING\r\n")
                continue

            print(f"📥 Reçu : {repr(cmd_str)}")

            # Traitement des commandes
            if cmd_str == "ST":
                resp = "ST 4 0 0\r\n"
            elif cmd_str.startswith("LS"):
                resp = "3\r\nFILE1.T2L\r\nFILE2.T2L\r\nTEST.T2L\r\n"
            elif cmd_str == "GO":
                conn.sendall(b"GO M\r\n")
                time.sleep(2)
                conn.sendall(b"GO F\r\n")
                continue  # Pas de réponse finale unique → on boucle directement
            else:
                resp = "ERR UNKNOWN COMMAND\r\n"

            print(f"📤 Envoi : {repr(resp.strip())}")
            conn.sendall(resp.encode("ascii"))


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"🟢 Fake Gravotech Server lancé sur {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()