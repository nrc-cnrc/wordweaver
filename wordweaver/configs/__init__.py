import os
import yaml
from wordweaver.configs import __file__ as config_dir

BUILD_CONFIG_PATH = os.path.join(os.path.dirname(config_dir), 'build_config.yaml')
ENV_CONFIG_PATH = os.path.join(os.path.dirname(config_dir), 'env_config.yaml')
INTERFACE_CONFIG_PATH = os.path.join(os.path.dirname(config_dir), 'interface_config.yaml')
LANG_CONFIG_PATH = os.path.join(os.path.dirname(config_dir), 'lang_config.yaml')

with open(BUILD_CONFIG_PATH, 'r') as stream:
    try:
        BUILD_CONFIG = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

with open(ENV_CONFIG_PATH, 'r') as stream:
    try:
        ENV_CONFIG = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

with open(INTERFACE_CONFIG_PATH, 'r') as stream:
    try:
        INTERFACE_CONFIG = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

with open(LANG_CONFIG_PATH, 'r') as stream:
    try:
        LANG_CONFIG = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
