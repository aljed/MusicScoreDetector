from dataclasses import dataclass

from StaffPositionRetriever import Staff
from Converter import ElementsMap
import xml.etree.cElementTree as ET
from independent.Note import Note, get_pitch_xml
from jupyter.score_structure.ScoreFactory import transform_measure
from jupyter.score_structure.ScoreStructure import IndependentSymbol, Modifier
from jupyter.score_structure.independent.Rest import Rest
from jupyter.score_structure.modifiers.Flag import Flag, transform_by_beans_number, Beam


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
        modifiers, independent = transform_measure(self.elements)
        main = [i for i in independent if isinstance(i, Note) or isinstance(i, Rest) or isinstance(i, Flag)]
        beams = [i for i in modifiers if isinstance(i, Beam)]

        moments = []
        i = 0
        while i < len(main):
            moment = [main[i]]
            i += 1
            while i < len(main) and (main[i].position.xmin - main[i - 1].position.xmin) < 30:
                moment.append(main[i])
                i += 1
            moments.append(moment)
        root = ET.Element("measure", width=str(self.xmax - self.xmin))
        for moment in moments:

            moment.sort(key=lambda a: a.position.ymin)
            beams_over = [b for b in beams if b.position.xmin < moment[0].position.xmin + 30 < b.position.xmax + 60]
            notes = [i for i in moment if isinstance(i, Note)]
            notes_xml = {n: n.create_independent_symbol(staff, False) for n in notes}
            rests_xml = [i.create_independent_symbol() for i in moment if isinstance(i, Rest)]
            modifiers = [i for i in moment if isinstance(i, Modifier)]

            for modifier in modifiers:
                yavg = (modifier.position.ymax - modifier.position.ymin) / 2
                midpoint_lengths = [(note, abs(yavg - (note.position.ymax - note.position.ymin)) / 2) for note in notes]
                midpoint_lengths.sort(key=lambda a,b: b)
                closest_note = midpoint_lengths[0][0]
                notes_xml[closest_note] = modifier.transform_independent_symbol(notes_xml[closest_note])

            if len(beams_over) > 0:
                transform_by_beans_number(len(beams_over), notes[0])

            ind = [notes_xml[key] for key in notes_xml] + rests_xml
            ind.sort(key=lambda a: a.position.ymin)
            for i in ind:
                root.append(i)

        return root
