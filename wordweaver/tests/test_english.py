from unittest import TestCase
from wordweaver.fst.english_generator import EnglishGenerator
from wordweaver.data.api_data.models import pronoun_data as pd, verb_data as vd

class EnglishTest(TestCase):
    def setUp(self):
        self.eg = EnglishGenerator()

    def test_copula(self):
        '''Make sure copulas are working with pronouns
        '''
        for pn in pd:
            self.assertEqual(self.eg.return_copula(pn, tags=self.eg.inf_tags).strip(), 'be')
            if pn in self.eg.first:
                self.assertEqual(self.eg.return_copula(pn, tags=['Pres']).strip(), 'am')
                self.assertEqual(self.eg.return_copula(pn, tags=self.eg.past_tags).strip(), 'was')
            elif pn in self.eg.third:
                self.assertEqual(self.eg.return_copula(pn, tags=['Pres']).strip(), 'is')
                self.assertEqual(self.eg.return_copula(pn, tags=self.eg.past_tags).strip(), 'was')
            else:
                self.assertEqual(self.eg.return_copula(pn, tags=['Pres']).strip(), 'are')
                self.assertEqual(self.eg.return_copula(pn, tags=self.eg.past_tags).strip(), 'were')

    def test_have(self):
        '''Make sure have helper is working with pronouns
        '''
        for pn in pd:
            if pn in self.eg.third:
                self.assertEqual(self.eg.return_have(pn).strip(), 'has')
            else:
                self.assertEqual(self.eg.return_have(pn).strip(), 'have')

    def test_problems(self):
        self.assertEqual(self.eg.transduce_tags('Verb+Fut+Active+AgentSg1+PatSg3Neuter+kwenyes-r+Punct'), "I will be able")
        self.assertEqual(self.eg.transduce_tags('Verb+Cond+Active+AgentSg1+PatSg3Neuter+kwenyes-r+Punct'), "I would be able")
        self.assertEqual(self.eg.transduce_tags('Verb+Active+AgentSg1+PatSg3Neuter+kwenyes-r+Habitual'), 'I am able')
        self.assertEqual(self.eg.transduce_tags('Verb+Active+AgentSg1+PatSg3Neuter+nenhs-r+State'), 'I am stealing something')

    def test_command(self):
        self.assertEqual(self.eg.transduce_tags('Verb+Active+AgentSg2+PatSg3Neuter+atenhninon-r+Command'), '(You) sell something')
        self.assertEqual(self.eg.transduce_tags('Verb+Active+AgentSg1+PatSg3Neuter+atenhninon-r+Command'), 'Let me sell something')