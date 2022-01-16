import string
from dataclasses import dataclass
#
# PNG_PATH = r'/content/drive/MyDrive/Nuty/deep_scores_dense/deep_scores_dense/images_png/'
# XML_PATH = r'/content/drive/MyDrive/Nuty/deep_scores_dense/deep_scores_dense/xml_annotations/'
# CONVERTED_PATH = r'/content/drive/MyDrive/Nuty/deep_scores_dense/deep_scores_dense/converted/'
# CLASSES_PATH = r'/content/drive/MyDrive/Nuty/deep_scores_dense/deep_scores_dense/meta_info/'


PNG_PATH = r'C:\Users\user\PycharmProjects\nuty5\deep_scores_dense\images_png'
XML_PATH = r'C:\Users\user\PycharmProjects\nuty5\deep_scores_dense\xml_annotations'
CONVERTED_PATH = r'C:\Users\user\PycharmProjects\nuty5\deep_scores_dense\converted'
CLASSES_PATH = r'C:\Users\user\PycharmProjects\nuty5\deep_scores_dense\meta_info'
X = 256
Y = 256
#CLASSES = ['noteheadBlack']
CLASSES = None
# CLASSES = ['accidentalFlat','accidentalFlatSmall','accidentalNatural','accidentalNaturalSmall','accidentalSharp',
#            'accidentalSharpSmall','augmentationDot','flag128thUp','flag16thDown','flag16thUp','flag32ndDown','flag32ndUp',
#            'flag64thDown','flag64thUp','flag8thDown','flag8thDownSmall','flag8thUp','flag8thUpSmall','keyFlat','keyNatural','keySharp',
#            'noteheadBlack','noteheadBlackSmall','noteheadDoubleWhole','noteheadDoubleWholeSmall','noteheadHalf','noteheadHalfSmall',
#            'noteheadWhole','noteheadWholeSmall','rest128th','rest16th','rest32nd','rest64th','rest8th','restDoubleWhole','restHBar',
#            'restHalf','restLonga','restMaxima','restQuarter','restWhole','tuplet3','tuplet6']

@dataclass
class Params:
    X: int
    Y: int
    RECORDS_TO_SAVE: int
    BATCH_SIZE: int
    CLASSES: list
    PNG_PATH: string
    XML_PATH: string
    CONVERTED_PATH: string
    CLASSES_PATH: string
