import json

recv_buffer = b''


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


def reliable_send(sock, data):
    jsondata = json.dumps(data)
    sock.send(jsondata.encode() + b'\n')
