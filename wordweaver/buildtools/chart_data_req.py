import requests
import json
from wordweaver.data import pronoun_data, verb_data
from wordweaver.resources.affix import AFFIX_OPTIONS
from pydash import merge
from wordweaver.config import BUILD_CONFIG


class ChartData():
    def __init__(self):                
        self.PATH = BUILD_CONFIG['echart']['path']
        vres = requests.get(self.PATH.format(ep="verbs"))
        self.no_of_verbs = len(vres.json())
        self.affopts = AFFIX_OPTIONS['AFFIX_OPTIONS']
        self.verbs = verb_data
        self.pronouns = pronoun_data
    
    def getConjugations(self):
        limit = 5
        offset = 0
        conjugations = []
        while limit < self.no_of_verbs:
            print(limit)
            res = requests.get(self.PATH.format(ep="conjugations"), params={"limit": limit, "offset": offset})
            print(res.status_code)
            conjugations += res.json()
            if limit + 5 < self.no_of_verbs:
                limit += 5
                offset += 5
            elif limit > self.no_of_verbs:
                limit = self.no_of_verbs
                offset += 5
            else:
                break
        jsd = json.dumps(conjugations)
        with open('alldata.json', 'w+') as f:
            f.write(jsd)

    def returnValue(self, conj):
        morphemes = [conj['aspect'], conj['root'], conj['pronoun']]
        
        for m in conj['post_aspect']:
            morphemes.append(m)
        
        for m in conj['required_affixes']:
            morphemes.append(m)

        for m in conj['tmp_affix']:
            morphemes.append(m)

        morphemes.sort(key=lambda x: x['position'])

        return "".join([m['value'] for m in morphemes])
    
    def createChartData(self, conjs):
        data = []
        node = {}
        for conj in conjs:
            v = conj['root']['tag']
            t = next(iter([a for a in self.affopts if a['tag'] == conj['affopt']]))['gloss']
            vb = next(iter([verb for verb in self.verbs if verb['tag'] == v]))
            if 'red' == vb['thematic_relation']:
                p = [p for p in self.pronouns if p['tag'] == conj['pronoun']['agent']][0]['gloss']
            elif 'blue' == vb['thematic_relation']:
                p = [p for p in self.pronouns if p['tag'] == conj['pronoun']['patient']][0]['gloss']
            else:
                p = next(iter([p for p in self.pronouns if p['tag'] == conj['pronoun']['agent']]))['gloss'] + ' > ' + next(iter([p for p in self.pronouns if p['tag'] == conj['pronoun']['patient']]))['obj_gloss']
            val = self.returnValue(conj)
            # newconj = {v: { t: { p: val}}}
            newconj = {v: {p: {t: val}}}
            node = merge(node, newconj)
        
        for verb in node.keys():
            nv = {"name": verb, "children": []}
            for second in node[verb].keys():
                ns = {"name": second, "children": []}
                for third in node[verb][second].keys():
                    nt = {"name": third, "children": [{"name": node[verb][second][third]}]}
                    ns['children'].append(nt)
                nv['children'].append(ns)
            data.append(nv)
        return data

    def exportToEcharts(self):
        with open('alldata.json', 'r') as f:
            conjugations = json.load(f)
        data = self.createChartData(conjugations)
        with open('data.json', 'w') as f:
            ndata = [{"name": BUILD_CONFIG['echart']['path'], "children": data}]
            f.write(json.dumps(ndata))
        
cd = ChartData()
cd.getConjugations()
cd.exportToEcharts()

