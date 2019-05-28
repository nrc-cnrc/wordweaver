# -*- coding: utf-8 -*-

"""
This is an abstract base class that needs to be implemented to access an arbitrary FST.
"""

import abc

class abstract_fst_access(abc.ABC):

    @abc.abstractmethod
    def __init__(self, path_to_compiled_fst):
        pass

    @abc.abstractmethod
    def down(self, generate_command):
        """
        :param generate_command: a string of markers to pass to the FST with up, e.g. '+Noun+Pl+book'
        :return:
        """
        pass

    @abc.abstractmethod
    def up(self, analyze_command):
        """
        :param analyze_command: a string of text to pass to FST for analysis, e.g. 'books'
        :return:
        """
        pass