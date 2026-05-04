import socket

from server.ui.banner import print_gradient_banner
from server.ui.prompt import print_colored


def start_listener(host, port, session_callback):
    print_gradient_banner()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)
    print_colored('[+] Listening For The Incoming Connections', 'green')

    try:
        while True:
            target, ip = sock.accept()
            target.settimeout(None)
            print_colored(f'[+] Target Connected From: {ip}', 'green')

            try:
                session_callback(target, ip)
            except Exception as e:
                print_colored(f'[-] Connection Lost: {str(e)}', 'red')

            try:
                target.close()
            except Exception:
                pass

            print_colored('[*] Waiting for new connection...', 'yellow')

    except KeyboardInterrupt:
        print_colored('\n[-] Exiting Server...', 'red')
        sock.close()
