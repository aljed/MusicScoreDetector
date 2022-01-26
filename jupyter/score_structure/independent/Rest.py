import math
import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import IndependentSymbol
from jupyter.score_structure.StaffPositionRetriever import Staff


class Rest(IndependentSymbol):

    RESTS = ['rest128th', 'rest16th', 'rest32nd', 'rest64th', 'rest8th', 'restDoubleWhole', 'restHalf', 'restHBar',
             'restLonga', 'restMaxima', 'restQuarter', 'restWhole']

    RESTS_TO_TYPE_MAP = {'rest128th': '128th',
                        'rest16th': '16th',
                        'rest32nd': '32nd',
                        'rest64th': '64th',
                        'rest8th': '8th',
                        'restDoubleWhole': 'breve',
                        'restHalf': 'half',
                        'restHBar': 'maxima',  # todo
                        'restLonga': 'long',
                        'restMaxima': 'maxima',
                        'restQuarter': 'quarter',
                        'restWhole': 'whole'
                        }

    def create_independent_symbol(self):
        note_xml = ET.Element('note')
        rest = ET.Element('rest')
        note_xml.append(rest)
        typ = ET.Element('type')
        typ.text = self.RESTS_TO_TYPE_MAP[self.typ]
        note_xml.append(typ)
        return note_xml
