from score_structure import data as d
import importlib


importlib.reload(d)
from score_structure.parameters import Params
import os

params = Params(X=256,
                Y=256,
                RECORDS_TO_SAVE=10000,
                CLASSES=['ottavaBracket', 'dynamicCrescendoHairpin', 'dynamicDiminuendoHairpin', 'slur', 'tie',
                    'tupletBracket', 'brace', 'beam'],
                PNG_PATH = r'E:\Downloads\ds2_dense\images'
                )

M0 = ['staff']
M1 = ['ottavaBracket', 'dynamicCrescendoHairpin', 'dynamicDiminuendoHairpin', 'slur',  'tie', 'tupletBracket','brace','beam']
M2 = ['repeatDot','articAccentAbove', 'articAccentBelow', 'articStaccatoAbove', 'articStaccatoBelow', 'articTenutoAbove', 'articTenutoBelow', 'articStaccatissimoAbove', 'articStaccatissimoBelow', 'articMarcatoAbove', 'articMarcatoBelow','augmentationDot']
M3 = ['accidentalFlat', 'accidentalFlatSmall', 'accidentalNatural', 'accidentalNaturalSmall', 'accidentalSharp', 'accidentalSharpSmall', 'accidentalDoubleSharp', 'accidentalDoubleFlat', 'keyFlat', 'keyNatural', 'keySharp','keyboardPedalPed', 'keyboardPedalUp','fermataAbove', 'fermataBelow'  'ornamentTrill', 'ornamentTurn', 'ornamentTurnInverted', 'ornamentMordent',   'stringsDownBow', 'stringsUpBow','tremolo1', 'tremolo2', 'tremolo3', 'tremolo4', 'tremolo5',  'segno', 'coda', 'clefG', 'clefCAlto', 'clefCTenor', 'clefF', 'clefUnpitchedPercussion', 'clef8', 'clef15', 'arpeggiato','restDoubleWhole', 'restWhole', 'restHalf', 'restQuarter', 'rest8th', 'rest16th', 'rest32nd', 'rest64th', 'rest128th', 'restHNr','restHBar','ledgerLine','stem']
M4 = ['tuplet1', 'tuplet2', 'tuplet4', 'tuplet5', 'tuplet7', 'tuplet8', 'tuplet9', 'tuplet3', 'tuplet6', 'fingering0', 'fingering1', 'fingering2', 'fingering3', 'fingering4', 'fingering5', 'caesura',  'dynamicP', 'dynamicM', 'dynamicF', 'dynamicS', 'dynamicZ', 'dynamicR', 'timeSig0', 'timeSig1', 'timeSig2', 'timeSig3', 'timeSig4', 'timeSig5', 'timeSig6', 'timeSig7', 'timeSig8', 'timeSig9', 'timeSigCommon', 'timeSigCutCommon']
M5 = ['noteheadBlackOnLine', 'noteheadBlackOnLineSmall', 'noteheadBlackInSpace', 'noteheadBlackInSpaceSmall', 'noteheadHalfOnLine', 'noteheadHalfOnLineSmall', 'noteheadHalfInSpace', 'noteheadHalfInSpaceSmall', 'noteheadWholeOnLine', 'noteheadWholeOnLineSmall', 'noteheadWholeInSpace', 'noteheadWholeInSpaceSmall', 'noteheadDoubleWholeOnLine', 'noteheadDoubleWholeOnLineSmall', 'noteheadDoubleWholeInSpace', 'noteheadDoubleWholeInSpaceSmall', 'graceNoteAcciaccaturaStemUp', 'graceNoteAppoggiaturaStemUp', 'graceNoteAcciaccaturaStemDown', 'graceNoteAppoggiaturaStemDown']
M6 = ['flag8thUp', 'flag8thUpSmall', 'flag16thUp', 'flag32ndUp', 'flag64thUp', 'flag128thUp', 'flag8thDown', 'flag8thDownSmall', 'flag16thDown', 'flag32ndDown', 'flag64thDown', 'flag128thDown']


counter = 0
names = {}

for index in M6:
    names[counter+1] = index
    counter += 1

print(len(names))
print( names)