import os
from unittest import TestLoader, TextTestRunner, TestSuite
# Unit tests
## Resources
from .test_affix import AffixTest
from .test_pronoun import PronounTest
from .test_verb import VerbTest
## Spec
from .test_spec import SwaggerSpecTest
## Other
from .test_tag_maker import TagTest
from .test_english import EnglishTest

# Integration tests
from .integration.test_basic_errors import ResourceIntegrationBasicErrorTest
from .integration.test_resources import ResourceIntegrationTest
from .integration.test_swagger_integration import SwaggerSpecIntegrationTest
from .integration.test_specific_errors import ResourceIntegrationSpecificErrorTest

from . import log

loader = TestLoader()

prod_tests = [
        loader.loadTestsFromTestCase(test)
        for test in (AffixTest, EnglishTest, PronounTest, VerbTest, TagTest, 
                     SwaggerSpecTest, ResourceIntegrationBasicErrorTest,
                     ResourceIntegrationTest, SwaggerSpecIntegrationTest,
                     ResourceIntegrationSpecificErrorTest)
    ]

fst_dev_tests = []

dev_tests = [
        loader.loadTestsFromTestCase(test)
        for test in (AffixTest, EnglishTest, PronounTest, VerbTest, TagTest, 
                     SwaggerSpecTest)
    ]

def run_tests(suite):
    if suite == 'all':
        suite = loader.discover(os.path.dirname(log.__file__))
    elif suite == 'prod':
        suite = TestSuite(prod_tests)
    elif suite == 'dev':
        suite = TestSuite(dev_tests)

    runner = TextTestRunner(verbosity=3)
    runner.run(suite)

if __name__ == "__main__":
    run_tests('prod')