from unittest import TestCase
import re
from wordweaver import app
from wordweaver.data.api_data.models import affix_data, pronoun_data, verb_data
from wordweaver.resources.affix import AFFIX_OPTIONS
import requests
import logging
from .. import logger

class ResourceIntegrationTest(TestCase):
    """
    This tests that the api returns 200s for all basic
    GET requests.    

    """
    def setUp(self):
        # host
        self.host = "http://localhost:5000"
        self.prefix = "/api/v1"
        # routes
        self.routes = [str(route) for route in app.url_map.iter_rules()]
        self.routes_no_fst_no_args = [route for route in self.routes if not "<" in route and not "conjugation" in route]
        self.routes_no_args = [route for route in self.routes if not "<" in route and route not in self.routes_no_fst_no_args]
        self.routes_only_args = [route for route in self.routes if "<" in route and route != "/static/<path:filename>"]
        # endpoints
        self.rules_by_endpoint = app.url_map._rules_by_endpoint
        self.endpoints = [rt for rt in self.rules_by_endpoint.keys()]
        # args
        self.arg_match = re.compile(r'\<[a-z:]+\>')
        self.all_pronoun_tags = [x['tag'] for x in pronoun_data]
        self.affix_options = AFFIX_OPTIONS['AFFIX_OPTIONS']
        self.all_affopt_tags = [x['tag'] for x in self.affix_options]
        self.all_verb_tags = [x['tag'] for x in verb_data]
        self.all_affix_tags = [x['tag'] for x in affix_data]
        self.args_to_check = ("affix", "aff-option", "pronoun", "verb")
    
    def return_endpoint_arg(self, ep):
        split = ep.split('.')
        split_length = len(split)
        return split[split_length-1]
    
    def return_route_from_endpoint(self, ep):
        return str(self.rules_by_endpoint[ep][0])

    def test_response_code(self):
        '''
        Ensure all routes return 200
        '''
        for rt in self.routes_no_fst_no_args:
            try:
                r = requests.get(self.host + rt)
                self.assertEqual(r.status_code, 200)
                logger.info("Route " + self.host + rt + " returned " + str(r.status_code))
            except:
                logger.error("Couldn't connect. Is flask running?")
            

        for rt in self.routes_no_args:
            try:
                r = requests.get(self.host + rt)
                self.assertEqual(r.status_code, 200)
                logger.info("Route " + self.host + rt + " returned " + str(r.status_code))
            except AssertionError:
                logger.error("Route " + self.host + rt + " returned " + str(r.status_code) + ". Is the FST running?")
            except:
                logger.error("Couldn't connect. Is flask running?")
        
    def test_response_code_with_args(self):
        '''
        Ensure all args return 200
        '''
        for ep in self.routes_only_args:
            if "/verb" in ep:
                for x in self.all_verb_tags:
                    rt = re.sub(self.arg_match, x, ep)
                    try:
                        r = requests.get(self.host + rt)
                        self.assertEqual(r.status_code, 200)
                    except AssertionError:
                        logger.error("Route " + self.host + rt + " returned " + str(r.status_code) + ". Is the FST running?")
                    except:
                        logger.error("Couldn't connect. Is flask running?")
                logger.info("Successfully tested " + str(len(self.all_verb_tags)) + " verb resources at route " + self.host + ep + " .")

            elif "/aff-option" in ep:
                for x in self.all_affopt_tags:
                    rt = re.sub(self.arg_match, x, ep)
                    try:
                        r = requests.get(self.host + rt)
                        self.assertEqual(r.status_code, 200)
                    except AssertionError:
                        logger.error("Route " + self.host + rt + " returned " + str(r.status_code) + ". Is the FST running?")
                    except:
                        logger.error("Couldn't connect. Is flask running?")
                
                logger.info("Successfully tested " + str(len(self.all_affopt_tags)) + " affix option resources at route " + self.host + ep + ".")

            elif "/affix" in ep:
                for x in self.all_affix_tags:
                    rt = re.sub(self.arg_match, x, ep)
                    try:
                        r = requests.get(self.host + rt)
                        self.assertEqual(r.status_code, 200)
                    except AssertionError:
                        logger.error("Route " + self.host + rt + " returned " + str(r.status_code) + ". Is the FST running?")
                    except:
                        logger.error("Couldn't connect. Is flask running?")
                logger.info("Successfully tested " + str(len(self.all_affix_tags)) + " affix resources at route " + self.host + ep + ".")

            elif "/pronoun" in ep:
                for x in self.all_pronoun_tags:
                    rt = re.sub(self.arg_match, x, ep)
                    try:
                        r = requests.get(self.host + rt)
                        self.assertEqual(r.status_code, 200)
                    except AssertionError:
                        logger.error("Route " + self.host + rt + " returned " + str(r.status_code) + ". Is the FST running?")
                    except:
                        logger.error("Couldn't connect. Is flask running?")
                logger.info("Successfully tested " + str(len(self.all_pronoun_tags)) + " pronoun resources at route " + self.host + ep + ".")
            elif "/conjugations":
                logger.debug("Passing conjugations args for other test")
                pass
            else:
                logger.warning("Route " + ep + " was registered, but not tested.")
