# -*- coding: utf-8 -*-

import logging
from subprocess import Popen, PIPE
from wordweaver.fst.utils.abstract_fst_access import abstract_fst_access


class foma_access (abstract_fst_access):
    """A utility class to allow access to a Foma FST by piping command line output into Python.
    This is a workaround for situations where Python bindings are not available.
    Implements abstract_fst_access.
    """

    path_to_model = None

    def __init__(self, path_to_fst):
        """
        :param path_to_fst: path where .fomabin file should be loaded from
        """
        self.logger = logging.getLogger('root')
        self.logger.setLevel(logging.DEBUG)
        self.path_to_model = path_to_fst
        return

    def up(self, text):
        """
        :param text: a Mohawk verb to be analysed
        :return:
        """
        return (self.execute_foma_command('up ' + text))




    def down (self, tags):
        """
        :param tags: a string of morphological tags to input into FST
        :return:
        """
        return ( self.execute_foma_command('down ' + tags))



    def execute_foma_command(self, foma_command):
        """
        :param foma_command:
        :return:
        """

        command = 'foma\n' + 'load ' + self.path_to_model + '\n' + foma_command + '\n'
        command = str(command)

        foma_process = Popen('/bin/bash', shell=False, universal_newlines=True,
                             stdin=PIPE, stdout=PIPE, stderr=PIPE)
        self.logger.info('command is ' + command)

        out, err = foma_process.communicate(command)

        self.logger.info('out is:'  + out)

        if (err.strip() != ''):
            self.logger.error(err)
            return None

        #get output of Foma after
        tmp = out.split('paths.')

        for t in tmp:
            self.logger.info('\ttmp: ' + t)

        lines = tmp[1].split('\n')
        answers = []
        line_no = 0
        for l in lines:
            if (l.strip() == ''):
                continue
            elif (l.startswith('foma')):
                continue
            else:
                answers.append(l.strip())
            line_no = line_no + 1

        return answers

