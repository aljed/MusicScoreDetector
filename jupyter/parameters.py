import string
from dataclasses import dataclass

PNG_PATH = r'C:\Users\user\PycharmProjects\nuty5\deep_scores_dense\images_png'
XML_PATH = r'C:\Users\user\PycharmProjects\nuty5\deep_scores_dense\xml_annotations'
CONVERTED_PATH = r'C:\Users\user\PycharmProjects\nuty5\deep_scores_dense\converted'
CLASSES_PATH = r'C:\Users\user\PycharmProjects\nuty5\deep_scores_dense\meta_info'
X = 100
Y = 100
GX = 1
GY = 2
PARTS_NUMBER = 50
CLASSES = ['noteheadBlack']
BATCH_SIZE = 1


@dataclass
class Params:
    X: int
    Y: int
    GX: int
    GY: int
    PARTS_NUMBER: int
    BATCH_SIZE: int
    CLASSES: list
    PNG_PATH: string
    XML_PATH: string
    CONVERTED_PATH: string
    CLASSES_PATH: string