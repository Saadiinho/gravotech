from time import sleep

from gravotech.streamers.ip_streamer import IPStreamer

__version__ = "1.0.0"

HOST = "127.0.0.1"
PORT = 3000

ip_streamer = IPStreamer(HOST, PORT)

if __name__ == "__main__":
    ip_streamer.connect()
    sleep(5)
    ip_streamer.close()