import socket
import threading
import time


HOST = "127.0.0.1"
PORT = 3000


def handle_client(conn, addr):
    print(f"✅ Client connecté : {addr}")

    with conn:
        file = conn.makefile("r")

        while True:
            line = file.readline()
            if not line:
                print("❌ Client déconnecté")
                break

            cmd = line.strip()
            print(f"📥 Reçu : {repr(cmd)}")

            # --- Simulation des commandes Gravotech ---

            if cmd == "ST":
                resp = "ST 4 0 0\n"   # READY
            elif cmd.startswith("LD"):
                resp = "OK\n"
            elif cmd.startswith("VG"):
                resp = "HELLO\n"
            elif cmd.startswith("VS"):
                resp = "OK\n"
            elif cmd.startswith("LS"):
                # Simule 3 fichiers
                resp = "3\nFILE1.T2L\nFILE2.T2L\nTEST.T2L\n"
            elif cmd == "GO":
                # Réponse immédiate : marking started
                conn.sendall(b"GO M\n")

                # Simule le marquage
                time.sleep(2)

                # Message spontané : finished
                conn.sendall(b"GO F\n")
                continue
            else:
                resp = "ERR UNKNOWN COMMAND\n"

            print(f"📤 Envoi : {repr(resp.strip())}")
            conn.sendall(resp.encode("ascii"))


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"🟢 Fake Gravotech Server lancé sur {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
