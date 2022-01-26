import string
from dataclasses import dataclass
#
# PNG_PATH = r'/content/drive/MyDrive/Nuty/deep_scores_dense/deep_scores_dense/images_png/'
# XML_PATH = r'/content/drive/MyDrive/Nuty/deep_scores_dense/deep_scores_dense/xml_annotations/'
# CONVERTED_PATH = r'/content/drive/MyDrive/Nuty/deep_scores_dense/deep_scores_dense/converted/'
# CLASSES_PATH = r'/content/drive/MyDrive/Nuty/deep_scores_dense/deep_scores_dense/meta_info/'


PNG_PATH = r'/images_png'
XML_PATH = r'/xml_annotations'
CONVERTED_PATH = r'C:\Users\user\PycharmProjects\nuty5\deep_scores_dense\converted'
CLASSES_PATH = r'/meta_info'
X = 256
Y = 256


#CLASSES = ['noteheadBlack']

# ofter
# CLASSES = ['dynamicFF', 'dynamicFFF', 'dynamicFFFF', 'dynamicFFFFF', 'dynamicForte', 'dynamicFortePiano', 'dynamicMezzo',
#       'dynamicMF', 'dynamicMP', 'dynamicPiano', 'dynamicPP', 'dynamicPPP', 'dynamicPPPP', 'dynamicPPPPP',
#       'dynamicRinforzando2', 'dynamicSforzando1', 'dynamicSforzato']
# rare
#CLASSES = ['articAccentAbove', 'articAccentBelow', 'articMarcatoAbove', 'articMarcatoBelow', 'articStaccatissimoAbove', 'articStaccatissimoBelow', 'articTenutoAbove', 'articTenutoBelow', 'dynamicRinforzando2', 'dynamicSforzando1', 'dynamicSforzato', 'brace', 'caesura', 'segno', 'stringsDownBow', 'stringsUpBow', 'summary', 'coda', 'ornamentMordent', 'ornamentTrill', 'ornamentTurn', 'ornamentTurnInverted', 'augmentationDot', 'fermataAbove', 'fermataBelow', 'arpeggiato', 'cClefAlto', 'cClefAltoChange', 'cClefTenor', 'cClefTenorChange', 'unpitchedPercussionClef1', 'fingering0', 'fingering1', 'fingering2', 'fingering3', 'fingering4', 'fingering5', 'tuplet3', 'tuplet6', 'timeSig0', 'timeSig1', 'timeSig12', 'timeSig16', 'timeSig2', 'timeSig3', 'timeSig4', 'timeSig5', 'timeSig6', 'timeSig7', 'timeSig8', 'timeSig9', 'timeSigCommon', 'timeSigCutCommon']
# 53
#{1: articAccentAbove, 2: articAccentBelow, 3: articMarcatoAbove, 4: articMarcatoBelow, 5: articStaccatissimoAbove, 6: articStaccatissimoBelow, 7: articTenutoAbove, 8: articTenutoBelow, 9: dynamicRinforzando2, 10: dynamicSforzando1, 11: dynamicSforzato, 12: brace, 13: caesura, 14: segno, 15: stringsDownBow, 16: stringsUpBow, 17: summary, 18: coda, 19: ornamentMordent, 20: ornamentTrill, 21: ornamentTurn, 22: ornamentTurnInverted, 23: augmentationDot, 24: fermataAbove, 25: fermataBelow, 26: arpeggiato, 27: cClefAlto, 28: cClefAltoChange, 29: cClefTenor, 30: cClefTenorChange, 31: unpitchedPercussionClef1, 32: fingering0, 33: fingering1, 34: fingering2, 35: fingering3, 36: fingering4, 37: fingering5, 38: tuplet3, 39: tuplet6, 40: timeSig0, 41: timeSig1, 42: timeSig12, 43: timeSig16, 44: timeSig2, 45: timeSig3, 46: timeSig4, 47: timeSig5, 48: timeSig6, 49: timeSig7, 50: timeSig8, 51: timeSig9, 52: timeSigCommon, 53: timeSigCutCommon}

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
