from dataclasses import dataclass
import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import Modifier


class Ornament(Modifier):

    ORNAMENTS = ['ornamentMordent', 'ornamentTrill', 'ornamentTurn', 'ornamentTurnInverted']

    ORNAMENTS_MAP = {'ornamentMordent': 'mordent',
                    'ornamentTrill': 'trill-mark',
                    'ornamentTurn': 'turn',
                    'ornamentTurnInverted': 'inverted-turn'
                    }

    def transform_independent_symbol(self, parent: ET.Element):
        if parent.tag == 'notations':

            ornaments = parent.find('ornaments')
            ornament = ET.Element(self.ORNAMENTS_MAP[self.typ])

            if ornaments is not None:
                ornaments.append(ornament)
            else:
                ornaments = ET.Element('ornaments')
                ornaments.append(ornament)
                parent.append(ornaments)

        return parent
