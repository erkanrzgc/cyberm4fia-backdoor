from abc import ABC, abstractmethod


class AbstractPlatform(ABC):

    @abstractmethod
    def list_dir_cmd(self, path=None):
        ...

    @abstractmethod
    def current_dir_cmd(self):
        ...

    @abstractmethod
    def delete_cmd(self, path, recursive=False):
        ...

    @abstractmethod
    def move_cmd(self, src, dst):
        ...

    @abstractmethod
    def read_file_cmd(self, path):
        ...

    @abstractmethod
    def touch_cmd(self, path):
        ...

    @abstractmethod
    def process_list_cmd(self):
        ...

    @abstractmethod
    def kill_process_cmd(self, pid):
        ...

    @abstractmethod
    def network_info_cmd(self):
        ...

    @abstractmethod
    def install_persistence(self, reg_name, copy_name):
        ...

    @abstractmethod
    def get_appdata_path(self):
        ...

    @abstractmethod
    def check_admin(self):
        ...

    @abstractmethod
    def get_system_user(self):
        ...

    @abstractmethod
    def get_memory_info(self):
        ...

    @abstractmethod
    def grep_cmd(self, pattern):
        ...

    @abstractmethod
    def clear_screen_cmd(self):
        ...
