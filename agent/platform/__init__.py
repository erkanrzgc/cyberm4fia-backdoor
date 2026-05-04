import os
from agent.platform.windows import WindowsPlatform
from agent.platform.linux import LinuxPlatform


def get_platform():
    if os.name == 'nt':
        return WindowsPlatform()
    return LinuxPlatform()
