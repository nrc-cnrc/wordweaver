# -*- coding: utf-8 -*-

class FomaInputException(Exception):
    """
    Exceptions raised to capture mal-formed strings of tags for Foma FST

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error

    """

    def __init__(self, msg=""):
        # text = "Failed to form a valid Foma tag string: " + msg
        # super(FomaInputException, self).__init__(text)
        if msg is None:
            self.mesg = "Failed to initialize a Foma transducer"
        else:
            self.mesg = msg
        super(FomaInputException, self).__init__(self.mesg)


class IncorrectConjugationException(Exception):
    """
    Exceptions raised when an answer obtained from Foma differs from gold standard answer.
    """

    def __init__(self, tag_str='', expected_str='', actual_list=''):
        msg = "Answer obtain from Foma fails match gold standard: tag: {}, expected: {}, actual: {}".format(
            tag_str, expected_str, str(actual_list))
        super(IncorrectConjugationException, self).__init__(msg)


class InvalidLexVerbDefinitionException(Exception):
    """
    Exceptions raised when a Foma transducer has not been initialized successfully.
    """

    def __init__(self, msg = None, verb_dict = ''):
        if msg is None:
            msg = "Failed to generate a lexical item for verb using the CSV file. " + str(verb_dict)
        else:
            msg = "Error in Excel definition of a verb. " + msg + str(verb_dict)


        super(InvalidLexVerbDefinitionException, self).__init__(msg)

class NullFomaTransducerException(Exception):
    """
    Exceptions raised when a Foma transducer has not been initialized successfully.
    """

    def __init__(self, msg = None, path_to_fomabin = ''):
        if msg is None:
            msg = "Failed to initialize a Foma transducer from {}".format(path_to_fomabin)
        else:
            msg = msg + " Path: {}".format(path_to_fomabin)
        self.path = path_to_fomabin

        super(NullFomaTransducerException, self).__init__(msg)

class TestFileNotFoundException(Exception):
    """
    Exceptions test file with gold standard conjugations is not found.
    """

    def __init__(self, msg, path = ''):
        if msg is None:
            msg = "Failed to read test data from file {0}".format(path)
        else:
            msg = msg + " Path {0}".format(path)
        self.file_path = path

        super(TestFileNotFoundException, self).__init__(msg)

class MisconfiguredEnvironment(Exception):
    '''
    Exception rasied for missing ENV variables
    '''
    def __init__(self, msg):
        if msg is None:
            msg = "Environment variables are misconfigured. Please check the documentation"
        else:
            msg = msg

        super(MisconfiguredEnvironment, self).__init__(msg)
