# -*- coding: utf-8 -*-
from unittest import TestCase
import json
import os
import requests
from jsonpointer import resolve_pointer, set_pointer, JsonPointerException
from slugify import slugify
from wordweaver.resources.affix import AFFIX_OPTIONS
from wordweaver.data.api_data.models import affix_data, pronoun_data, verb_data
from wordweaver.data import swagger
from wordweaver import static
from . import logger

class SwaggerSpecTest(TestCase):
    def setUp(self):
        self.pre_path = os.path.join(os.path.dirname(swagger.__file__), "swagger-pre.json")
        self.static = os.path.join(os.path.dirname(static.__file__), "swagger.json")
        
        with open(self.pre_path, 'r', encoding='utf8') as f:
            self.pre_data = json.load(f)

        with open(self.static, 'r', encoding='utf8') as f:
            self.generated_data = json.load(f)

        # define pointers
        self.servers = resolve_pointer(self.generated_data, '/servers')
        self.vb_pointer = '/components/schemas/VerbTags/enum'
        self.pn_pointer = '/components/schemas/PronounTags/enum'
        self.aff_pointer = '/components/schemas/AffixTags/enum'
        self.affopt_pointer = '/components/schemas/AffOptionTags/enum'
        self.pointers = [self.vb_pointer, self.pn_pointer, self.aff_pointer, self.affopt_pointer]
        
        # define tags from json
        self.vb_tags = sorted(list(set([slugify(x['tag']) for x in verb_data])))
        self.pn_tags = sorted(list(set([slugify(x['tag']) for x in pronoun_data])))
        self.aff_tags = sorted(list(set([slugify(x['tag']) for x in affix_data])))
        aff_options = AFFIX_OPTIONS['AFFIX_OPTIONS']
        self.affopt_tags = sorted(list(set([slugify(x['tag']) for x in aff_options])))

        # define tags in generated data
        self.gen_vb_tags = resolve_pointer(self.generated_data, self.vb_pointer)
        self.gen_pn_tags = resolve_pointer(self.generated_data, self.pn_pointer)
        self.gen_aff_tags = resolve_pointer(self.generated_data, self.aff_pointer)
        self.gen_affopt_tags = resolve_pointer(self.generated_data, self.affopt_pointer)

    def test_pointers_exist_in_pre(self):
        '''
        Check pointers are valid in pre-generated data.
        '''
        with self.assertRaises(JsonPointerException):
            resolve_pointer(self.pre_data, '/foo/bar')
        self.assertTrue(all(type(data) == list for data in [resolve_pointer(self.pre_data, pointer) for pointer in self.pointers]))

    def test_pointers_exist_in_generated(self):
        '''
        Check pointers are valid in generated data.
        '''
        with self.assertRaises(JsonPointerException):
            resolve_pointer(self.generated_data, '/foo/bar')
        self.assertTrue(all(type(data) == list for data in [resolve_pointer(self.generated_data, pointer) for pointer in self.pointers]))

    def test_spec_and_json_equal(self):
        ''' 
        Check that the generated spec sheet has all tags found in json files and vice versa.
        '''
        self.assertTrue(all([True if tag in self.vb_tags else logger.warn("The verb tag " + tag + " is in the spec sheet, but doesn't exist in the json file. Please run 'fab spec'.") for tag in self.gen_vb_tags]))
        self.assertTrue(all([True if tag in self.pn_tags else logger.warn("The pronoun tag " + tag + " is in the spec sheet, but doesn't exist in the json file. Please run 'fab spec'.") for tag in self.gen_pn_tags]))
        self.assertTrue(all([True if tag in self.aff_tags else logger.warn("The affix tag " + tag + " is in the spec sheet, but doesn't exist in the json file. Please run 'fab spec'.") for tag in self.gen_aff_tags]))
        self.assertTrue(all([True if tag in self.affopt_tags else logger.warn("The affix option tag " + tag + " is in the spec sheet, but doesn't exist in the json file. Please run 'fab spec'.") for tag in self.gen_affopt_tags]))
        self.assertTrue(all([True if tag in self.gen_vb_tags else logger.warn("The verb tag " + tag + " is in the json file, but wasn't generated. Please run 'fab spec'.") for tag in self.vb_tags]))
        self.assertTrue(all([True if tag in self.gen_pn_tags else logger.warn("The pronoun tag " + tag + " is in the json file, but wasn't generated. Please run 'fab spec'.") for tag in self.pn_tags]))
        self.assertTrue(all([True if tag in self.gen_aff_tags else logger.warn("The affix tag " + tag + " is in the json file, but wasn't generated. Please run 'fab spec'.") for tag in self.aff_tags]))
        self.assertTrue(all([True if tag in self.gen_affopt_tags else logger.warn("The affix option tag " + tag + " is in the json file, but wasn't generated. Please run 'fab spec'.") for tag in self.affopt_tags]))

