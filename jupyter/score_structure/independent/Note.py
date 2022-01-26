import math
import xml.etree.cElementTree as ET

from jupyter.score_structure.ScoreStructure import IndependentSymbol
from jupyter.score_structure.StaffPositionRetriever import Staff


class Note(IndependentSymbol):

    NOTES = ['noteheadBlack', 'noteheadBlackSmall', 'noteheadDoubleWhole', 'noteheadDoubleWholeSmall', 'noteheadHalf',
             'noteheadHalfSmall', 'noteheadWhole', 'noteheadWholeSmall']

    NOTE_TO_TYPE_MAP = {'noteheadBlack': 'quarter',
                        'noteheadBlackSmall': 'quarter',
                        'noteheadDoubleWhole': 'breve',
                        'noteheadDoubleWholeSmall': 'breve',
                        'noteheadHalf': 'half',
                        'noteheadHalfSmall': 'half',
                        'noteheadWhole': 'whole',
                        'noteheadWholeSmall': 'whole'
                        }

    def create_independent_symbol(self, staff: Staff, is_chord):
        note_xml = ET.Element("note")
        pitch_xml = get_pitch_xml((self.position.xmax + self.position.xmin) / 2,
                                  (self.position.ymax + self.position.ymin) / 2, staff)
        if is_chord:
            note_xml.append(ET.Element("chord"))
        note_xml.append(pitch_xml)

        typ = ET.Element('type')
        typ.text = self.NOTE_TO_TYPE_MAP[self.typ]
        note_xml.append(typ)

        return note_xml


def get_pitch_xml(x, y, staff: Staff):
    def y_line(x_pos, line):
        return (line.r - x_pos * math.cos(math.radians(line.theta))) / math.sin(math.radians(line.theta))

    pitch_xml = ET.Element("pitch")
    octave_xml = ET.Element("octave")
    step_xml = ET.Element("step")
    d = round((staff.lines[4].r - staff.lines[0].r) / 4)
    y_normalized = round(38 + 2 * (y_line(x, staff.lines[0]) - y) / d)
    assert 0 <= y_normalized <= 70
    step = math.floor(y_normalized % 7)
    assert 0 <= step <= 6
    steps_map = {0: "C", 1: "D", 2: "E", 3: "F", 4: "G", 5: "A", 6: "B"}
    step_xml.text = steps_map[step]
    octave = int((y_normalized - step) / 7)
    octave_xml.text = str(octave)
    pitch_xml.append(step_xml)
    pitch_xml.append(octave_xml)
    return pitch_xml
