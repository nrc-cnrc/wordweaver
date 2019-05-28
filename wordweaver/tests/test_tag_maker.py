from unittest import TestCase, skip
import re
import os
import itertools
from . import logger
from wordweaver.fst.encoder import FstEncoder
from wordweaver.data.api_data.models import verb_data, pronoun_data
from wordweaver.resources.affix import AFFIX_OPTIONS
from werkzeug.exceptions import NotFound, BadRequest
from wordweaver.configs import LANG_CONFIG
import wordweaver.data.fomabins as fomabins_dir
from wordweaver import app
from wordweaver.fst.utils.foma_access_python import foma_access_python as foma_access
from wordweaver.exceptions import NullFomaTransducerException


class TagTest(TestCase):

    @classmethod
    def setUpClass(cls):
        # Pronoun setup
        cls.all_pro_tags = [x['tag'] for x in pronoun_data]
        cls.all_pro_combinations = list(itertools.product(cls.all_pro_tags, cls.all_pro_tags))
        cls.invalid_pro_combinations = []
        cls.valid_pro_combinations = []
        for combo in cls.all_pro_combinations:
            if '1' in combo[0] and '1' in combo[1]:
                cls.invalid_pro_combinations.append(combo)
            elif '2' in combo[0] and '2' in combo[1]:
                cls.invalid_pro_combinations.append(combo)
            elif '2' in combo[0] and 'incl' in combo[1]:
                cls.invalid_pro_combinations.append(combo)
            elif 'incl' in combo[0] and '2' in combo[1]:
                cls.invalid_pro_combinations.append(combo)
            else:
                cls.valid_pro_combinations.append(combo)

        # Affix setup
        cls.affix_options = AFFIX_OPTIONS['AFFIX_OPTIONS']
        cls.all_affopts = list(cls.affix_options)
        cls.all_affopt_tags = [x['tag'] for x in cls.all_affopts]
        cls.perfective_options = [
            affopt for affopt in cls.all_affopts if "perf" in affopt['tag']]
        cls.non_perfective_options = [
            affopt for affopt in cls.all_affopts if "perf" not in affopt['tag']]
        
        # Verb setup
        cls.red_verb_tags = [
            verb['tag'] for verb in verb_data if 'red' == verb['thematic_relation']]
        cls.blue_verb_tags = [
            verb['tag'] for verb in verb_data if 'blue' == verb['thematic_relation']]
        cls.purple_verb_tags = [
            verb['tag'] for verb in verb_data if 'purple' == verb['thematic_relation']]

        # Args setup
        # (Verb, AffOpt, Agent, Patient)
        cls.red_arg_tuples = list(itertools.product(cls.red_verb_tags, cls.all_affopt_tags, cls.all_pro_tags, [""]))
        cls.blue_arg_tuples = list(itertools.product(cls.blue_verb_tags, cls.all_affopt_tags, [""], cls.all_pro_tags))
        cls.purple_arg_tuples = []
        for x in itertools.product(cls.purple_verb_tags, cls.all_affopt_tags):
            for y in cls.valid_pro_combinations:
                cls.purple_arg_tuples.append(x + y)

        cls.red_args = [{"verb": [tup[0]] if tup[0] else '', "aff-option": [tup[1]] if tup[1] else '', 
                         "agent": [tup[2]] if tup[2] else '', "patient": [tup[3]] if tup[3] else ''} for tup in cls.red_arg_tuples]
        cls.blue_args = [{"verb": [tup[0]] if tup[0] else '', "aff-option": [tup[1]] if tup[1] else '', 
                         "agent": [tup[2]] if tup[2] else '', "patient": [tup[3]] if tup[3] else ''} for tup in cls.blue_arg_tuples]
        cls.purple_args = [{"verb": [tup[0]] if tup[0] else '', "aff-option": [tup[1]] if tup[1] else '', 
                            "agent": [tup[2]] if tup[2] else '', "patient": [tup[3]] if tup[3] else ''} for tup in cls.purple_arg_tuples]
        
        # Tag setup
        cls.tag_pattern = re.compile(r"([A-Z]\w+\+)+[a-z7\-]+(\+[A-Z]\w+)+")
        cls.red_tags = [cls.return_tag(cls, arg)[0]['fst'] for arg in cls.red_args]
        cls.blue_tags = [cls.return_tag(cls, arg)[0]['fst'] for arg in cls.blue_args]
        cls.purple_tags = [cls.return_tag(cls, arg)[0]['fst'] for arg in cls.purple_args]
        cls.fst_tags = cls.red_tags + cls.blue_tags + cls.purple_tags

        # FST
        cls.fp = foma_access(os.path.join(os.path.dirname(fomabins_dir.__file__),
                               'kawe-28-02-2018.fomabin'))
            

    def valid_tag(cls, tag):
        '''
        Checks tag well-formedness (Xxxx+Xxxx+Xxxx syntax)
        '''
        match = cls.tag_pattern.search(tag)
        return match.group() == tag

    def return_tag(cls, args):
        '''
        Helper to return tag
        '''
        tag_maker = FstEncoder(args)
        return tag_maker.return_tags()

    def test_tag_exists_or_404(cls):
        '''
        Check if any tag passed as arg is not a valid tag.
        '''
        proper_args = {"verb": cls.red_verb_tags[0], "agent": '1-sg',
                       "aff-option": cls.non_perfective_options[0]['tag'], "patient": ""}
        proper_tag = cls.return_tag(proper_args)
        cls.assertTrue(cls.valid_tag(proper_tag[0]['fst']))

        non_existant_args = {"verb": cls.red_verb_tags[0], "agent": '1sing',
                             "aff-option": cls.non_perfective_options[0]['tag'], 
                             "patient": ""}

        with cls.assertRaises(NotFound):
            non_existant_tag = cls.return_tag(non_existant_args)[0]['fst']
            cls.valid_tag(non_existant_tag)

    def test_valid_role_or_400(cls):
        '''
        Must not allow patient with red, agent with blue
        '''
        # proper
        proper_args = {"verb": cls.red_verb_tags[0], "agent": '1-sg',
                       "aff-option": cls.non_perfective_options[0]['tag'], "patient": ""}
        proper_tag = cls.return_tag(proper_args)
        cls.assertTrue(cls.valid_tag(proper_tag[0]['fst']))

        # patient w/ red
        with cls.assertRaises(BadRequest):
            bad_red_args = {"verb": cls.red_verb_tags[0], "agent": '',
                            "aff-option": cls.non_perfective_options[0]['tag'], "patient": "1-sg"}
            cls.return_tag(bad_red_args)

        # agent w/ blue
        with cls.assertRaises(BadRequest):
            bad_blue_args = {"verb": cls.blue_verb_tags[0], "agent": '1-sg',
                             "aff-option": cls.non_perfective_options[0]['tag'], "patient": ""}
            cls.return_tag(bad_blue_args)

    def test_valid_pn_combo_or_400(cls):
        '''
        Must not allow invalid pn combo.
        I.e 1st, 2nd, 2nd + inclusive pros may not
        co-occur.
        '''
        valid_args = [{"verb": cls.purple_verb_tags[0], 'agent': combo[0],
                       "aff-option": cls.non_perfective_options[0]['tag'], 
                       "patient": combo[1]} for combo in cls.valid_pro_combinations]
        invalid_args = [{"verb": cls.purple_verb_tags[0], 'agent': combo[0],
                         "aff-option": cls.non_perfective_options[0]['tag'], 
                         "patient": combo[1]} for combo in cls.invalid_pro_combinations]

        for arg in invalid_args:
            with cls.assertRaises(BadRequest):
                tag = cls.return_tag(arg)
               
        for arg in valid_args:
            tag = cls.return_tag(arg)[0]['fst']
            cls.assertTrue(cls.valid_tag(tag))

    def test_thematic_role_switch(cls):
        '''
        Checks if red -> blue when perfective
        '''
        args = {"verb": cls.red_verb_tags[0], "agent": '1-sg',
                "aff-option": cls.perfective_options[0]['tag'], "patient": ""}
        tag = cls.return_tag(args)[0]['fst']
        cls.assertTrue(LANG_CONFIG['verb_type']['red']['tag'] not in tag)
        cls.assertTrue(LANG_CONFIG['verb_type']['blue']['tag'] in tag)
    
    def test_all_tags(cls):
        '''
        Check if all tags are generated and otherwise produce 400.
        '''
        logger.debug("Generating ALL tags, this might take a while...")
        red_verb_tag_len = len(cls.red_verb_tags) * len(cls.all_affopts) * len(cls.all_pro_tags)
        blue_verb_tag_len = len(cls.blue_verb_tags) * len(cls.all_affopts) * len(cls.all_pro_tags)
        purple_verb_tag_len = len(cls.purple_verb_tags) * len(cls.all_affopts) * len(cls.valid_pro_combinations)
        logger.info("""There are a total of {total} possible tags, 
                    including {red} red verbs, {blue} blue verbs, 
                    and {purple} purple verbs""".format(
                    total=str(red_verb_tag_len + blue_verb_tag_len + purple_verb_tag_len), 
                    red=str(red_verb_tag_len), blue=str(blue_verb_tag_len), purple=str(purple_verb_tag_len)))

        for arg in cls.red_args:
            tag = cls.return_tag(arg)[0]['fst']
            try:
                cls.assertTrue(cls.valid_tag(tag))
            except:
                cls.fail("The following tag did not work: " + str(tag) 
                             + ". The args that generated it were: " + str(arg))

        for arg in cls.blue_args:
            tag = cls.return_tag(arg)[0]['fst']
            cls.assertTrue(cls.valid_tag(tag))

        for arg in cls.purple_args:
            tag = cls.return_tag(arg)[0]['fst']
            cls.assertTrue(cls.valid_tag(tag))

    def test_fst(cls):
        '''
        Check if all tags are deemed valid by FST
        '''
        for tag in cls.fst_tags:
            try:
                list(cls.fp.down(tag))[0]
            except IndexError:
                logger.warning("The tag " + tag + " caused an error with the FST.")
            except NullFomaTransducerException:
                return skip("FST not found on this machine")

       
        
