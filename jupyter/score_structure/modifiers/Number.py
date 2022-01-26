from dataclasses import dataclass
import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import Modifier


class Number(Modifier):

    NUMBERS = ['fingering0', 'fingering1', 'fingering2', 'fingering3', 'fingering4', 'fingering5', 'tuplet3', 'tuplet6']

    NUMBERS_MAP = {'fingering0': 1, 'fingering1': 1, 'fingering2': 2, 'fingering3': 3, 'fingering4': 4,
                   'fingering5': 5, 'tuplet3': 3, 'tuplet6': 3
                   }

    def transform_independent_symbol(self, parent: ET.Element):
        if parent.tag == 'technical':

            fingering = ET.Element('fingering')
            fingering.text = self.NUMBERS_MAP[self.typ]
            parent.append(fingering)

        return parent
