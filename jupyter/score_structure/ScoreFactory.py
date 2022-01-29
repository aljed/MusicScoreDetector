from ScoreStructure import BoundingBox, Modifier, IndependentSymbol
from jupyter.score_structure.independent.Note import Note
from jupyter.score_structure.independent.Rest import Rest
from jupyter.score_structure.modifiers.Flag import Flag
from jupyter.score_structure.modifiers.Accent import Accent
from jupyter.score_structure.modifiers.Accidental import Accidental
from jupyter.score_structure.modifiers.Dynamic import Dynamic
from jupyter.score_structure.modifiers.Notation import NoteModifier
from jupyter.score_structure.modifiers.Number import Number
from jupyter.score_structure.modifiers.Ornament import Ornament
from jupyter.score_structure.Converter import ElementsMap


def create(typ, bb: BoundingBox):
    if typ in Flag.FLAGS:
        return Flag(typ, bb)
    elif typ in Note.NOTES:
        return Note(typ, bb)
    elif typ in Rest.RESTS:
        return Rest(typ, bb)
    elif typ in Number.NUMBERS:
        return Number(typ, bb)
    elif typ in Accent.ACCENTS:
        return Accent(typ, bb)
    elif typ in Accidental.ACCIDENTALS:
        return Accidental(typ, bb)
    elif typ in Dynamic.DYNAMICS:
        return Dynamic(typ, bb)
    elif typ in Ornament.ORNAMENTS:
        return Ornament(typ, bb)
    elif typ in NoteModifier.NOTATIONS:
        return NoteModifier(typ, bb)
    return None


def transform_measure(elements_map: ElementsMap):
    elements = []

    def sort_func(_, pos):
        x = (pos.xmax - pos.xmin)/2
        y = (pos.ymax - pos.ymin)/2
        return x, y

    for typ, group in elements_map.elements:
        for e in group:
            elements.append((typ, e.position))

    elements = sorted(elements, key=sort_func)
    elements = [create(typ, bb) for typ, bb in elements]
    modifiers = [e for e in elements if isinstance(e, Modifier)]
    independent = [e for e in elements if isinstance(e, IndependentSymbol)]

    return modifiers, independent
