from dataclasses import dataclass
import parameters as p
import data as d
import os
import classes as c
counter = 0


@dataclass
class Element:
    position: d.BoundingBox


# @dataclass
# class IndependentSymbol(Element):
#
#
# @dataclass
# class Modifier(Element):



@dataclass
class Accidental(Element):
    typ: str
    keyAccidental: bool

@dataclass
class Accent(Element):
    typ: str
    keyAccidental: bool