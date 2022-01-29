from dataclasses import dataclass
import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import Modifier


class Ornament(Modifier):

    ORNAMENTS = ['ornamentTrill', 'ornamentTurn', 'ornamentTurnInverted', 'ornamentMordent', 'tremolo1', 'tremolo2',
                 'tremolo3', 'tremolo4', 'tremolo5',   'fermataAbove', 'fermataBelow',]

    ORNAMENTS_MAP = {'ornamentTrill': 'trill-mark',
                     'ornamentTurn': 'turn',
                     'ornamentTurnInverted': 'inverted-turn',
                     'ornamentMordent': 'mordent',
                     # 'tremolo1',
                     # 'tremolo2',
                     # 'tremolo3',
                     # 'tremolo4',
                     # 'tremolo5',
                     # 'fermataAbove',
                     # 'fermataBelow',
                    }

    def transform_independent_symbol(self, parent: ET.Element):
        return parent
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
