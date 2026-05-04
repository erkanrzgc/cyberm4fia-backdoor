import json
import os


def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    defaults = {
        'server_host': '127.0.0.1',
        'server_port': 5555,
        'reconnect_interval': 5
    }
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        defaults.update(config)
    except Exception:
        pass
    return defaults
