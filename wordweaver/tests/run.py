# -*- coding: utf-8 -*-

""" Execution script for running tests
"""

from unittest import TestLoader, TextTestRunner, TestSuite
import sys
import os

# Unit tests
# Resources
from .test_affix import AffixTest
from .test_pronoun import PronounTest
from .test_verb import VerbTest
# Spec
from .test_spec import SwaggerSpecTest
# Other
from .test_tag_maker import TagTest
from .test_english import EnglishTest

# Integration tests
from .integration.test_basic_errors import ResourceIntegrationBasicErrorTest
from .integration.test_resources import ResourceIntegrationTest
from .integration.test_swagger_integration import SwaggerSpecIntegrationTest
from .integration.test_specific_errors import ResourceIntegrationSpecificErrorTest

LOADER = TestLoader()

PROD_TESTS = [
    LOADER.loadTestsFromTestCase(test)
    for test in (AffixTest, EnglishTest, PronounTest, VerbTest, TagTest,
                 SwaggerSpecTest, ResourceIntegrationBasicErrorTest,
                 ResourceIntegrationTest, SwaggerSpecIntegrationTest,
                 ResourceIntegrationSpecificErrorTest)
]

DEV_TESTS = [
    LOADER.loadTestsFromTestCase(test)
    for test in (AffixTest, EnglishTest, PronounTest, VerbTest, TagTest,
                 SwaggerSpecTest)
]

def run_tests(suite):
    '''Run tests'''
    if suite == 'all':
        suite = LOADER.discover(os.path.dirname(__file__))
    elif suite == 'prod':
        suite = TestSuite(PROD_TESTS)
    elif suite == 'dev':
        suite = TestSuite(DEV_TESTS)

    runner = TextTestRunner(verbosity=3)
    runner.run(suite)


if __name__ == "__main__":
    try:
        run_tests(sys.argv[1])
    except IndexError:
        print("Please specify a test suite to run: i.e. 'dev' or 'all'")
