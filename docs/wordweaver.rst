.. wordweaver:

Word Weaver
==============

Build Tools
______________
These are tools that build and compile various files needed by WordWeaver.

The FileMaker class is used to create both docx and latex outputs of conjugations.

.. autoclass:: wordweaver.buildtools.file_maker.FileMaker

.. autoclass:: wordweaver.buildtools.file_maker.DocxMaker

.. autoclass:: wordweaver.buildtools.file_maker.LatexMaker


Configs
_______________

There are four configuration files (yaml) that inform WordWeaver. A "build" configuration file that informs the Build Tools described above,
an "environment" configuration file that specifies certain run-time variables and security policies, an "interface" configuration file that specifies the way that
WordWeaver interacts with the language model, and a "language" configuration file that specifies variables about the language. Check out the :ref:`guides` section to learn how to configure these files properly.


Data
_______________

Your Data folder contains static data for the WordWeaver API, including the fomabin of your language model, a swagger template and flat files (json) containing data about your language's pronouns, verbs and affixes. 


FST
_______________

This folder deals with interactions between the API and the fomabin language model.

Requests must be encoded into tags for the FST:

.. autoclass:: wordweaver.fst.encoder.FstEncoder

The output of the FST must be decoded into a response that the API returns:

.. autoclass:: wordweaver.fst.decoder.FstDecoder

Translations into English are done through the EnglishGenerator class:

.. autoclass:: wordweaver.fst.english_generator.EnglishGenerator


Resources
_______________

This folder contains all resources for the RESTful WordWeaver API.

