# -*- coding: utf-8 -*-

""" Test Foma access
"""

import os

from wordweaver.fst.foma import FST
from wordweaver.exceptions import NullFomaTransducerException
from wordweaver.fst.utils.foma_access_python import foma_access_python
from wordweaver.fst.utils.foma_access import foma_access
from wordweaver.data import data_dir
from wordweaver.log import logger

from unittest import TestCase

class TestFomaBindings(TestCase):

    def setUp(self):
        self.path_to_model = os.path.join(data_dir, 'fomabins', 'toy-kawe-stressed-markup.fomabin')
        self.transducer = None
        self.testFile = os.path.join(os.path.dirname(__file__), 'test_data', 'test-foma-bindings.txt')

    def test_TransducerDirectly(self):

        try:
            self.transducer = FST.load(self.path_to_model)
        except Exception as e:
            logger.error("Could not initialize a Foma FST. path_to_model: {}".format(
                self.path_to_model) + e)
        fin = open(self.testFile, 'r')
        c = -1

        for line in fin:
            c = c + 1
            try:
                down_string = line.strip()
                logger.info("Direct: {0}: In: {1}".format(str(c), down_string))

                res = self.transducer.apply_down(down_string)
                for r in res:
                    logger.info(" out: {0}".format(r))
                logger.info("-")
            except Exception as e:
                logger.error("Error in TestBindingDirect: " + e)

        fin.close()

    def test_BindingsFomaAccessPython(self):
        self.foma_accessor = None
        try:
            foma_accessor = foma_access_python(self.path_to_model)
        except NullFomaTransducerException as e:
                logger.info("Failed to initialize FST", exc_info=True)

        fin = open(self.testFile, 'r')
        c = -1

        for line in fin:
            c = c + 1
            try:
                down_string = line.strip()
                logger.info("foma-access-python: {0}: In: {1}".format(str(c), down_string))

                res = foma_accessor.down(down_string)
                for r in res:
                    logger.info(" out: {0}".format(r))
                logger.info("-")
            except Exception as e:
                logger.error("Error in TestBindingsFomaAccessPython: " + e)

        fin.close()

    def test_foma_access_Shell(self):

        foma_shell = None

        try:
            foma_shell = foma_access(self.path_to_model)
        except NullFomaTransducerException as e:
            logger.info("Failed to initialize foma-access", exc_info=True)

        fin = open(self.testFile, 'r')
        c = -1

        for line in fin:
            c = c + 1
            try:
                down_string = line.strip()
                logger.info("foma-shell: {0}: In: {1}".format(str(c), down_string))

                res = foma_shell.down(down_string)
                for r in res:
                    logger.info(" out: {0}".format(r))
                logger.info("-")
            except Exception as e:
                logger.error("Error in TestBindingsFomaAccessPython: " + e)

        fin.close()




