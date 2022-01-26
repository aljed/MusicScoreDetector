import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import IndependentSymbol


class Clef(IndependentSymbol):

    CLEFS = ['cClefAlto', 'cClefAltoChange', 'cClefTenor', 'cClefTenorChange', 'clef15', 'clef8', 'fClef', 'fClefChange',
         'unpitchedPercussionClef1', 'gClef', 'gClefChange']

    CLEF_TO_SIGN_MAP = {'cClefAlto': 'C',
                        'cClefAltoChange': 'C',
                        'cClefTenor': 'C',
                        'cClefTenorChange': 'C',
                        'clef15': 'G',
                        'clef8': 'G',
                        'fClef': 'F',
                        'fClefChange': 'F',
                        'unpitchedPercussionClef1': 'percussion',
                        'gClef': 'G',
                        'gClefChange': 'G'
                        }

    CLEF_TO_LINE_MAP = {'cClefAlto': '3',
                        'cClefAltoChange': '3',
                        'cClefTenor': '4',
                        'cClefTenorChange': '4',
                        'clef15': '2',
                        'clef8': '2',
                        'fClef': '4',
                        'fClefChange': '4',
                        'unpitchedPercussionClef1': '',
                        'gClef': '2',
                        'gClefChange': '2'
                        }

    def create_independent_symbol(self):
        clef = ET.Element('clef')
        sign = ET.Element('sign')
        sign.text = self.CLEF_TO_SIGN_MAP[self.typ]
        clef.append(sign)
        line = self.CLEF_TO_LINE_MAP[self.typ]
        if line != '':
            line_xml = ET.Element('line')
            line_xml.text = line
            clef.append(line)
        return clef
