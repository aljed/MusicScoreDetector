from dataclasses import dataclass
import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import Modifier


class NoteModifier(Modifier):

    NOTATIONS = ['fermataAbove', 'fermataBelow',  'arpeggiato']

    NOTATIONS_MAP = {'fermataAbove': 'fermata',
                     'fermataBelow': 'fermata',
                     'arpeggiato': 'arpeggiate'}

    def transform_independent_symbol(self, parent: ET.Element):
        if parent.tag == 'notations':

            new_element = ET.Element(self.NOTATIONS_MAP[self.typ])
            parent.append(new_element)

        return parent
