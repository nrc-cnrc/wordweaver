# -*- coding: utf-8 -*-

import json

import os
from jsonpointer import resolve_pointer, set_pointer
from slugify import slugify
from wordweaver.resources.affix import AFFIX_OPTIONS
from wordweaver.data import affix_data, pronoun_data, verb_data
from wordweaver import static
from wordweaver.config import BUILD_CONFIG
from wordweaver.app import app
from wordweaver.log import logger
from wordweaver import __file__ as ww_file

data_dir = os.environ.get('WW_DATA_DIR')

if not data_dir:
    logger.warn('WW_DATA_DIR environment variable is not set, using default sample data instead.')
    data_dir = os.path.join(os.path.dirname(ww_file), 'sample', 'data')

swagger_dir = os.path.join(os.path.abspath(data_dir), 'swagger')

class SwaggerSpecGenerator():
    def __init__(self):
        self.pre_path = os.path.join(swagger_dir, BUILD_CONFIG['pre'])
        self.post_path = os.path.join(os.path.dirname(static.__file__), BUILD_CONFIG['post'])
        with open(self.pre_path, 'r', encoding='utf8') as f:
            self.data = json.load(f)

        # define pointers
        self.vb_pointer = BUILD_CONFIG['pointers']['vb']
        self.pn_pointer = BUILD_CONFIG['pointers']['pn']
        self.aff_pointer = BUILD_CONFIG['pointers']['aff']
        self.affopt_pointer = BUILD_CONFIG['pointers']['ao']

        # define tags
        self.vb_tags = sorted(list(set([slugify(x['tag']) for x in verb_data])))
        self.pn_tags = sorted(list(set([slugify(x['tag']) for x in pronoun_data])))
        self.aff_tags = sorted(list(set([slugify(x['tag']) for x in affix_data])))
        aff_options = AFFIX_OPTIONS['AFFIX_OPTIONS']
        self.affopt_tags = sorted(list(set([slugify(x['tag']) for x in aff_options])))

    # set pointers and return new data 
    def setPointers(self):
        set_pointer(self.data, self.vb_pointer, self.vb_tags)
        set_pointer(self.data, self.pn_pointer, self.pn_tags)
        set_pointer(self.data, self.aff_pointer, self.aff_tags)
        set_pointer(self.data, self.affopt_pointer, self.affopt_tags)
        return self.data

    def writeNewData(self):
        set_pointer(self.data, self.vb_pointer, self.vb_tags)
        set_pointer(self.data, self.pn_pointer, self.pn_tags)
        set_pointer(self.data, self.aff_pointer, self.aff_tags)
        set_pointer(self.data, self.affopt_pointer, self.affopt_tags)
        with open(self.post_path, 'w') as f:
            json.dump(self.data, f)
