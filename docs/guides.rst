.. _guides:

Guides
======

Here are some guides to help do some of the basic tasks required for creating a WordWeaver instance.

Running your instance
----------------------

    1. Make sure you have all the required data and configuration files described in :ref:`data` and :ref:`configuration`
    2. Copy the `sample directory <https://github.com/roedoejet/wordweaver/tree/master/wordweaver/sample>`_ and replace all of the data and configuration files with your own.
    3. Set the environment variable WW_CONFIG_DIR equal to the absolute path to the folder called :code:`configs` from step 2.
    4. Set the environment variable WW_DATA_DIR equal to the absolute path to the folder called :code:`data` from step 2.
    5. Run the following python code, either from the interpreter or in a script:

    .. code-block:: python

        from wordweaver.app import app
        app.run()

    If you have gunicorn installed on your machine, you can also run it from the command line:

    .. code-block::
    
        gunicorn wordweaver.app:app --bind 0.0.0.0:$PORT

Adding/editing a verb
----------------------

    1. Add/edit the verb in your :code:`verbs.json` file. (see :ref:`data`)

    .. code-block:: json

        {
        "display": "wake'nahsan\u00e9n:taks",
        "eng-3": "is tongue tied; gets tongue tied",
        "eng-inf": "be tongue tied; get tongue tied",
        "eng-past": "was tongue tied; got tongue tied",
        "eng-perf": "been tongue tied; gotten tongue tied",
        "eng-prog": "being tongue tied; getting tongue tied",
        "gloss": "be tongue tied; get tongue tied",
        "root": "'nahsanentak",
        "state_type": "hab",
        "stative-perf-trans": "",
        "stative-pres-trans": "",
        "tag": "7nahsanentak-b",
        "thematic_relation": "blue"
        }

    2. Update your Swagger Spec (see :ref:`data`)

That's it! Next time you run your WordWeaver instance, the verb will be there.

Adding/editing a pronoun
-------------------------

    1. Add/edit the pronoun in your :code:`pronouns.json` file. (see :ref:`data`)

    .. code-block:: json

        {
        "person": "1",
        "number": "SG",
        "gender": "",
        "inclusivity": "",
        "role": "",
        "value": "ke",
        "gloss": "I",
        "obj_gloss": "Me",
        "tag": "1-sg"
        }

    2. Update your Swagger Spec (see :ref:`data`)
    3. Update the :code:`pronoun` key in your interface configuration file. (see :ref:`configuration`)

That's it! Next time you run your WordWeaver instance, the pronoun will be there.

Adding/editing an new temporal option
--------------------------------------

This step is for adding/editing a new aspect (or tense) to your model.

    1. Ensure that you have added the affixes needed by your new aspect.

    2. Add/edit your aspect/tense to :code:`affix_options` in your language configuration file. (see :ref:`configuration`)

    .. code-block:: yaml

        affix_options:
          - tag: habpres
            gloss: Habitual (present)
            affixes:
              - habitual
              - pres
            public: true

    3. Update your Swagger Spec (see :ref:`data`)

That's it! Next time you run your WordWeaver instance, the tense/aspect will be there.

Adding an affix
----------------

Adding/editing an optional affix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This step is for adding/editing affixes that must be selected through 'affix options'.

1. Add/edit the affix to :code:`affixes.json`. (see :ref:`data`)

    .. code-block:: json

        {
        "gloss": "perfective",
        "type": "aspect",
        "morphemes": [],
        "tag": "perf"
        }

2. Add/edit the affix to under the proper type beneath the :code:`affixes` key in your language configuration file. (see :ref:`configuration`)

    .. code-block:: yaml

        affixes:
          aspect:
            perf:
               tag: "+Perf"
               marker: "R"

3. Add/edit it for any tense/aspect affix options that require it.

4. Update your Swagger Spec (see :ref:`data`) 

That's it! Next time you run your WordWeaver instance, the affix will be there.

Adding an affix required by certain verbs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This step is for adding affixes that are required by verbs but cannot be optionally added through affix options.

1. Add/edit the affix to :code:`affixes.json`. (see :ref:`data`)

    .. code-block:: json

        {
        "gloss": "duplicative",
        "type": "prepronominal_prefix",
        "morphemes": [],
        "tag": "dup"
        }

2. Add/edit the affix to under the proper type beneath the :code:`decoding` and :code:`bundled_affixes` keys in your interface configuration file. (see :ref:`configuration`)

    .. code-block:: yaml

        decoding:
          bundled_affixes:
            dup: TE

3. Add/edit it for any verbs that require it.

    .. code-block:: json

        {
            "display": "tekonia'ni\u00e1nawenks",
            "eng-3": "puts gloves on someone",
            "eng-inf": "put gloves on someone",
            "eng-past": "put gloves on someone",
            "eng-perf": "put gloves on someone",
            "eng-prog": "putting gloves on someone",
            "gloss": "put gloves on someone",
            "required_affixes": [
                "dup"
            ],
            "root": "a'nyanawenk",
            "state_type": "hab",
            "stative-perf-trans": "",
            "stative-pres-trans": "",
            "tag": "a7nyanawenk-p",
            "thematic_relation": "purple"
        }

4. Update your Swagger Spec (see :ref:`data`) 

That's it! Next time you run your WordWeaver instance, the affix will be there.
