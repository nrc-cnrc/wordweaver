import json
import os
from wordweaver.log import logger
from wordweaver import __file__ as ww_file

data_dir = os.environ.get('WW_DATA_DIR')

if not data_dir:
    logger.warn('WW_DATA_DIR environment variable is not set, using default sample data instead.')
    data_dir = os.path.join(os.path.dirname(ww_file), 'sample', 'data')

with open(os.path.join(data_dir, 'api_data', 'affixes.json'), encoding='utf-8') as affix_file:
    affix_data = json.load(affix_file, encoding='utf-8')

with open(os.path.join(data_dir, 'api_data', 'pronouns.json'), encoding='utf-8') as pronoun_file:
    pronoun_data = json.load(pronoun_file, encoding='utf-8')

with open(os.path.join(data_dir, 'api_data', 'verbs.json'), encoding='utf-8') as verb_file:
    verb_data = json.load(verb_file, encoding='utf-8')

