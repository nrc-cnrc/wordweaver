# -*- coding: utf-8 -*-

from wordweaver.fst.foma import *
from wordweaver.exceptions import NullFomaTransducerException
from wordweaver.fst.utils.foma_access_python import foma_access_python
from wordweaver.fst.utils.foma_access import foma_access

import wordweaver.tests as testdata_dir
import wordweaver.data.fomabins as fst_dir

import os.path
import logging
from unittest import TestCase

class TestFoma_bindings(TestCase):

    def setUp(self):
        logging.basicConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.WARN)

        self.path_to_model = os.path.join(os.path.dirname(fst_dir.__file__), 'kawe-stressed-nomarkup.fomabin')
        self.transducer = None

        self.testFile = os.path.join(os.path.dirname(testdata_dir.__file__), 'test-foma-bindings.txt')

        return

    def test_TransducerDirectly(self):

        try:
            self.transducer = FST.load(self.path_to_model)
        except Exception as e:
            self.logger.error("Could not initialize a Foma FST. path_to_model: {}".format(
                self.path_to_model) + e.message)


        fin = open(self.testFile, 'r')
        c = -1

        for line in fin:
            c = c + 1
            try:
                down_string = line.strip()
                self.logger.info("Direct: {0}: In: {1}".format(str(c), down_string))

                res = self.transducer.apply_down(down_string)
                for r in res:
                    self.logger.info(" out: {0}".format(r))
                self.logger.info("-")
            except Exception as e:
                self.logger.error("Error in TestBindingDirect: " + e.message)

        fin.close()

    def test_BindingsFomaAccessPython(self):
        self.foma_accessor = None

        try:
            foma_accessor = foma_access_python(self.path_to_model)
        except NullFomaTransducerException as e:
                self.logger.info("Failed to initialize FST", exc_info=True)

        fin = open(self.testFile, 'r')
        c = -1

        for line in fin:
            c = c + 1
            try:
                down_string = line.strip()
                self.logger.info("foma-access-python: {0}: In: {1}".format(str(c), down_string))

                res = foma_accessor.down(down_string)
                for r in res:
                    self.logger.info(" out: {0}".format(r))
                self.logger.info("-")
            except Exception as e:
                self.logger.error("Error in TestBindingsFomaAccessPython: " + e.message)

        fin.close()

    def test_foma_access_Shell(self):

        foma_shell = None

        try:
            foma_shell = foma_access(self.path_to_model)
        except NullFomaTransducerException as e:
            self.logger.info("Failed to initialize foma-access", exc_info=True)

        fin = open(self.testFile, 'r')
        c = -1

        for line in fin:
            c = c + 1
            try:
                down_string = line.strip()
                self.logger.info("foma-shell: {0}: In: {1}".format(str(c), down_string))

                res = foma_shell.down(down_string)
                for r in res:
                    self.logger.info(" out: {0}".format(r))
                self.logger.info("-")
            except Exception as e:
                self.logger.error("Error in TestBindingsFomaAccessPython: " + e.message)

        fin.close()




