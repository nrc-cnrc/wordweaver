from flask import abort

from collections import OrderedDict
from wordweaver.data import affix_data, pronoun_data, verb_data
import re
from wordweaver.exceptions import FomaInputException
from wordweaver.resources.affix import AFFIX_OPTIONS

from wordweaver.resources.pronoun import PnOptions

from wordweaver.config import INTERFACE_CONFIG, LANG_CONFIG

import logging

class FstEncoder:
    """
    A class for batch creating upper-side sequence of morphological tags to be submitted to the FST
    with
    down fst_tag
    Template follows spec from FST_CONFIG['template']

    """

    def __init__(self, args):
        logging.basicConfig()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.template = "".join(INTERFACE_CONFIG['encoding']['template'])
        self.template_args = OrderedDict({re.sub(re.compile('[\{\}]'), '', k): "" for k in INTERFACE_CONFIG['encoding']['template'] if "{" in k})
        self.args = args
        self.all_pronoun_tags = [x['tag'] for x in pronoun_data]
        aff_options = AFFIX_OPTIONS['AFFIX_OPTIONS']
        self.AFF_OPTIONS = aff_options

    def parse_person(self, pn):
        return LANG_CONFIG['pronouns'][pn['tag']]

    def fill_template(self):
        variables_pattern = re.compile('(?<=\{)\w+(?=\})')
        template = self.template
        index = 0
        for match in variables_pattern.finditer(template):
            template = re.sub(re.compile('\{' + match.group() + '\}'), '{' + str(index) + '}', template)
            index += 1
        args_list = [v for v in self.template_args.values()]
        return template.format(*args_list)

    def return_pronouns(self, verb_type):
        """
        Find pronoun according to args, return 404 if not found, set to default pn if verb is blue, else all pns    

        """

        pnopts = PnOptions()

        if LANG_CONFIG['verb_type'][verb_type]['pronouns'] == 'patient':
            pronouns = pnopts.intransPatientPros()
        elif LANG_CONFIG['verb_type'][verb_type]['pronouns'] == 'agent':
            pronouns = pnopts.intransAgentPros()
        elif LANG_CONFIG['verb_type'][verb_type]['pronouns'] == 'transitive':
            pronouns = pnopts.transPros()
        else:
            abort(400, description=f"There is an error in your configuration. Your verb types must be associated with either 'agent', 'patient', or 'transtive' pronouns")
      
        # check agent has a value
        if self.args['agent']:
            # filter all valid pronouns based on value. If none exist, return 400 or 404
            pronouns = [x for x in pronouns if x['agent']['tag'] in self.args['agent']]
            if not pronouns:
                if not [x for x in self.all_pronoun_tags if x in self.args['agent']]:
                    abort(404, description="The pronoun with a tag '{}' does not exist.".format(self.args['agent']))
                else:
                    abort(400, description="Using the agent tag '{ag}', with the patient tag '{pat}', affix option '{aff}' and verb '{vb}' is not valid.".format(ag=self.args['agent'], pat=self.args['patient'], vb=self.args['root'], aff=self.args['aff-option']))

        # check patient has a value
        if self.args['patient']:
            # filter all valid pronouns based on value. If none exist, return 400 or 404
            pronouns = [x for x in pronouns if x['patient']['tag'] in self.args['patient']]
            if not pronouns:
                if not [x for x in self.all_pronoun_tags if x in self.args['patient']]:
                    abort(404, description="The pronoun with a tag '{}' does not exist.".format(self.args['patient']))
                else:
                    abort(400, description="Using the agent tag '{ag}', with the patient tag '{pat}', affix option '{aff}' and verb '{vb}' is not valid.".format(ag=self.args['agent'], pat=self.args['patient'], vb=self.args['root'], aff=self.args['aff-option']))
      
        return pronouns

    def return_tags(self):
        """
        A method for the conjugations endpoint.
        """

        # find verb, return 404 if not found, set to range between offset and limit otherwise
        if self.args['root']:
            verb = [verb for verb in verb_data if verb["tag"] in self.args['root']]
            if not verb:
                abort(404, description="The verb with a tag '{}' does not exist".format(self.args['root']))
        else:
            verb = verb_data[self.args['offset']:self.args['limit']]
      
        if self.args['aff-option']:
            affoption = [affoption for affoption in self.AFF_OPTIONS if affoption['tag'] in self.args['aff-option']]
            if not affoption:
                abort(404, description="The affix option with a tag '{}' does not exist".format(self.args['aff-option']))

        else:
            affoption = self.AFF_OPTIONS
     
        # tags for FST
        tags = []

        # tags for HTTP response
        id_tags = []

        # for each verb
        for vb in verb:
            # tag for FST
            self.template_args['root'] = vb["tag"]
            verb_root_id_tag = self.template_args['root']

            verb_type = vb["thematic_relation"]            
            self.template_args['verb_type'] = LANG_CONFIG['verb_type'][verb_type]['tag']

            # for each affoption
            for affopt in affoption:
                # tags for HTTP response **needs +recursive**
                affopt_id_tag = affopt['tag']

                # tags for FST
                for aff_type, affixes in LANG_CONFIG['affixes'].items():
                    self.template_args[aff_type] = ''
                    for aff in affopt['affixes']:
                        if aff['type'] == aff_type:
                            self.template_args[aff_type] = affixes[aff['tag']]['tag']
                
                # for each pronoun
                for pronoun in self.return_pronouns(verb_type):
                    # tags for HTTP
                    agent_id_tag = pronoun['agent']['tag']
                    patient_id_tag = pronoun['patient']['tag']
                    # tags for FST
                    self.template_args['agent'] = LANG_CONFIG['pronoun_role']["agent"] + self.parse_person(pronoun["agent"]) + "+"
                    self.template_args['patient'] = LANG_CONFIG['pronoun_role']["patient"] + self.parse_person(pronoun["patient"]) + "+"

                     # change verb_thematic_relation_tag if aspect is perf TODO: How to put this in config?
                    if INTERFACE_CONFIG['encoding']['post_processing']:
                        for process in INTERFACE_CONFIG['encoding']['post_processing']:
                            conditions = process['conditions']
                            results = process['results']
                            conditions_met = [self.template_args[cond['template_arg_key']] == cond['equal_to'] for cond in conditions]
                            if all(conditions_met):
                                for result in results:
                                    if "operation" in result:
                                        if result['operation'] == 'switch_pros':
                                            self.template_args['agent'] = LANG_CONFIG['pronoun_role']['agent'] + self.parse_person(pronoun['patient']) + '+'
                                            self.template_args['patient'] = LANG_CONFIG['pronoun_role']['patient'] + self.parse_person(pronoun['agent']) + '+'
                                    else:
                                        self.template_args[result['template_arg_key']] = result['equal_to']

                    filled_template = self.fill_template()

                    tags.append({"fst": filled_template,
                                "http_args": {"root": verb_root_id_tag,
                                         "agent": agent_id_tag,
                                         "patient": patient_id_tag,
                                         "affopt": affopt_id_tag
                                         }})
        return tags