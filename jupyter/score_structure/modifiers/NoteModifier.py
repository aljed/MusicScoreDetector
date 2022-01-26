from dataclasses import dataclass
import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import Modifier


class NoteModifier(Modifier):

    NOTATIONS = ['augmentationDot']

    NOTATIONS_MAP = {'augmentationDot': 'dot'}

    def transform_independent_symbol(self, parent: ET.Element):
        if parent.tag == 'note':

            dot = ET.Element(self.NOTATIONS_MAP[self.typ])
            parent.append(dot)

        return parent
