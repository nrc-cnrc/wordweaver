import logging
import os,sys
import log

from wordweaver.tests import log

import wordweaver.data.fomabins as fomabin_dir
from wordweaver.fst.utils.foma_access_python import foma_access_python

from unittest import TestCase
from wordweaver.exceptions import NullFomaTransducerException



class TestFoma_access_python(TestCase):

    foma_accessor = None
    fomabin_name = 'kawe-stressed-nomarkup.fomabin'
    path_to_fomabin = None

    def setUp(self):
        logging.basicConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

        self.path_to_fomabin = os.path.join(os.path.dirname(fomabin_dir.__file__), self.fomabin_name)

        self.foma_accessor = foma_access_python(self.path_to_fomabin)
        return



    def test_reload_FST(self):
        self.foma_accessor.reload_FST()

        #test loading an incorrect path
        bad_foma = foma_access_python(path_to_fst='ankhjhgj')

        try:
            bad_fst = bad_foma.reload_FST()
        except NullFomaTransducerException as e:
            self.logger.info("Correctly handled wrong path to FST", exc_info=True)


    def test_run_up(self):
        up_tags = 'kekhón:nis'
        res = self.foma_accessor.up(up_tags)
        expected = 1
        actual = 0
        for r in res:
            self.logger.info(r)
            actual = actual + 1
        if expected != actual:
            self.logger.error("test_run_up: Incorrect number of answers for test_run_up ({}). Expected: {}, "
                              "actual {}.".format(up_tags,
                                                                                                       expected,
                                                                                                       actual))
            self.fail()


    def test_run_down(self):
        down_tags = 'Verb+Active+AgentSg1+PatSg3Neuter+khonni-perf-r+Habitual'
        res = self.foma_accessor.down(down_tags)

        num_answers = 1
        actual = 0
        for r in res:
            self.logger.info(r)
            actual = actual + 1

        if actual != num_answers:
            self.logger.error("test_run_down: Incorrect number of answers for test_run_down ({}). Expected {}, "
                              "actual {}.".format(down_tags,
                                                                                                           num_answers,
                                                                                                           actual))
            self.fail()

    def test_get_FST(self):
        self.foma_accessor.get_FST()
        if self.foma_accessor is None:
            self.logger.error("Error in test_get_FST")


