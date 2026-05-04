import json
import os


def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    defaults = {
        'bind_host': '0.0.0.0',
        'bind_port': 5555,
        'loot_dir': './loot'
    }
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        defaults.update(config)
    except Exception:
        pass
    return defaults
