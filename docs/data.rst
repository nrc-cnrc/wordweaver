.. _data:

Data
==============

You must provide some static data for WordWeaver 
including the `fomabin` of your language model, a swagger template and flat files (json) 
containing data about your language's pronouns, verbs and affixes. 

JSON data
-----------

Affixes
~~~~~~~~

Pronouns
~~~~~~~~~

Verbs
~~~~~~

Foma Binary
------------

You must have a valid `Foma <https://fomafst.github.io/morphtut.html>`_ binary.


Swagger
--------

WordWeaver uses Swagger to document its API. We recommend using the `default swagger spec <https://github.com/roedoejet/wordweaver/tree/master/wordweaver/sample/data/swagger/swagger-pre.json>`_
instead of writing your own. In order to update your swagger spec, run the following code:

.. code-block:: python

    gen = SwaggerSpecGenerator()
    gen.writeNewData()

We recommend integrating this into a CI/CD pipeline for your WordWeaver instance.

.. note::
    This will only edit your swagger spec at $WW_DATA_DIR/swagger/swagger-pre.json