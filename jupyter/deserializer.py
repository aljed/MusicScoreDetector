from dataclasses import dataclass

from StaffPositionRetriever import Staff
from Converter import ElementsMap
import xml.etree.cElementTree as ET


@dataclass
class Group:
    staff: Staff
    measures: list

    def deserialize(self):
        return [m.deserialize(self.staff) for m in self.measures]


@dataclass
class Measure:
    xmin: int
    xmax: int
    elements: ElementsMap

    def deserialize(self, staff):
        black_notes = self.elements.elements["noteheadBlack"]
        black_notes.sort(key=lambda e: e.position.xmin)
        chords = []
        i = 0
        while i < len(black_notes):
            chord = [black_notes[i]]
            i += 1
            # todo parameter
            while i < len(black_notes) and (black_notes[i].position.xmin - black_notes[i - 1].position.xmin) < 30:
                chord.append(black_notes[i])
                i += 1
            chords.append(chord)
        root = ET.Element("measure", width=str(self.xmax - self.xmin))
        for chord in chords:
            for note in chord:
                note_xml = ET.Element("note", {"default-x": str(note.position.xmin)})
                pitch_xml = get_pitch_xml((note.position.xmax + note.position.xmin) / 2, staff)
                duration_element = ET.Element("duration")
                duration_element.text = "1"
                if len(chord) > 1:
                    note_xml.append(ET.Element("chord"))
                note_xml.append(pitch_xml)
                note_xml.append(duration_element)
                root.append(note_xml)


def get_pitch_xml(x, staff):
    pitch_xml = ET.Element("pitch")
    octave_xml = ET.Element("octave")
    step_xml = ET.Element("step")
    d = (staff.line_positions[4] - staff.line_positions[0]) / 4
    y = 38 - 2 * ((staff.line_positions[0] - x) / d)
    assert 0 <= y <= 70
    step = y % 7
    assert 0 <= step <= 6
    steps_map = {0: "C", 1: "D", 2: "E", 3: "F", 4: "G", 5: "A", 6: "B"}
    step_xml.text = steps_map[step]
    octave = (y - step) / 7
    octave.text = octave
    pitch_xml.append(octave_xml)
    pitch_xml.append(step_xml)
    return pitch_xml
