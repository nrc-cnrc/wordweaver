# -*- coding: utf-8 -*-

import re
from wordweaver.config import INTERFACE_CONFIG, LANG_CONFIG
from wordweaver.data import affix_data
from itertools import chain
from slugify import slugify

# Marker keys *MUST* start with a capital letter and values *MUST NOT*


class FstDecoder(object):
    """
    Turn FST Output like ^PP-^seni^R-^khonni^R^ into values for HTTP response

    """

    def __init__(self, fst_output):
        self.vals_pattern = re.compile(INTERFACE_CONFIG['decoding']['vals_regex'])
        self.marker_keys_pattern = re.compile(
            INTERFACE_CONFIG['decoding']['keys_regex'])
        self.keys = re.findall(self.marker_keys_pattern, fst_output)
        self.values = re.split(self.vals_pattern, fst_output)[1:]
        # list of marker tuples with 0 as marker and 1 as value
        self.markers = list(zip(self.keys, self.values))
        self._affix_constants = [v for k, v in LANG_CONFIG['affixes'].items()]
        # create big list of tuples of all tenses and aspects and post_asp suffs where 0 is slug and 1 is constants
        self.all_affix_markers = [
            (v['marker'], k) for i in self._affix_constants for k, v in i.items() if 'marker' in v]
        self.bundled_affixes = [
            (v, k) for k, v in INTERFACE_CONFIG['decoding']['bundled_affixes'].items()]

    def returnTagFromMarker(self, marker):
        for k, v in INTERFACE_CONFIG['decoding']['bundled_affixes'].items():
            if marker == k:
                return v

        for a in self.all_affix_markers:
            if a[0] == marker:
                return slugify(a[1])

    def validateMarkers(self):
        """ Return whether fst_output has valid markers"""
        valid = True
        for key in INTERFACE_CONFIG['decoding']['validation']:
            if key in INTERFACE_CONFIG['decoding'] and INTERFACE_CONFIG['decoding'][key] in self.keys:
                continue
            elif key in LANG_CONFIG['affixes']:
                valid = any(
                    [x['marker'] in self.keys for x in LANG_CONFIG['affixes'][key].values()])
            else:
                valid = False
        return valid

    def returnValuesFromMarkers(self):
        """ Return values from fst_output """
        if self.validateMarkers():
            root = INTERFACE_CONFIG['decoding']['root']
            pn = INTERFACE_CONFIG['decoding']['pronoun']
            root_val = {"position": self.keys.index(
                root), "value": [x for x in self.markers if root in x][0][1]}
            pn_val = {"position": self.keys.index(
                pn), "value": [x for x in self.markers if pn in x][0][1]}

            chosen_affixes = []
            for marker_tuple in self.bundled_affixes + self.all_affix_markers:
                if marker_tuple[0] in self.keys:
                    index = self.keys.index(marker_tuple[0])
                    affix_type = [x for x in affix_data if x["tag"] == marker_tuple[1]][0]['type']
                    chosen_affixes.append(
                        {"value": self.markers[index][1], "position": index, "tag": marker_tuple[1], "type": affix_type})

            return {"pronoun": pn_val, "root": root_val, "affixes": chosen_affixes}
        else:
            raise TypeError("Incorrect marker format")
