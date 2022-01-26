from dataclasses import dataclass
import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import Modifier


class Flag(Modifier):

    CLEFS = ['cClefAlto', 'cClefAltoChange', 'cClefTenor', 'cClefTenorChange', 'clef15', 'clef8', 'fClef', 'fClefChange',
                'unpitchedPercussionClef1', 'gClef', 'gClefChange']

    FLAG_MAP = {'flag128thDown': '128th',
                'flag128thUp': '128th',
                'flag16thDown': '16th',
                'flag16thUp': '16th',
                'flag32ndDown': '32nd',
                'flag32ndUp': '32nd',
                'flag64thDown': '64th',
                'flag64thUp': '64th',
                'flag8thDown': '8th',
                'flag8thDownSmall': '8th',
                'flag8thUp': '8th',
                'flag8thUpSmall': '8th'
                }

    def transform_independent_symbol(self, parent: ET.Element):
        if parent.tag == 'note':

            typ = parent.find('type')
            typ.text = self.FLAG_MAP[self.typ]

        return parent
