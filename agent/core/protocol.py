import json
import threading

send_lock = threading.Lock()
recv_buffer = b''


def reliable_send(sock, data):
    jsondata = json.dumps(data)
    with send_lock:
        sock.send(jsondata.encode() + b'\n')


def reliable_recv(sock):
    global recv_buffer
    while True:
        try:
            if b'\n' in recv_buffer:
                message, recv_buffer = recv_buffer.split(b'\n', 1)
                return json.loads(message.decode())

            chunk = sock.recv(8192)
            if not chunk:
                raise ConnectionError("Connection closed")
            recv_buffer += chunk

        except (ValueError, UnicodeDecodeError):
            continue
