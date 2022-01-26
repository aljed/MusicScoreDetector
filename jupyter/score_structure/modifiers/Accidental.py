import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import Modifier


class Accidental(Modifier):

    ACCIDENTALS = ['accidentalDoubleFlat', 'accidentalDoubleSharp', 'accidentalFlat', 'accidentalFlatSmall',
                   'accidentalNatural', 'accidentalNaturalSmall', 'accidentalSharp', 'accidentalSharpSmall',
                   # 'keyFlat', 'keyNatural', 'keySharp'
                   ]

    ACCIDENTALS_MAP = {'accidentalDoubleFlat': 'flat',
                       'accidentalDoubleSharp': 'sharp',
                       'accidentalFlat': 'flat',
                       'accidentalFlatSmall': 'flat',
                       'accidentalNatural': 'natural',
                       'accidentalNaturalSmall': 'natural',
                       'accidentalSharp': 'sharp',
                       'accidentalSharpSmall': 'sharp',
                       'keyFlat': 'flat',
                       'keyNatural': 'natural',
                       'keySharp': 'sharp'
                       }

    def transform_independent_symbol(self, parent: ET.Element):
        if parent.tag == 'note':
            present_accidental = parent.find('accidental')
            text = self.ACCIDENTALS_MAP[self.typ]

            if present_accidental is None:
                accidental = ET.SubElement(parent, 'accidental')
                accidental.text = text
                parent.append(accidental)
            else:
                new_text = text
                if present_accidental.text == 'sharp':
                    if text == 'sharp':
                        new_text = 'sharp-sharp'
                elif present_accidental.text == 'natural':
                    if text == 'sharp':
                        new_text = 'natural-sharp'
                    elif text == 'flat':
                        new_text = 'natural-flat'
                elif present_accidental.text == 'flat':
                    if text == 'flat':
                        new_text = 'flat-flat'
                present_accidental.text = new_text

        return parent
