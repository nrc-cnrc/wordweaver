# -*- coding: utf-8 -*-

""" Test verb data
"""

from unittest import TestCase
import json
import os

from slugify import slugify

from wordweaver.data import verb_data

from wordweaver.data import data_dir
from wordweaver.log import logger

class VerbTest(TestCase):
    def setUp(self):
        default_data_path = os.path.join(data_dir, 'api_data')
        with open(os.path.join(default_data_path, 'verbs.json'), 'r') as verb_file:
            self.verb_data = json.load(verb_file, encoding='utf-8')

    def test_duplicates(self):
        '''
        Ensure no duplicate tags
        '''
        print(len(verb_data))
        print(len(list(set([v['tag'] for v in self.verb_data]))))
        import collections
        print(collections.Counter([v['tag'] for v in self.verb_data]))
        self.assertTrue(len(verb_data) == len(list(set([v['tag'] for v in self.verb_data]))))
    
    def test_all_verbs_have_tags(self):
        '''
        All verbs defined in wordweaver/data/api_data/verbs.json should have a value for tag
        '''
        self.assertTrue(all(v['tag'] for v in self.verb_data))

    def test_verb_slugs(self):
        '''
        All tags should be properly formed slugs
        '''
        for v in self.verb_data:
            try:
                self.assertTrue(v['tag'] == slugify(v['tag']))
            except AssertionError:
                logger.error("The tag " + v['tag'] + " does not equal its slugified version " + slugify(v['tag']) )
