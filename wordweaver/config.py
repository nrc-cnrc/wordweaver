import yaml
import os
from wordweaver.app import app

config_dir = app.config['CONFIG_DIR']

with open(os.path.join(os.path.abspath(config_dir), 'build_config.yaml'), 'r') as stream:
    try:
        BUILD_CONFIG = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

with open(os.path.join(os.path.abspath(config_dir), 'interface_config.yaml'), 'r') as stream:
    try:
        INTERFACE_CONFIG = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

with open(os.path.join(os.path.abspath(config_dir), 'lang_config.yaml'), 'r') as stream:
    try:
        LANG_CONFIG = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)