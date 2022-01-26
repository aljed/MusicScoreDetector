from dataclasses import dataclass

from StaffPositionRetriever import Staff
from Converter import ElementsMap
import xml.etree.cElementTree as ET
from independent.Note import Note, get_pitch_xml


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
                pitch_xml = get_pitch_xml((note.position.xmax + note.position.xmin) / 2,
                                          (note.position.ymax + note.position.ymin) / 2, staff)
                duration_element = ET.Element("duration")
                duration_element.text = "1"
                if len(chord) > 1 and note != chord[0]:
                    note_xml.append(ET.Element("chord"))
                note_xml.append(pitch_xml)
                note_xml.append(duration_element)
                root.append(note_xml)
        return root
