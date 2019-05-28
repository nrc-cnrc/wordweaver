from unittest import TestCase
import re
import os
from jsonpointer import resolve_pointer
import json
from wordweaver import app
from wordweaver.data.api_data.models import affix_data, pronoun_data, verb_data
from wordweaver.resources.affix import AFFIX_OPTIONS
from wordweaver import static
from wordweaver.data import swagger
import requests
import logging
from .. import logger


class ResourceIntegrationSpecificErrorTest(TestCase):
    """
    This tests language specific malformed requests.  
    """
    
    def setUp(self):
         # Swagger
        self.timeout = 5
        self.pre_path = os.path.join(os.path.dirname(swagger.__file__), "swagger-pre.json")
        self.static = os.path.join(os.path.dirname(static.__file__), "swagger.json")
        self.prefix = '/api/v1'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        with open(self.pre_path, 'r', encoding='utf8') as f:
            self.pre_data = json.load(f)
        with open(self.static, 'r', encoding='utf8') as f:
            self.generated_data = json.load(f)
        
        # example data
        self.all_affix_tags = [x['tag'] for x in affix_data]
        affix_options = AFFIX_OPTIONS['AFFIX_OPTIONS']
        self.all_affopt_tags = [x['tag'] for x in affix_options]
        self.all_pronoun_tags = [x['tag'] for x in pronoun_data]
        self.first_pers_tag = [tag for tag in self.all_pronoun_tags if '1' in tag][0]
        self.all_red_verb_tags = [x['tag'] for x in verb_data if 'red' == x['thematic_relation']]
        self.all_blue_verb_tags = [x['tag'] for x in verb_data if 'blue' == x['thematic_relation']]
        self.command_tag = "command"

        # define pointers
        self.servers = [s['url'] for s in resolve_pointer(self.generated_data, '/servers')]
        self.route = '/conjugations'
    
    def test_wrong_theta_role(self):
        '''
        If agent combined with blue verb, or patient combined with red verb,
        response should be a 400
        '''
        blue_params = {'verb': self.all_blue_verb_tags[0], 'aff-option': 'defpast',
                       'agent': self.first_pers_tag}
        red_params = {'verb': self.all_red_verb_tags[0], 'aff-option': 'defpast',
                      'patient': self.first_pers_tag}
        for host in self.servers:
            try:
                r_blue = requests.get(host + self.route, params=blue_params, headers=self.headers)
                self.assertEqual(r_blue.status_code, 400)
                logger.info("Request to " + r_blue.url +  " returned " + str(r_blue.status_code))
            except Exception as e:
                logger.error("Request to " + host + self.route +  f" returned {e}")
            try:
                r_red = requests.get(host + self.route, params=red_params, headers=self.headers)
                self.assertEqual(r_red.status_code, 400)
                logger.info("Request to " + r_red.url +  " returned " + str(r_red.status_code))
            except Exception as e:
                logger.error("Request to " + host + self.route +  f" returned {e}")
                
    
    def test_wrong_person_with_command(self):
        '''
        If anything other than 2nd person is used with command,
        response should be a 400 **this is unclear, and TBD. Currently returns nothing**
        '''
        params = {'verb': self.all_blue_verb_tags[0], 'aff-option': self.command_tag,
                  'patient': self.first_pers_tag}
        
        for host in self.servers:
            try:
                r = requests.get(host + self.route, params=params, headers=self.headers)
                self.assertEqual(r.status_code, 400)
                logger.info("Request to " + r.url + " returned " + str(r.status_code))
            except Exception as e:
                logger.warning("Request to " + host + self.route + " returned " + str(e))
