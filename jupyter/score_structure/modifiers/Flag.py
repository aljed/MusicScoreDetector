from dataclasses import dataclass
import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import Modifier


class Flag(Modifier):

    FLAGS = ['flag8thUp', 'flag8thUpSmall', 'flag16thUp', 'flag32ndUp', 'flag64thUp', 'flag128thUp', 'flag8thDown',
              'flag8thDownSmall', 'flag16thDown', 'flag32ndDown', 'flag64thDown', 'flag128thDown']

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


class Beam(Modifier):

    BEAM = ['beam']


def transform_by_beans_number(beans, parent):
    if parent.tag == 'note':
        txt = 'quarter'
        if beans == 1:
            txt = '8th'
        elif beans == 2:
            txt = '16th'
        elif beans == 3:
            txt = '32nd'
        elif beans == 4:
            txt = '64th'
        elif beans == 5:
            txt = '128th'
        typ = parent.find('type')
        typ.text = txt
    return parent
