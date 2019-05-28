# -*- coding: utf-8 -*-

"""
Data models saved in Database. Should update from TS files

"""

import datetime

import json

import os

from io import open
from wordweaver import app

default_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(default_path, 'affixes.json'), 'r') as affix_file:
    affix_data = json.load(affix_file, encoding='utf-8')

with open(os.path.join(default_path, 'pronouns.json'), 'r') as pronoun_file:
    pronoun_data = json.load(pronoun_file, encoding='utf-8')

with open(os.path.join(default_path, 'verbs.json'), 'r') as verb_file:
    verb_data = json.load(verb_file, encoding='utf-8')

