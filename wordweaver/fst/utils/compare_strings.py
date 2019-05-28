# -*- coding: utf-8 -*-

import re

class compare_strings:
    """
    A library of utility functions to help compare Kanyenkéha strings in a more flexible manner
    """

    def __init__(self):
        return

    def normalize_glottals(self, s):
        mappings = [["`", "'"],
                    ["’", "'"]]

        cand = s

        for cur_mapping in mappings:
            pat = cur_mapping[0]
            repl = cur_mapping[1]
            cand = re.sub(pat, repl, cand,  re.UNICODE)

        return cand

    def strict_compare(self, str1, str2):
        """
        Strictly compares two strings taking into account stress and glottals. Glottals are normalized before
        comparison.
        :param str1:
        :param str2:
        :return:
        """

        cand1 = self.normalize_glottals(str1)
        cand2 = self.normalize_glottals(str2)

        return (cand1 == cand2)

    def compare_ignore_stress(self, str1, str2):
        """
        Compares two strings ignoring case, stress accents ` ´ and also length of stress ':'
        :param str1: first string
        :param str2: second string
        :return:
        """



        cand1 = self.remove_long_stress(str1.lower())
        cand1 = self.normalize_glottals(cand1)
        cand1 = self.remove_stress(cand1)

        cand2 = self.remove_long_stress(str2.lower())
        cand2 = self.remove_stress(cand2)
        cand2 = self.normalize_glottals(cand2)

        return (cand1 == cand2)

    def compare_ignore_stress_and_glottals (self, str1, str2):
        """
        Compares two strings ignoring case, stress accents ` ´, length of stress ':' and glottal '
        :param str1: first string
        :param str2: second string
        :return:
        """
        cand1 = self.remove_long_stress(str1.lower())
        cand1 = self.normalize_glottals(cand1)
        cand1 = self.remove_glottals(cand1)
        cand1 = self.remove_stress(cand1)

        cand2 = self.remove_long_stress(str2.lower())
        cand2 = self.remove_stress(cand2)
        cand2 = self.normalize_glottals(cand2)
        cand2 = self.remove_glottals(cand2)

        return (cand1 == cand2)

    def remove_stress(self, str1):
        """removes stress marks ` and ´ from str1"""

        cur_str = str1

        mappings = [[r'á', 'a'],
                   [r'à', 'a'],
                   [r'é', 'e'],
                   [r'è', 'e'],
                   [r'í', 'i'],
                   [r'ì', 'i'],
                   [r'ó', 'o'],
                   [r'ò', 'o'] ]

        for cur_mapping in mappings:
            pat = cur_mapping[0]
            repl = cur_mapping[1]
            cur_str = re.sub(pat, repl, cur_str, re.IGNORECASE or re.UNICODE)
        return cur_str

    def remove_glottals(self, str1):
        cur_str = self.normalize_glottals(str1)
        cur_str = re.sub("'", "", cur_str)
        return cur_str


    def remove_long_stress(self, str1):
        """removes long stress character ':' from str1. Note, to remove accent marks use remove_stress """
        return re.sub(r':', '', str1, re.UNICODE)

    def compare_ignore_long_stress(self, str1, str2):
        """
        Compare 2 string ignoring case and long stress mark ':'. Accents are taken into account
        :param str1:
        :param str2:
        :return:
        """

        cand1 = self.remove_long_stress(str1.lower())
        cand2 = self.remove_long_stress(str2.lower())
        return (cand1 == cand2)