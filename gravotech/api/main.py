from gravotech.core.gravotech import Gravotech

__version__ = "1.0.0"

HOST = "127.0.0.1"
PORT = 3000

graveuse = Gravotech(HOST, PORT)

if __name__ == "__main__":
    print(graveuse.Actions.ls())
