# -*- coding: utf-8 -*-

""" Test all things related to affixes
"""

from unittest import TestCase
from itertools import chain

from slugify import slugify

from wordweaver.resources.affix import AFFIX_OPTIONS
from wordweaver.config import LANG_CONFIG
from wordweaver.data import affix_data
from wordweaver.log import logger

class AffixTest(TestCase):
    """
    This tests the following assumptions:

    - New affixes must be added to $WW_DATA_DIR/api_data/affixes.json
    / and $WW_CONFIG_DIR/lang_config.yaml and their tags must be valid slugs
    / and they must match.

    - For affix options to be made available, they must be declared in
    / $WW_CONFIG_DIR/lang_config.yaml and use only valid affix tags as
    / defined above

    """
    def setUp(self):
        self.affix_data = affix_data
        self.affix_tags = [affix['tag'] for affix in self.affix_data]
        self.interface_affix_tags = list(LANG_CONFIG['affixes']['tmp_affix'].keys(
        )) + list(LANG_CONFIG['affixes']['aspect'].keys()) + list(LANG_CONFIG['affixes']['post_aspectual_suffix'].keys())
        self.affix_options = AFFIX_OPTIONS['AFFIX_OPTIONS']
        self.aff_options_tags = [x['tag'] for x in self.affix_options]
        self.aff_options_affix_tags = chain.from_iterable([x['affixes'] for x in self.affix_options])

    def test_duplicate_affixes(self):
        '''
        Ensure no duplicate tags
        '''
        self.assertTrue(len(self.affix_data) == len(list(set(self.affix_tags))))

    def test_duplicate_affopts(self):
        '''
        Ensure no duplicate tags
        '''
        self.assertTrue(len(self.aff_options_tags) == len(list(set(self.aff_options_tags))))

    def test_all_affixes_have_tags(self):
        '''
        All affixes defined in wordweaver/data/api_data/affixes.json should have a value for tag
        '''
        self.assertTrue(all(affix['tag'] for affix in self.affix_data))

    def test_fst_constants(self):
        '''
        All affix constants declared in wordweaver/fst/fst_constants.py should exist in
        wordweaver/data/api_data/affix.json
        '''
        self.assertTrue(
            all([tag in self.affix_tags for tag in self.interface_affix_tags]))
        self.assertFalse('foobar' in self.affix_tags)
        self.assertFalse('foobar' in self.interface_affix_tags)

    def test_aff_options(self):
        '''
        All affix option constituent affix tags declared in wordweaver/resources/affix.py should exist in
        wordweaver/data/api_data/affix.json
        '''
        self.assertTrue(
            all([tag in self.affix_tags for tag in self.aff_options_affix_tags]))
        self.assertFalse('foobar' in self.affix_tags)
        self.assertFalse('foobar' in self.aff_options_tags)

    def test_affix_slugs(self):
        '''
        All affix tags should be properly formed slugs
        '''
        for x in self.affix_data:
            try:
                self.assertTrue(x['tag'] == slugify(x['tag']))
            except AssertionError:
                logger.error("The tag " + x['tag'] + " does not equal its slugified version " + slugify(x['tag']) )
    
    def test_aff_option_slugs(self):
        '''
        All affix option tags should be properly formed slugs
        '''
        self.assertTrue(
            all([tag == slugify(tag) for tag in self.aff_options_tags]))

    def test_affopt_types(self):
        '''
        Affix options must have one aspect, 0 or 1 temporal affix and 0 or 1 post aspectual suffix
        '''
        for affopt in self.affix_options:
            types = [x['type'] for x in affopt['affixes']]
            self.assertTrue(len([t for t in types if t == 'aspect']) == 1)
            self.assertTrue(len([t for t in types if t == 'tmp_affix']) <= 1)
            self.assertTrue(len([t for t in types if t == 'post_aspectual_suffix']) <= 1)
           
    

