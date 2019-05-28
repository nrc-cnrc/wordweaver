# -*- coding: utf-8 -*-

import logging
import os.path

from wordweaver.exceptions import NullFomaTransducerException
from wordweaver.exceptions import FomaInputException
from wordweaver.fst.utils.abstract_fst_access import abstract_fst_access

try:
    from wordweaver.fst.foma import FST
except:
    FST = False

class foma_access_python (abstract_fst_access):
    """A utility class to use Python bindings to access a Foma FST.
     Implements abstract_fst_access"""

    path_to_model = None
    transducer = None

    def __init__(self, path_to_fst):
        """
        :param path_to_fst: path where .fomabin file should be loaded from
        """
        self.logger = logging.getLogger('root')
        self.logger.setLevel(logging.DEBUG)
        if not FST:
            self.logger.warning(msg="This platform does not have Foma")
        self.path_to_model = path_to_fst

        return

    def reload_FST(self):

        if os.path.isfile(self.path_to_model):
            try:
                self.transducer = FST.load(self.path_to_model)
            except:
                self.logger.error("Could not initialize a Foma FST. path_to_model: {}".format(
                    self.path_to_model))
                raise NullFomaTransducerException(msg="Could not load a Foma FST from .fomabin. ", path_to_fomabin=self.path_to_model)
        else:
            raise NullFomaTransducerException(msg="Invalid path to fomabin. ", path_to_fomabin=self.path_to_model)



    def up(self, up_string):
        """

        :param up_string: a string to apply with "up"
        :return:
        """
        fst = self.get_FST()
        res = fst.apply_up(up_string)
        return res


    def down(self, down_string):
        """

        :param down_string: a string to apply with "down"
        :return:
        """
        fst = self.get_FST()
        res = fst.apply_down(down_string)
        return res

    def execute_foma_command(self, foma_command):
        """
        Uninmplemented method for compatibility with foma_access
        :param foma_command:
        :return:
        """
        e = FomaInputException("Cannot execute arbitrary foma commands: " + foma_command)
        raise e



    def get_FST(self):
        """

        :return: returns a foma.FST object
        """
        if self.transducer is None:
            self.reload_FST()
        return self.transducer