from dataclasses import dataclass
import xml.etree.cElementTree as ET
from typing import List

counter = 0


@dataclass
class BoundingBox:
    xmin: float
    xmax: float
    ymin: float
    ymax: float


class ScoreElement:
    position: BoundingBox
    typ: str

    def __init__(self, position, bb):
        self.position = position
        self.bb = bb


class IndependentSymbol(ScoreElement):
    pass


class Modifier(ScoreElement):

    def transform_independent_symbol(self, parent: ET.Element):
        pass


class SymbolGroup:

    def __init__(self, elements: List[ScoreElement]):
        self.elements = elements

    def create_independent_symbol(self):
        pass
