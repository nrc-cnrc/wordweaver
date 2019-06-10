import yaml
import os
from wordweaver.log import logger
from wordweaver import __file__ as ww_file

config_dir = os.environ.get('WW_CONFIG_DIR')

if not config_dir:
    logger.warn('WW_CONFIG_DIR environment variable is not set, using default sample configs instead.')
    config_dir = os.path.join(os.path.dirname(ww_file), 'sample', 'configs')

with open(os.path.join(os.path.abspath(config_dir), 'env_config.yaml'), encoding='utf-8') as stream:
    try:
        ENV_CONFIG = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

with open(os.path.join(os.path.abspath(config_dir), 'build_config.yaml'), encoding='utf-8') as stream:
    try:
        BUILD_CONFIG = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

with open(os.path.join(os.path.abspath(config_dir), 'interface_config.yaml'), encoding='utf-8') as stream:
    try:
        INTERFACE_CONFIG = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

with open(os.path.join(os.path.abspath(config_dir), 'lang_config.yaml'), encoding='utf-8') as stream:
    try:
        LANG_CONFIG = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)