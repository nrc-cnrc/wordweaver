"""
Create API Resource for returning all available pronouns

"""

from flask import jsonify, Blueprint, abort
import json
from flask_restful import (Resource, Api, reqparse, inputs, fields, url_for, marshal_with)
from flask_cors import CORS
from wordweaver.data import pronoun_data
from wordweaver.resources import require_appkey
from wordweaver.config import INTERFACE_CONFIG, LANG_CONFIG
from slugify import slugify

for pn in pronoun_data:
    pn['tag'] = slugify(pn['tag'])

pronoun_fields = {
    'person': fields.String,
    'number': fields.String,
    'gender': fields.String,
    'inclusivity': fields.String,
    'role': fields.String,
    'value': fields.String,
    'gloss': fields.String,
    'obj_gloss': fields.String,
    'position': fields.Integer,
    'tag': fields.String
}

# Possible combinations

class PnOptions():
    def __init__(self):
        self.transitive_filter = False
        for vtype, v in LANG_CONFIG['verb_type'].items():
            if v['pronouns'] == 'transtive':
                self.transitive_filter = v['filter']
        
   
    def intransAgentPros(self, neutral_tag = '3-sg-n'):
        return  [{"agent": pronoun, "patient": [x for x in pronoun_data if x['tag'] == neutral_tag][0] } for pronoun in pronoun_data]

    def intransPatientPros(self, neutral_tag = '3-sg-n'):
        return  [{"patient": pronoun, "agent": [x for x in pronoun_data if x['tag'] == neutral_tag][0] } for pronoun in pronoun_data]
   
    def transPros(self):
        pns = []
        for agent in pronoun_data:
            for patient in pronoun_data:
                passed = True
                if self.transitive_filter:
                    for f in self.transitive_filter:
                        ag_key = f['agent']['key']
                        ag_val = f['agent']['value']
                        pat_key = f['patient']['key']
                        pat_val = f['patient']['value']
                        if agent[ag_key] == ag_val and patient[pat_key] == pat_val:
                            passed = False
                        
                if passed:
                    pns.append({"agent": agent, "patient": patient})
        return pns

class PronounList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'tag', dest='tag',
            type=str, location='args', action='append',
            required=False, help="A tag to filter",
        )
    @marshal_with(pronoun_fields)
    @require_appkey
    def get(self):
        args = self.parser.parse_args()
        if args['tag']:
            return [pronoun for pronoun in pronoun_data if pronoun['tag'] in args['tag']], {'X-total-count': len(pronoun_data)}
        return [pronoun for pronoun in pronoun_data], {'X-total-count': len(pronoun_data)}


class Pronoun(Resource):
    @marshal_with(pronoun_fields)
    @require_appkey
    def get(self, tag):
        try:
            selected_pronoun = next(pronoun for pronoun in pronoun_data if pronoun['tag'] == slugify(tag))
        except StopIteration:
            abort(404)
        return selected_pronoun, {'X-total-count': len(pronoun_data)}

pronoun_api = Blueprint('resources.pronoun', __name__)

CORS(pronoun_api)

api = Api(pronoun_api)

api.add_resource(
    PronounList,
    '/pronouns',
    endpoint='pronouns'
)

api.add_resource(
    Pronoun,
    '/pronouns/<string:tag>',
    endpoint='pronoun'
)
