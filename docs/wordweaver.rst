.. wordweaver:

WordWeaver
==============

Build Tools
______________
These are tools that build and compile various files needed by WordWeaver.

The FileMaker class is used to create both docx and latex outputs of conjugations.

.. autoclass:: wordweaver.buildtools.file_maker.FileMaker

.. autoclass:: wordweaver.buildtools.file_maker.DocxMaker

.. autoclass:: wordweaver.buildtools.file_maker.LatexMaker

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

