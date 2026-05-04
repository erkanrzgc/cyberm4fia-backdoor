import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.core.config import load_config
from server.core.listener import start_listener
from server.core.session import run_session


def main():
    config = load_config()

    def session_callback(sock, ip):
        loot_dir = config.get('loot_dir', './loot')
        run_session(sock, ip, loot_dir)

    start_listener(config['bind_host'], config['bind_port'], session_callback)


if __name__ == '__main__':
    main()
