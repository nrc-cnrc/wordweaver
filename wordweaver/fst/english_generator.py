import re
from wordweaver.data import pronoun_data as pd, verb_data as vd
from wordweaver.config import LANG_CONFIG

class EnglishGenerator():
    """Generate basic plain English based on tag from FstTagMaker
    """
    def __init__(self):
        self.template = "{subject}{stuff}{verb}{obj}"
        self.dictionary = ( {"Fut": "will"},
                            {"Cond": "would"},
                            {"FPast": "used to"},
                            {"Cont": "keep on"})
        
        self.erroneous_tags = ["Verb"]
        self.verb_types = ["Active", "Passive", "Transitive"]
        self.sample = "Verb+Passive+AgentSg3Neuter+PatSg3Mal+athonte+Habitual"
        self.first = [pn['gloss'] for pn in pd if pn['tag'].startswith('1')]
        self.third = [pn['gloss'] for pn in pd if pn['tag'].startswith('3-sg')]
        self.dual = [pn['gloss'] for pn in pd if 'dl' in pn['tag']]
        self.plural = [pn['gloss'] for pn in pd if 'pl' in pn['tag']]
        self.non_pres = ["Fut", "Cond", "FPast", "Cont"]
        self.past_tags = ["DefPast"]
        self.inf_tags = ["Fut", "Cond", "FPast"]

    def return_copula(self, subj, tags):
        # breakpoint()
        if any((t in self.inf_tags for t in tags)):
            return "be"
        if any((t in self.past_tags for t in tags)):
            tense = 'past'
        else:
            tense = ''
        if subj in self.first and not subj in self.dual:
            if tense == 'past':
                return "was "
            else:
                return "am "
        elif subj in self.third:
            if tense == 'past':
                return "was "
            else:
                return "is "
        else:
            if tense == 'past':
                return "were "
            else:
                return "are "
    
    def return_have(self, subj):
        if subj in self.third:
            return "has "
        else:
            return "have "

    def return_command(self, subj_pn):
        if subj_pn['person'] == '2':
            return f"({subj_pn['gloss']}) "
        else:
            return f"Let {subj_pn['obj_gloss'].lower()} "

    def transduce_tags(self, tag):
        subject = ''
        stuff = ''
        verb = ''
        obj = ''
        tags = [t for t in tag.split("+") if t not in self.erroneous_tags]
        # find subj/obj and remove tags
        atag = [t for t in tags if t.startswith("Agent")][0]
        ptag = [t for t in tags if t.startswith("Pat")][0]
        verb_type = [t for t in tags if t in self.verb_types][0]
        pronouns = {v:k for k,v in LANG_CONFIG['pronouns'].items()}
        pat_pronoun = None



        if "Active" in tags:
            if "Command" in tags:
                pn = [p for p in pd if p['tag'] == pronouns[atag.replace("Agent", "")]][0]
                subject = self.return_command(pn)
            else:
                subject = [p for p in pd if p['tag'] == pronouns[atag.replace("Agent", "")]][0]['gloss'] + " "
        elif "Passive" in tags:
            if "Command" in tags:
                pn = [p for p in pd if p['tag'] == pronouns[ptag.replace("Pat", "")]][0]
                subject = self.return_command(pn)
            else:
                subject = [p for p in pd if p['tag'] == pronouns[ptag.replace("Pat", "")]][0]['gloss'] + " "
        elif "Transitive" in tags:
            if "Command" in tags:
                pn = [p for p in pd if p['tag'] == pronouns[atag.replace("Agent", "")]][0]
                subject = self.return_command(pn)
            else:
                subject = [p for p in pd if p['tag'] == pronouns[atag.replace("Agent", "")]][0]['gloss'] + " "

            obj = " " + [p for p in pd if p['tag'] == pronouns[ptag.replace("Pat", "")]][0]['obj_gloss'].lower()
            pat_pronoun = "" + [p for p in pd if p['tag'] == pronouns[ptag.replace("Pat", "")]][0]['obj_gloss'].lower()

        
        tags = [t for t in tags if t != atag and t != ptag and t != verb_type]




        # get verb
        try:
            vtag = [v for v in tags if v.islower()][0]
            verb_obj = [v for v in vd if v['tag'] == vtag][0]
            if "Cont" in tags:
                verb = verb_obj['eng-prog']
            elif ("Progr" in tags and "Perf" in tags) or "Progr" in tags or "State" in tags:
                if "State" in tags:
                    if "Perf" not in tags:
                        #this is Stative present
                        if 'stative-pres-trans' in verb_obj.keys() and verb_obj['stative-pres-trans'].strip() != '':
                            #the translation of this Stative present is irregular
                            #verb = self.return_copula(subject.strip(), tags) + verb_obj['stative-pres-trans']
                            state_form = verb_obj['stative-pres-trans']
                            if 'COP' in state_form:
                                state_form = state_form.replace('COP', '')
                                verb = self.return_copula(subject.strip(), tags) + state_form
                            else:
                                verb = verb_obj['stative-pres-trans']
                        else:
                            verb = self.return_copula(subject.strip(), tags) + verb_obj['eng-prog']
                    else:
                        #this is Stative Perfective
                        if 'stative-perf-trans' in verb_obj.keys() and verb_obj['stative-perf-trans'].strip() != '':
                            #the stative perfect form is an irregular one
                            self.return_have(subject.strip()) + verb_obj['stative-perf-trans']
                        else:
                            self.return_have(subject.strip()) + verb_obj['eng-perf']
                else:
                    #this is not a Stative form
                    verb = self.return_copula(subject.strip(), tags) + verb_obj['eng-prog']
            elif ("Progr" in tags and "Perf" in tags) or "Progr" in tags:
                verb = self.return_copula(subject.strip(), tags) + verb_obj['eng-prog']
            elif "Perf" in tags and not any((x in self.non_pres for x in tags)):
                verb = self.return_have(subject.strip()) + verb_obj['eng-perf']
            elif "Perf" in tags:
                verb = "have " + verb_obj['eng-perf']
            elif "DefPast" in tags:
                verb = verb_obj['eng-past']
            elif subject.strip() in self.third and not any((x in self.non_pres for x in tags)): 
                verb = verb_obj['eng-3']
            else:
                verb = verb_obj['eng-inf']
            verb = self.edit_verb(verb_type, verb, ptag, pat_pronoun)
        except IndexError:
            return "Sorry, we don't have an English translation for this yet."

        # get stuff
        for x in self.dictionary:
            st = list(x.keys())[0]
            if st in tags:
                stuff += x[st] + " "
        dtags = [list(t.keys())[0] for t in self.dictionary]
        # tags = [t for t in tags if t not in dtags]
        
        # resolve copulas
        verb = verb.replace("COP", self.return_copula(subject.strip(), tags))

        sentence = self.template.format(subject=subject, stuff=stuff, verb=verb, obj='')

        # resolve empty space
        sentence = sentence.replace("  ", " ")
        return sentence

    def edit_verb(self, verb_type, verb_text, ptag, pat_pronoun = None):
        new_verb_text = verb_text
        if "Transitive" in verb_type:
            #replace 'something/someone' or 'someone' with a corresponding patient pronoun
            new_verb_text = verb_text.replace ('someone/something', pat_pronoun)
            new_verb_text = new_verb_text.replace('someone', pat_pronoun)
            #new_verb_text = verb_text.replace('someone/something', '')
        elif "Active" in verb_type or "Passive" in verb_type:
            #replace 'something/someone' with 'something'
            #new_verb_text = verb_text.replace ('someone/something', 'something')
            pass

        return new_verb_text

if __name__ == '__main__':
    eg = EnglishGenerator()
    print(eg.transduce_tags(eg.sample))
    
