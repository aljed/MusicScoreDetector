from dataclasses import dataclass
import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import Modifier


class Dynamic(Modifier):

    DYNAMICS = ['dynamicFF', 'dynamicFFF', 'dynamicFFFF', 'dynamicFFFFF', 'dynamicForte', 'dynamicFortePiano',
                'dynamicMezzo', 'dynamicMF', 'dynamicMP', 'dynamicPiano', 'dynamicPP', 'dynamicPPP', 'dynamicPPPP',
                'dynamicPPPPP', 'dynamicRinforzando2', 'dynamicSforzando1', 'dynamicSforzato']

    DYNAMICS_MAP = {'dynamicFF': 'ff',
                    'dynamicFFF': 'fff',
                    'dynamicFFFF': 'ffff',
                    'dynamicFFFFF': 'fffff',
                    'dynamicForte': 'f',
                    'dynamicFortePiano': 'fp',
                    'dynamicMezzo': 'n',  # todo
                    'dynamicMF': 'mf',
                    'dynamicMP': 'mp',
                    'dynamicPiano': 'p',
                    'dynamicPP': 'pp',
                    'dynamicPPP': 'ppp',
                    'dynamicPPPP': 'pppp',
                    'dynamicPPPPP': 'ppppp',
                    'dynamicRinforzando2': 'rf',
                    'dynamicSforzando1': 'sfz',
                    'dynamicSforzato': 'sf'
                    }

    def transform_independent_symbol(self, parent: ET.Element):
        if parent.tag == 'notations':

            if parent.find(self.DYNAMICS_MAP[self.typ]) is None:
                dynamic = ET.Element(self.DYNAMICS_MAP[self.typ])
                parent.append(dynamic)

        return parent
