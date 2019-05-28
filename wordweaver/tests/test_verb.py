from unittest import TestCase
import os
import json
from wordweaver.data.api_data.models import verb_data
from wordweaver.fst.fst_constants import verb_tense, verb_aspect, verb_post_aspectual_suffix
from slugify import slugify
from wordweaver.data import api_data
from . import logger



class VerbTest(TestCase):
    def setUp(self):
        default_data_path = os.path.dirname(os.path.realpath(api_data.__file__))
        with open(os.path.join(default_data_path, 'verbs.json'), 'r') as verb_file:
            self.verb_data = json.load(verb_file, encoding='utf-8')

    def test_duplicates(self):
        '''
        Ensure no duplicate tags
        '''
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
