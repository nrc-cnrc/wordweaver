import sys, os.path
import wordweaver.data.fomabins as fomabin_dir

from wordweaver.fst.utils.foma_access import foma_access

import logging

from unittest import TestCase
from . import log



class TestFoma_access_shell(TestCase):

    path_to_foma = None
    foma_shell = None
    fomabin_name = 'kawe-stressed-nomarkup.fomabin'

    def setUp(self):
        logging.basicConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.path_to_foma = os.path.dirname(fomabin_dir.__file__)
        self.foma_shell = foma_access(os.path.join (self.path_to_foma, self.fomabin_name))

        return


    def test_up(self):
        verb = 'sekhón:nis'
        res = self.foma_shell.up(verb)
        if (len(res) != 1):
            self.fail("Expected one answer for 'sekhón:nis'")
        else:
            for r in res:
                self.logger.debug(r)

    def test_down(self):
        tags = 'Verb+Active+AgentSg2+PatSg3Neuter+khonni-perf-r+Habitual'
        res = self.foma_shell.down(tags)
        if (len(res) != 1):
            self.fail("Excpected a single answer for Verb+Active+AgentSg2+PatSg3Neuter+khonni-perf-r+Habitual")
        elif (res[0] != 'sekhón:nis'):
            self.fail('Expected "sekhón:nis", got ' + res[0])
        else:
            self.logger.debug(res[0])

    def test_execute_foma_command(self):
        return
        res = self.foma_shell.execute_foma_command('random_upper')
        for r in res:
            self.logger.debug(r)
