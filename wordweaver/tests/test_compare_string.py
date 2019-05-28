#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from unittest import TestCase
import sys, os.path
import logging

parentdir  = os.path.abspath(__file__ + "/../../")
sys.path.insert(0, parentdir)
from wordweaver.fst.utils.compare_strings import compare_strings

class TestCompare_string(TestCase):
    def setUp(self):

        self.logger = logging.getLogger('root')
        self.logger.setLevel(logging.DEBUG)

        self.utilCmp = compare_strings()

        self.longstress = [['kawennó:nis', 'kawennónis'],
                           ['kawennónis', 'kawennónis'],
                           ['kawennón:nis', 'kawennónnis']]

        self.allstress = [['kawennó:nis', 'kawennonis'],
                           ['kawennónis', 'kawennonis'],
                           ['kawennón:nis', 'kawennonnis'],
                          ['kawennonnis', 'kawennonnis']]


        self.compare_longstress = [['kawennó:nis', 'kawennónis', True],
                                   ['kawennónis', 'kawennó:nis', True],
                                  ['kawennó:nis', 'kawennónnis', False],
                                  ['kawennónnis', 'kawennó:nis', False] ]

        self.compare_allstress = [['kawennó:nis', 'kawennonis', True],
                                   ['kawennó:nis', 'kawennonnis', False],
                                   ['kawenn:nis', 'kawennonis', False],
                                   ['kawenna:nnis', 'kawennonnis', False],
                                   ['kawennòn:nis', 'kawennonnis', True]
                                     ]

        self.compare_allstress_glottals = [['kawennó:nis\'', 'kawennonis', True],
                                  ['kawennó:nis', 'kawennonnis\'', False],
                                  ['kawenn:nis`', 'kawennonis', False],
                                  ['kawenna:nnis', 'kawennonnis`', False],
                                  ['kawennòn:nis`', 'kawennonnis\'', True],
                                  ['ki\'tenhnyothahkwe', 'ki’tenhnyothahkwe', True],
                                  ["ki'tenhnyothahkwe", "ki’tenhnyóthahkwe", True]

                                  ]


        return 0



    def test_remove_stress(self):
        for pair in self.allstress:
            old = pair[0]
            expected = pair[1]
            new = self.utilCmp.remove_stress(pair[1])
            msg = "old: " + old + " new: " + new + " (expected: " + expected + ")"
            self.logger.info(msg)
            if (new != expected):
                self.logger.error(msg)
                self.fail(msg)


    def test_remove_long_stress(self):
        for pair in self.longstress:
            old = pair[0]
            expected = pair[1]
            new = self.utilCmp.remove_long_stress(pair[1])
            msg = "test_remove_long_stress: old: " + old + " new: " + new + " (expected: " + expected + ")"
            self.logger.info(msg)
            if (new != expected):
                self.logger.error(msg)
                self.fail(msg)


    def test_compare_ignore_long_stress(self):
        for triple in self.compare_longstress:
            s1 = triple[0]
            s2 = triple[1]
            ifSameExp = triple[2]
            ifSame = self.utilCmp.compare_ignore_long_stress(s1, s2)

            msg = "test_compare_ignore_long_stress: s1: " + s1 + ", s2: " + s2 + ", ifSameExp: " + str(ifSameExp) + \
                  ", ifSame: " + str(ifSame)
            if ifSame is ifSameExp:
                self.logger.info(msg)
            else:
                self.logger.error(msg)
                self.fail(msg)

    def test_compare_ignore_stress(self):
        for triple in self.compare_allstress:
            s1 = triple[0]
            s2 = triple[1]
            ifSameExp = triple[2]
            ifSame = self.utilCmp.compare_ignore_stress(s1, s2)

            msg = "test_compare_ignore_stress: s1: " + s1 + ", s2: " + s2 + ", ifSameExp: " + str(ifSameExp) + ", " \
                                                                                                              "ifSame: " + str(ifSame)
            if ifSame is ifSameExp:
                self.logger.info(msg)
            else:
                self.logger.error(msg)
                self.fail(msg)

    def test_compare_ignore_stress_and_glottals(self):
        for triple in self.compare_allstress_glottals:
            s1 = triple[0]
            s2 = triple[1]
            ifSameExp = triple[2]
            ifSame = self.utilCmp.compare_ignore_stress_and_glottals(s1, s2)

            msg = "test_compare_ignore_stress_and_glottals: s1: " + s1 + ", s2: " + s2 + ", ifSameExp: " + str(ifSameExp) + ", " \
                                                                                                               "ifSame: " + str(
                ifSame)
            if ifSame is ifSameExp:
                self.logger.info(msg)
            else:
                self.logger.error(msg)
                self.fail(msg)