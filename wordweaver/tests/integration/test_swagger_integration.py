# -*- coding: utf-8 -*-

""" Checks that Swagger Spec endpoints are valid
"""

from unittest import TestCase
import json
import os

from jsonpointer import resolve_pointer
import requests

from wordweaver.data import pronoun_data, affix_data, verb_data
from wordweaver.resources.affix import AFFIX_OPTIONS
from wordweaver.data import data_dir
from wordweaver.log import logger
from wordweaver import static

class SwaggerSpecIntegrationTest(TestCase):
    def setUp(self):
        # Swagger
        self.timeout = 5
        self.pre_path = os.path.join(data_dir, 'swagger', "swagger-pre.json")
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
        self.all_verb_tags = [x['tag'] for x in verb_data]

        # define pointers
        self.servers = [s['url'] for s in resolve_pointer(self.generated_data, '/servers')]
        self.route_pointer = '/paths'
        self.routes = resolve_pointer(self.generated_data, self.route_pointer).keys()
        self.routes_with_args = [self.insert_example_arg(x) for x in self.routes]
    
    def insert_example_arg(self, url):
        return url.format(verbTag=self.all_verb_tags[0], pronounTag=self.all_pronoun_tags[0],
                          affixTag=self.all_affix_tags[0], affoptionTag=self.all_affopt_tags[0])

    def test_routes_and_servers(self):
        '''
        All servers in spec should be reachable
        '''
        for host in self.servers:
            logger.info("Testing with host %s", host)
            for route in self.routes_with_args:
                try:
                    r = requests.get(host + route, headers=self.headers, timeout=self.timeout)
                    t = r.elapsed.total_seconds()
                    try:
                        self.assertEqual(r.status_code, 200)
                        logger.info("Server at " + host + route + " responded in " 
                                    + str(t) + " seconds, with a " + str(r.status_code) + " status code.")
                    except:
                        logger.error("Server at " + host + route + " responded in " 
                                    + str(t) + " seconds, with a " + str(r.status_code) + " status code.")
                except requests.exceptions.ReadTimeout:
                    logger.error("Server at " + host + route + " timed out after " 
                                + str(self.timeout) + " seconds.")
                except requests.exceptions.ConnectTimeout:
                    logger.error("Server at " + host + route + " could not connect and timed out after " 
                                + str(self.timeout) + " seconds.")