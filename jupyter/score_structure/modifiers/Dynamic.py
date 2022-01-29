from dataclasses import dataclass
import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import Modifier


class Dynamic(Modifier):

    DYNAMICS = ['dynamicP', 'dynamicM', 'dynamicF', 'dynamicS', 'dynamicZ', 'dynamicR']

    DYNAMICS_MAP = {'dynamicP': 'p',
                    'dynamicM': 'm',
                    'dynamicF': 'f',
                    'dynamicS': 's',
                    'dynamicZ': 'z',
                    'dynamicR': 'r'
                    }

    def transform_independent_symbol(self, parent: ET.Element):
        if parent.tag == 'notations':

            if parent.find(self.DYNAMICS_MAP[self.typ]) is None:
                dynamic = ET.Element(self.DYNAMICS_MAP[self.typ])
                parent.append(dynamic)

        return parent
