# -*- coding: utf-8 -*-

""" Test Pronoun data
"""

from unittest import TestCase
import json
import os

from slugify import slugify

from wordweaver.data import data_dir
from wordweaver.log import logger

class PronounTest(TestCase):
    def setUp(self):
        default_data_path = os.path.join(data_dir, 'api_data')
        with open(os.path.join(default_data_path, 'pronouns.json'), 'r') as f:
            self.pronoun_data = json.load(f, encoding='utf-8')

    def test_duplicates(self):
        '''
        Ensure no duplicate tags
        '''
        self.assertTrue(len(self.pronoun_data) == len(list(set([pn['tag'] for pn in self.pronoun_data]))))

    def test_all_pronouns_have_tags(self):
        '''
        All pronouns defined in $WW_DATA_DIR/api_data/pronouns.json should have a value for tag
        '''
        self.assertTrue(all(pn['tag'] for pn in self.pronoun_data))

    def test_pn_slugs(self):
        '''
        All pronoun tags should be properly formed slugs
        '''
        for x in self.pronoun_data:
            try:
                self.assertTrue(x['tag'] == slugify(x['tag']))
            except AssertionError:
                logger.error("The tag " + x['tag'] + " does not equal its slugified version " + slugify(x['tag']) )
