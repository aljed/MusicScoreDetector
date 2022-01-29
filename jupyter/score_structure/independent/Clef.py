import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import IndependentSymbol


class Clef(IndependentSymbol):

    CLEFS = ['clefG', 'clefCAlto', 'clefCTenor', 'clefF', 'clefUnpitchedPercussion', 'clef8', 'clef15']

    CLEF_TO_SIGN_MAP = {'clefCAlto': 'C',
                        'clefCTenor': 'C',
                        'clef15': 'G',
                        'clef8': 'G',
                        'clefF': 'F',
                        'clefUnpitchedPercussion': 'percussion',
                        'clefG': 'G'
                        }

    CLEF_TO_LINE_MAP = {'cClefAlto': '3',
                        'cClefTenor': '4',
                        'clef15': '2',
                        'clef8': '2',
                        'clefF': '4',
                        'clefUnpitchedPercussion': '',
                        'clefG': '2',
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
