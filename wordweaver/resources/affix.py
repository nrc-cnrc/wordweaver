"""

Create API Resource for returning all available affixs

"""
from flask import jsonify, Blueprint, abort
import json
from flask_restful import (Resource, Api, reqparse, inputs, fields, url_for, marshal_with, marshal)
from flask_cors import CORS
from wordweaver.data import affix_data
from wordweaver.resources import require_appkey
from wordweaver.config import LANG_CONFIG
from slugify import slugify
from itertools import chain
import yaml
import os

for af in affix_data:
    af['tag'] = slugify(af['tag'])

affix_fields = {
    # 'id': fields.Integer,
    'gloss': fields.String,
    'tag': fields.String,
    'type': fields.String,
    'morphemes': fields.List(fields.Nested({'value': fields.String, 'position': fields.Integer}))
}

combination_fields = {
    # 'id': fields.Integer,
    'tag': fields.String,
    'gloss': fields.String,
    'affixes': fields.Nested(affix_fields)
}

# Possible combinations
def convertAffOption(aff_option):
        aff_option['tag'] = slugify(aff_option['tag'])
        aff_option['affixes'] = [item for item in affix_data if item['tag'] in aff_option['affixes']]
        return aff_option
# breakpoint()
AFFIX_OPTIONS = {}
AFFIX_OPTIONS['CONFIG'] = LANG_CONFIG['affix_options']
AFFIX_OPTIONS['_AFFIX_OPTIONS'] = tuple(ao for ao in AFFIX_OPTIONS['CONFIG'] if ao['public'])
AFFIX_OPTIONS['AFFIX_OPTIONS_TAGS'] = tuple(set(ao['tag'] for ao in AFFIX_OPTIONS['_AFFIX_OPTIONS']))
AFFIX_OPTIONS['AFFIX_OPTIONS_AFFIX_TAGS'] = tuple(chain.from_iterable([ao['affixes'] for ao in AFFIX_OPTIONS['_AFFIX_OPTIONS']]))
AFFIX_OPTIONS['AFFIX_OPTIONS'] = tuple(convertAffOption(option) for option in AFFIX_OPTIONS['_AFFIX_OPTIONS'])



class AffixList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'type', dest='type',
            type=str, location='args',
            required=False, help='A type to filter',
        )
        self.parser.add_argument(
            'tag', dest='tag',
            type=str, location='args', action='append',
            required=False, help="A tag to filter",
        )

    @marshal_with(affix_fields)
    @require_appkey
    def get(self):
        args = self.parser.parse_args()
        if args['tag']:
            return [affix for affix in [x for x in affix_data if x["tag"] in args["tag"]]]
        if args['type']:
            return [affix for affix in [x for x in affix_data if slugify(x["type"]) == slugify(args["type"])]]
        else:
            return affix_data, {'X-total-count': len(affix_data)} 

class Affix(Resource):
    @marshal_with(affix_fields)
    @require_appkey
    def get(self, tag):
        try:
            selected_affix = next(affix for affix in affix_data if affix['tag'] == slugify(tag))
        except StopIteration:
            abort(404)
        return selected_affix, {'X-total-count': len(affix_data)} 

class PossList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'tag', dest='tag',
            type=str, location='args', action='append',
            required=False, help="A tag to filter",
        )
    @require_appkey
    def get(self):
        args = self.parser.parse_args()
        aff_options = AFFIX_OPTIONS['AFFIX_OPTIONS']
        if args['tag']:
            return marshal([aff_opt for aff_opt in [x for x in aff_options if x["tag"] in args["tag"]]], combination_fields)
        return marshal(aff_options, combination_fields)

class Poss(Resource):
    @require_appkey
    def get(self, tag):
        try:
            aff_options = AFFIX_OPTIONS['AFFIX_OPTIONS']
            selected_affix_option = next(aff_option for aff_option in aff_options if aff_option['tag'] == slugify(tag))
        except StopIteration:
            abort(404)
        return selected_affix_option

affix_api = Blueprint('resources.affix', __name__)

CORS(affix_api)

api = Api(affix_api)

api.add_resource(
    AffixList,
    '/affixes',
    endpoint='affixes'
)

api.add_resource(
    Affix,
    '/affixes/<string:tag>',
    endpoint='affix'
)

api.add_resource(
    PossList,
    '/aff-options',
    endpoint='aff-options'
)

api.add_resource(
    Poss,
    '/aff-options/<string:tag>',
    endpoint='aff-option'
)
