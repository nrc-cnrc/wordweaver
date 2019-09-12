# -*- coding: utf-8 -*-

""" Test Access to Fomabin
"""

import os

from wordweaver.log import logger

from wordweaver.data import data_dir
from wordweaver.fst.utils.foma_access_python import foma_access_python

from unittest import TestCase
from wordweaver.exceptions import NullFomaTransducerException


class TestFoma_access_python(TestCase):

    foma_accessor = None
    fomabin_name = 'toy-kawe-stressed-markup.fomabin'
    path_to_fomabin = None

    def setUp(self):
        self.path_to_fomabin = os.path.join(
            data_dir, 'fomabins', self.fomabin_name)

        self.foma_accessor = foma_access_python(self.path_to_fomabin)
        return

    def test_reload_FST(self):
        self.foma_accessor.reload_FST()

        # test loading an incorrect path
        bad_foma = foma_access_python(path_to_fst='ankhjhgj')

        try:
            bad_foma.reload_FST()
        except NullFomaTransducerException as e:
            logger.info("Correctly handled wrong path to FST", exc_info=True)

    def test_run_up(self):
        up_tags = "^PP-^ke^R-^'níkhons^H^"
        res = self.foma_accessor.up(up_tags)
        expected = 1
        actual = 0
        for r in res:
            logger.info(r)
            actual = actual + 1
        if expected != actual:
            logger.error("test_run_up: Incorrect number of answers for test_run_up ({}). Expected: {}, "
                         "actual {}.".format(up_tags, expected, actual))
            self.fail()

    def test_run_down(self):
        down_tags = 'Verb+Active+AgentSg1+PatSg3Neuter+7nikhon-r+Habitual'
        res = self.foma_accessor.down(down_tags)
        num_answers = 1
        actual = 0
        for r in res:
            logger.info(r)
            actual = actual + 1
        if actual != num_answers:
            logger.error("test_run_down: Incorrect number of answers for test_run_down ({}). Expected {}, "
                         "actual {}.".format(down_tags, num_answers, actual))
            self.fail()

    def test_get_FST(self):
        self.foma_accessor.get_FST()
        if self.foma_accessor is None:
            logger.error("Error in test_get_FST")
