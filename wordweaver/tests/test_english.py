from unittest import TestCase
from wordweaver.fst.english_generator import EnglishGenerator
from wordweaver.data import pronoun_data as pd, verb_data as vd


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
        print ('Verb+Fut+Active+AgentSg1+PatSg3Neuter+kweny-r+Punct -> ' + self.eg.transduce_tags(
            'Verb+Fut+Active+AgentSg1+PatSg3Neuter+kweny-r+Punct') + '<> I will be able')
        self.assertEqual(self.eg.transduce_tags('Verb+Fut+Active+AgentSg1+PatSg3Neuter+kweny-r+Punct'), "I will be able")
        self.assertEqual(self.eg.transduce_tags('Verb+Cond+Active+AgentSg1+PatSg3Neuter+kweny-r+Punct'), "I would be able")
        self.assertEqual(self.eg.transduce_tags('Verb+Active+AgentSg1+PatSg3Neuter+kweny-r+Habitual'), 'I am able')
        self.assertEqual(self.eg.transduce_tags('Verb+Active+AgentSg1+PatSg3Neuter+nenhskw-r+State'), 'I am stealing something')

    def test_transitive(self):
        str = self.eg.transduce_tags(
            'Verb+Transitive+AgentSg1+PatSg3Mal+kwennyenhst-p+State')
        print ('Verb+Fut+Transitive+AgentSg1+PatSg2+kwennyenhst-p+Punct -> ' + self.eg.transduce_tags(
            'Verb+Fut+Transitive+AgentSg1+PatSg2+kwennyenhst-p+Punct') + '<> I will respect you')

        self.assertEqual('I will respect you', self.eg.transduce_tags('Verb+Fut+Transitive+AgentSg1+PatSg2+kwenyenst-p+Punct'))

        self.assertEqual('I would respect him',
                         self.eg.transduce_tags('Verb+Cond+Transitive+AgentSg1+PatSg3Mal+kwenyenst-p+Punct'))
        self.assertEqual('I respected you',
                         self.eg.transduce_tags('Verb+DefPast+Transitive+AgentSg1+PatSg2+kwenyenst-p+Punct'))
        self.assertEqual('I respect you',
                         self.eg.transduce_tags('Verb+Transitive+AgentSg1+PatSg2+kwenyenst-p+Habitual'))
        self.assertEqual('Let me respect you',
                         self.eg.transduce_tags('Verb+Transitive+AgentSg1+PatSg2+kwenyenst-p+Command'))
        self.assertEqual('I am respecting you',
                         self.eg.transduce_tags('Verb+Transitive+AgentSg1+PatSg2+kwenyenst-p+State'))
        self.assertEqual('I am respecting him',
                         self.eg.transduce_tags('Verb+Transitive+AgentSg1+PatSg3Mal+kwenyenst-p+State'))

        #convince someone of something
        self.assertEqual('I will convince him of something',
                         self.eg.transduce_tags('Verb+Fut+Transitive+AgentSg1+PatSg3Mal+7nikonhrakweny-p+Punct'))
        self.assertEqual('(You) convince him of something',
                         self.eg.transduce_tags('Verb+Transitive+AgentSg2+PatSg3Mal+7nikonhrakweny-p+Command'))

        #see someone/something
        self.assertEqual('I will see him',
                         self.eg.transduce_tags('Verb+Fut+Transitive+AgentSg1+PatSg3Mal+ken-p+Punct'))

        #make something for someone
        self.assertEqual('I will make something for him',
                         self.eg.transduce_tags('Verb+Fut+Transitive+AgentSg1+PatSg3Mal+onnyen-p+Punct'))



    def test_blue(self):
        self.assertEqual('She will get hurt',
                         self.eg.transduce_tags('Verb+Fut+Passive+AgentSg3Neuter+PatSg3Fem+karewaht-b+Punct'))
        self.assertEqual('(You) get hurt',
                         self.eg.transduce_tags('Verb+Passive+AgentSg3Neuter+PatSg2+karewaht-b+Command'))
        self.assertEqual('(You) get angry',
                         self.eg.transduce_tags('Verb+Passive+AgentSg3Neuter+PatSg2+na7khwen-b+Command'))

    def test_red(self):
        self.assertEqual('She will respect something; value something',
                         self.eg.transduce_tags('Verb+Fut+Active+AgentSg3Fem+PatSg3Neuter+kwenyenhst-r+Punct'))
        self.assertEqual('(You) respect something; value something',
                         self.eg.transduce_tags('Verb+Active+AgentSg2+PatSg3Neuter+kwenyenhst-r+Command'))
        # AgentDu31
        self.assertEqual('S.o and I are respecting something; valuing something',
                         self.eg.transduce_tags('Verb+Active+AgentDu31+PatSg3Neuter+kwenyenhst-r+State'))

        self.assertEqual('You and I are respecting something; valuing something',
                        self.eg.transduce_tags('Verb+Active+AgentDu21+PatSg3Neuter+kwenyenhst-r+State'))


    def test_command(self):
        self.assertEqual(self.eg.transduce_tags('Verb+Active+AgentSg2+PatSg3Neuter+atenhninon-r+Command'), '(You) sell something')
        self.assertEqual(self.eg.transduce_tags('Verb+Active+AgentSg1+PatSg3Neuter+atenhninon-r+Command'), 'Let me sell something')

    def test_stative_pres_regular(self):
        self.assertEqual('I am respecting him',
                         self.eg.transduce_tags('Verb+Transitive+AgentSg1+PatSg3Mal+kwenyenst-p+State'))
        self.assertEqual('I am stealing something',
                         self.eg.transduce_tags('Verb+Active+AgentSg1+PatSg3Neuter+nenhskw-r+State'))



    def test_stative_pres_irregular(self):
        self.assertEqual('I am angry',
                         self.eg.transduce_tags('Verb+Passive+AgentSg3Neuter+PatSg1+na7khwen-b+State'))

        #this is a non-copular construction
        self.assertEqual('I have lice',
                         self.eg.transduce_tags('Verb+Passive+AgentSg3Neuter+PatSg1+tsi7nonhtara7n-b+State'))

        # a transitive verb
        self.assertEqual('I am cheating him',
                         self.eg.transduce_tags('Verb+Transitive+AgentSg1+PatSg3Mal+7nikonhrha7ten-p+State'))

    def test_progressive(self):
        self.assertEqual('I am getting angry', self.eg.transduce_tags(
            'Verb+Passive+AgentSg3Neuter+PatSg1+na7khwen-b+Perf+Progr'))
