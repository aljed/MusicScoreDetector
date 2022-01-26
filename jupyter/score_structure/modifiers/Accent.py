from dataclasses import dataclass
import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import Modifier


class Accent(Modifier):

    ACCENTS = ['articAccentAbove', 'articAccentBelow', 'articMarcatoAbove', 'articMarcatoBelow',
               'articStaccatissimoAbove', 'articStaccatissimoBelow', 'articStaccatoAbove', 'articStaccatoBelow',
               'articTenutoAbove', 'articTenutoBelow']

    ACCENTS_MAP = {'articAccentAbove': 'accent',
                   'articAccentBelow': 'accent',
                   'articMarcatoAbove': 'marcato',
                   'articMarcatoBelow': 'marcato',
                   'articStaccatissimoAbove': 'staccatissimo',
                   'articStaccatissimoBelow': 'staccatissimo',
                   'articStaccatoAbove': 'staccato',
                   'articStaccatoBelow': 'staccato',
                   'articTenutoAbove': 'tenuto',
                   'articTenutoBelow': 'tenuto'
                   }

    def transform_independent_symbol(self, parent: ET.Element):
        if parent.tag == 'articulations':

            if parent.find(self.ACCENTS_MAP[self.typ]) is None:
                accent = ET.Element(self.ACCENTS_MAP[self.typ])
                parent.append(accent)

        return parent
