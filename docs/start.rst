.. start:

Getting Started
================

Overview
########

What is WordWeaver?
************************************

WordWeaver is a Python library for turning an FST made with `Foma <https://fomafst.github.io/>`_ into a RESTful API. It combines with the WordWeaver GUI to create an interactive web application for the data as well.
WordWeaver was initially built for `Kanyen'kéha <https://www.aclweb.org/anthology/W18-4806>`_ but with all Iroquoian languages in mind. It will likely work for similar polysynthetic languages and Foma FSTs that model inflectional verbal morphology, but
non-Iroquoian languages will likely have to modify the source in order to work.

Who made this?
************************************

WordWeaver is the outcome of collaborative research between the `Onkwawenna Kenyohkwa Mohawk Immersion school <https://onkwawenna.info/>`_ and the `Indigenous Language Technology research group <https://nrc.canada.ca/en/node/1378>`_ at the National Research Council of Canada.

How do I make this for another language?
*****************************************

While we have made deliberate efforts to make WordWeaver simple to use, it will likely still require somebody with some experience with Natural Language Processing (`NLP <https://en.wikipedia.org/wiki/Natural_language_processing>`_) in order to implement.
The basic gist of it is that you will need to create or have the following:

1. An `FST <https://en.wikipedia.org/wiki/Finite-state_transducer>`_-based model of your language's inflectional verbal morphology (i.e. a model of how to make "conjugations"). Currently this must be a `.fomabin` file. Please contact us if you need other formats supported. (see :ref:`data`)
2. Four configuration files for setting up your WordWeaver instance (see :ref:`configuration`.)
3. JSON files containing all the verbs, pronouns and other affixes in your model (see :ref:`data`.)
4. A Swagger Specification for your API (see :ref:`data`)

For steps on what to do next, please visit the :ref:`guides`.





