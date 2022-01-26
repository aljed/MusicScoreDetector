import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import SymbolGroup


class KeySignature(SymbolGroup):

    KEY_SIGNATURES = ['keyFlat', 'keyNatural', 'keySharp']

    KEY_SIGNATURES_MAP = {'keyFlat': 'flat',
                          'keyNatural': 'natural',
                          'keySharp': 'sharp'
                          }

    def create_independent_symbol(self):
        key = ET.Element('key')
        naturals = [e for e in self.elements if e.typ == 'keyNatural']
        cancel = ET.Element('cancel')
        cancel.text = len(naturals)
        sharps = [e for e in self.elements if e.typ == 'keySharp']
        flats = [e for e in self.elements if e.typ == 'keyFlat']

        if sharps and flats:
            print("Warning: there are both flats and sharps in one group")

        fifths = ET.Element('fifths')
        fifths.text = len(sharps) - len(flats)
        key.append(cancel)
        key.append(fifths)
        return key
