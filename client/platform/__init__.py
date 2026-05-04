import os
from client.platform.windows import WindowsPlatform
from client.platform.linux import LinuxPlatform


def get_platform():
    if os.name == 'nt':
        return WindowsPlatform()
    return LinuxPlatform()
