import yaml
import os

config_dir = os.environ.get('WW_CONFIG_DIR')

with open(os.path.join(os.path.abspath(config_dir), 'env_config.yaml'), 'r') as stream:
    try:
        ENV_CONFIG = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

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