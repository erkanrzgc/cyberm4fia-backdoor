import os
import base64

from server.core.protocol import reliable_recv, reliable_send
from server.ui.prompt import print_colored


def upload_file(sock, file_name):
    try:
        with open(file_name, 'rb') as f:
            reliable_send(sock, base64.b64encode(f.read()).decode())
    except Exception as e:
        print_colored(f'[-] Error uploading file: {str(e)}', 'red')


def download_file(sock, file_name):
    try:
        result = reliable_recv(sock)
        if isinstance(result, str) and result.startswith('[-]'):
            print_colored(result, 'red')
            return

        with open(file_name, 'wb') as f:
            f.write(base64.b64decode(result))
        print_colored(f'[+] File saved: {file_name}', 'green')
    except Exception as e:
        print_colored(f'[-] Error downloading file: {str(e)}', 'red')
