import json
import os

default_path = os.environ.get('WW_DATA_DIR')

with open(os.path.join(default_path, 'api_data', 'affixes.json'), encoding='utf-8') as affix_file:
    affix_data = json.load(affix_file, encoding='utf-8')

with open(os.path.join(default_path, 'api_data', 'pronouns.json'), encoding='utf-8') as pronoun_file:
    pronoun_data = json.load(pronoun_file, encoding='utf-8')

with open(os.path.join(default_path, 'api_data', 'verbs.json'), encoding='utf-8') as verb_file:
    verb_data = json.load(verb_file, encoding='utf-8')

