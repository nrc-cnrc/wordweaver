"""
Create API Resource for returning all available verbs

"""

from flask import jsonify, Blueprint, abort
import json
from flask_restful import (Resource, Api, reqparse, inputs, fields, url_for, marshal_with)
from flask_cors import CORS
from wordweaver.resources.affix import affix_fields
from wordweaver.data import affix_data, verb_data
from wordweaver.resources import require_appkey
from slugify import slugify

for v in verb_data:
    v['tag'] = slugify(v['tag'])

verb_fields = {
    'thematic_relation': fields.String,
    'display': fields.String,
    'gloss': fields.String,
    'tag': fields.String,
    'required_affixes' : fields.List(fields.Nested(affix_fields)),
    'position': fields.Integer
}

class VerbList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'thematic-relation', dest='thematic_relation',
            type=str, location='args',
            required=False, help='A thematic relation to filter',
            )
        self.parser.add_argument(
            'tag', dest='tag',
            type=str, location='args', action='append',
            required=False, help="A tag to filter",
        )

    def addRequired(self, verb):
        if "required_affixes" in list(verb.keys()) and verb["required_affixes"]:
            if type(verb["required_affixes"][0]) is str or type(verb["required_affixes"][0]) is str:
                # return any tags in verb["required"] that match affix tags in affix_data
                req_affs = []   
                for morpheme in verb["required_affixes"]:
                    req_affs += [x for x in affix_data if x['tag'] == morpheme]
                verb["required_affixes"] = req_affs
                return verb
            else:
                return verb
        else:
            verb['required_affixes'] = []
            return verb

    @marshal_with(verb_fields)
    @require_appkey
    def get(self):
        args = self.parser.parse_args()
        thematic_relation = args['thematic_relation']
        if args['tag']:
            return [self.addRequired(verb) for verb in verb_data if verb['tag'] in args['tag']], {'X-total-count': len(verb_data)}
        if thematic_relation:
            return [self.addRequired(verb) for verb in [x for x in verb_data if thematic_relation == x['thematic_relation']]], {'X-total-count': len(verb_data)}
        else:
            return [self.addRequired(verb) for verb in verb_data], {'X-total-count': len(verb_data)}


class Verb(Resource):
    def addRequired(self, verb):
        if "required_affixes" in list(verb.keys()) and verb["required_affixes"]:
            if type(verb["required_affixes"][0]) is str or type(verb["required_affixes"][0]) is str:
                # return any tags in verb["required"] that match affix tags in affix_data   
                verb["required_affixes"] = [[x for x in affix_data if x['tag'] == morpheme] for morpheme in verb['required_affixes']]
                return verb
            else:
                return verb
        else:
            verb['required_affixes'] = []
            return verb

    @marshal_with(verb_fields)
    @require_appkey
    def get(self, tag):
        try:
            selected_verb = next(self.addRequired(verb) for verb in verb_data if verb['tag'] == slugify(tag))
        except StopIteration:
            abort(404)
        return selected_verb, {'X-total-count': len(verb_data)}

verb_api = Blueprint('resources.verb', __name__)

CORS(verb_api)

api = Api(verb_api)

api.add_resource(
    VerbList,
    '/verbs',
    endpoint='verbs'
)

api.add_resource(
    Verb,
    '/verbs/<string:tag>',
    endpoint='verb'
)
