# -*- coding: utf-8 -*-

""" Test Access to Fomabin
"""

from unittest import TestCase
import os

from wordweaver.data import data_dir
from wordweaver.fst.utils.foma_access import foma_access
from wordweaver.log import logger

class TestFoma_access_shell(TestCase):
    path_to_foma = None
    foma_shell = None
    fomabin_name = 'toy-kawe-stressed-markup.fomabin'

    def setUp(self):
        self.path_to_foma = os.path.join(data_dir, 'fomabins')
        self.foma_shell = foma_access(os.path.join(self.path_to_foma, self.fomabin_name))

    def test_up(self):
        verb = "^PP-^ke^R-^'níkhons^H^"
        res = self.foma_shell.up(verb)
        if len(res) != 1:
            self.fail("Expected one answer for '^PP-^ke^R-^'níkhons^H^'")
        else:
            for r in res:
                logger.debug(r)

    def test_down(self):
        tags = 'Verb+Active+AgentSg1+PatSg3Neuter+7nikhon-r+Habitual'
        res = self.foma_shell.down(tags)
        if len(res) != 1:
            self.fail("Excpected a single answer for Verb+Active+AgentSg1+PatSg3Neuter+7nikhon-r+Habitual")
        elif res[0] != "^PP-^ke^R-^'níkhons^H^":
            self.fail('Expected "^PP-^ke^R-^\'níkhons^H^", got ' + res[0])
        else:
            logger.debug(res[0])

    def test_execute_foma_command(self):
        res = self.foma_shell.execute_foma_command('random_upper')
        for r in res:
            logger.debug(r)
