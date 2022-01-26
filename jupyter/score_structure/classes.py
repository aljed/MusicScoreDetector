ACCIDENTALS = ['accidentalDoubleFlat', 'accidentalDoubleSharp', 'accidentalFlat', 'accidentalFlatSmall',
               'accidentalNatural', 'accidentalNaturalSmall', 'accidentalSharp', 'accidentalSharpSmall',
               'keyFlat', 'keyNatural', 'keySharp']

ACCENTS = ['articAccentAbove', 'articAccentBelow', 'articMarcatoAbove', 'articMarcatoBelow', 'articStaccatissimoAbove',
           'articStaccatissimoBelow', 'articStaccatoAbove', 'articStaccatoBelow', 'articTenutoAbove', 'articTenutoBelow']

DYNAMICS = ['dynamicFF', 'dynamicFFF', 'dynamicFFFF', 'dynamicFFFFF', 'dynamicForte', 'dynamicFortePiano',
             'dynamicMezzo', 'dynamicMF', 'dynamicMP', 'dynamicPiano', 'dynamicPP', 'dynamicPPP', 'dynamicPPPP', 'dynamicPPPPP',
            'dynamicRinforzando2', 'dynamicSforzando1', 'dynamicSforzato']

MISC_SYMBOLS = ['brace', 'caesura', 'keyboardPedalPed', 'keyboardPedalUp', 'segno', 'stringsDownBow', 'stringsUpBow',
                        'summary',  'coda', 'repeatDot']

MISC_NOTE_MODIFIERS = ['ornamentMordent', 'ornamentTrill', 'ornamentTurn', 'ornamentTurnInverted', 'augmentationDot',
                       'fermataAbove', 'fermataBelow',  'arpeggiato']

CLEFS = ['cClefAlto', 'cClefAltoChange', 'cClefTenor', 'cClefTenorChange', 'clef15', 'clef8', 'fClef', 'fClefChange',
         'unpitchedPercussionClef1', 'gClef', 'gClefChange']

NOTES = [ 'noteheadBlack', 'noteheadBlackSmall', 'noteheadDoubleWhole', 'noteheadDoubleWholeSmall', 'noteheadHalf',
          'noteheadHalfSmall', 'noteheadWhole', 'noteheadWholeSmall']

GRACES = ['graceNoteAcciaccaturaStemDown',
          'graceNoteAcciaccaturaStemUp', 'graceNoteAppoggiaturaStemDown', 'graceNoteAppoggiaturaStemUp']

RESTS = ['rest128th', 'rest16th', 'rest32nd', 'rest64th', 'rest8th', 'restDoubleWhole', 'restHalf', 'restHBar',
         'restLonga', 'restMaxima', 'restQuarter', 'restWhole']

NUMBERS = ['fingering0', 'fingering1', 'fingering2', 'fingering3', 'fingering4', 'fingering5', 'tuplet3', 'tuplet6']

FLAGS = ['flag128thDown', 'flag128thUp', 'flag16thDown', 'flag16thUp', 'flag32ndDown', 'flag32ndUp', 'flag64thDown',
         'flag64thUp', 'flag8thDown', 'flag8thDownSmall', 'flag8thUp', 'flag8thUpSmall']

TIME_SIGNATURES = ['timeSig0', 'timeSig1', 'timeSig12', 'timeSig16', 'timeSig2', 'timeSig3', 'timeSig4', 'timeSig5',
                    'timeSig6', 'timeSig7', 'timeSig8', 'timeSig9', 'timeSigCommon', 'timeSigCutCommon']

ALL = ['accidentalDoubleFlat', 'accidentalDoubleSharp', 'accidentalFlat', 'accidentalFlatSmall', 'accidentalNatural', 'accidentalNaturalSmall', 'accidentalSharp', 'accidentalSharpSmall', 'keyFlat', 'keyNatural', 'keySharp',
 'articAccentAbove', 'articAccentBelow', 'articMarcatoAbove', 'articMarcatoBelow', 'articStaccatissimoAbove', 'articStaccatissimoBelow', 'articStaccatoAbove', 'articStaccatoBelow', 'articTenutoAbove', 'articTenutoBelow',
 'dynamicFF', 'dynamicFFF', 'dynamicFFFF', 'dynamicFFFFF', 'dynamicForte', 'dynamicFortePiano', 'dynamicMezzo', 'dynamicMF', 'dynamicMP', 'dynamicPiano', 'dynamicPP', 'dynamicPPP', 'dynamicPPPP', 'dynamicPPPPP',
 'brace', 'caesura', 'dynamicRinforzando2', 'dynamicSforzando1', 'dynamicSforzato', 'keyboardPedalPed', 'keyboardPedalUp', 'segno', 'stringsDownBow', 'stringsUpBow', 'summary',  'coda', 'repeatDot',
 'ornamentMordent', 'ornamentTrill', 'ornamentTurn', 'ornamentTurnInverted', 'augmentationDot', 'fermataAbove', 'fermataBelow',  'arpeggiato',
 'cClefAlto', 'cClefAltoChange', 'cClefTenor', 'cClefTenorChange', 'clef15', 'clef8', 'fClef', 'fClefChange', 'unpitchedPercussionClef1', 'gClef', 'gClefChange',
 'noteheadBlack', 'noteheadBlackSmall', 'noteheadDoubleWhole', 'noteheadDoubleWholeSmall', 'noteheadHalf', 'noteheadHalfSmall', 'noteheadWhole', 'noteheadWholeSmall', 'graceNoteAcciaccaturaStemDown', 'graceNoteAcciaccaturaStemUp', 'graceNoteAppoggiaturaStemDown', 'graceNoteAppoggiaturaStemUp',
 'rest128th', 'rest16th', 'rest32nd', 'rest64th', 'rest8th', 'restDoubleWhole', 'restHalf', 'restHBar', 'restLonga', 'restMaxima', 'restQuarter', 'restWhole',
 'fingering0', 'fingering1', 'fingering2', 'fingering3', 'fingering4', 'fingering5', 'tuplet3', 'tuplet6',
 'flag128thDown', 'flag128thUp', 'flag16thDown', 'flag16thUp', 'flag32ndDown', 'flag32ndUp', 'flag64thDown',
 'flag64thUp', 'flag8thDown', 'flag8thDownSmall', 'flag8thUp', 'flag8thUpSmall',
 'timeSig0', 'timeSig1', 'timeSig12', 'timeSig16', 'timeSig2', 'timeSig3', 'timeSig4', 'timeSig5', 'timeSig6', 'timeSig7', 'timeSig8', 'timeSig9', 'timeSigCommon', 'timeSigCutCommon']

MODIFIER_TYPES = [ACCIDENTALS, ACCENTS, DYNAMICS, MISC_NOTE_MODIFIERS, NUMBERS, FLAGS ]
INDEPENDENT_TYPES = [MISC_SYMBOLS, CLEFS, NOTES, RESTS, TIME_SIGNATURES, GRACES]



MISC_SYMBOLS = ['brace', 'caesura', 'keyboardPedalPed', 'keyboardPedalUp', 'segno', 'stringsDownBow', 'stringsUpBow',
                        'summary',  'coda', 'repeatDot']

MISC_NOTE_MODIFIERS = ['ornamentMordent', 'ornamentTrill', 'ornamentTurn', 'ornamentTurnInverted', 'augmentationDot',
                       'fermataAbove', 'fermataBelow',  'arpeggiato']


OFTEN = []
OFTEN += ACCIDENTALS
OFTEN += [ 'articStaccatoAbove', 'articStaccatoBelow']
OFTEN += ['dynamicFF', 'dynamicFFF', 'dynamicFFFF', 'dynamicFFFFF', 'dynamicForte', 'dynamicFortePiano',
             'dynamicMezzo', 'dynamicMF', 'dynamicMP', 'dynamicPiano', 'dynamicPP', 'dynamicPPP', 'dynamicPPPP', 'dynamicPPPPP']
OFTEN += ['keyboardPedalPed', 'keyboardPedalUp', 'repeatDot']
OFTEN += ['augmentationDot']
OFTEN += ['gClef', 'gClefChange', 'fClef', 'fClefChange', 'clef15', 'clef8']
OFTEN += [ 'noteheadBlack', 'noteheadBlackSmall', 'noteheadDoubleWhole', 'noteheadDoubleWholeSmall', 'noteheadHalf',
          'noteheadHalfSmall', 'noteheadWhole', 'noteheadWholeSmall', 'graceNoteAcciaccaturaStemDown',
          'graceNoteAcciaccaturaStemUp', 'graceNoteAppoggiaturaStemDown', 'graceNoteAppoggiaturaStemUp']
OFTEN += ['rest128th', 'rest16th', 'rest32nd', 'rest64th', 'rest8th', 'restDoubleWhole', 'restHalf', 'restHBar',
         'restLonga', 'restMaxima', 'restQuarter', 'restWhole']
OFTEN += ['flag128thDown', 'flag128thUp', 'flag16thDown', 'flag16thUp', 'flag32ndDown', 'flag32ndUp', 'flag64thDown',
         'flag64thUp', 'flag8thDown', 'flag8thDownSmall', 'flag8thUp', 'flag8thUpSmall']

RARE = ['articAccentAbove', 'articAccentBelow', 'articMarcatoAbove', 'articMarcatoBelow', 'articStaccatissimoAbove',
           'articStaccatissimoBelow', 'articTenutoAbove', 'articTenutoBelow']
RARE += ['dynamicRinforzando2', 'dynamicSforzando1', 'dynamicSforzato']
RARE += ['brace', 'caesura', 'segno', 'stringsDownBow', 'stringsUpBow', 'summary',  'coda']
RARE += ['ornamentMordent', 'ornamentTrill', 'ornamentTurn', 'ornamentTurnInverted', 'augmentationDot',
                       'fermataAbove', 'fermataBelow',  'arpeggiato']
RARE += ['cClefAlto', 'cClefAltoChange', 'cClefTenor', 'cClefTenorChange', 'unpitchedPercussionClef1']
RARE += ['fingering0', 'fingering1', 'fingering2', 'fingering3', 'fingering4', 'fingering5', 'tuplet3', 'tuplet6']
RARE += ['timeSig0', 'timeSig1', 'timeSig12', 'timeSig16', 'timeSig2', 'timeSig3', 'timeSig4', 'timeSig5',
                    'timeSig6', 'timeSig7', 'timeSig8', 'timeSig9', 'timeSigCommon', 'timeSigCutCommon']



CLEFS = ['cClefAlto', 'cClefAltoChange', 'cClefTenor', 'cClefTenorChange', 'clef15', 'clef8', 'fClef', 'fClefChange',
         'unpitchedPercussionClef1', 'gClef', 'gClefChange']

OFTEN = ['brace', 'keyboardPedalPed', 'keyboardPedalUp',  'repeatDot', 'gClef', 'gClefChange', 'clef15', 'clef8', 'fClef', 'fClefChange']
RARE = ['caesura', 'segno', 'stringsDownBow', 'stringsUpBow', 'summary',  'coda', 'ornamentMordent', 'ornamentTrill',
        'ornamentTurn', 'ornamentTurnInverted', 'augmentationDot', 'fermataAbove', 'fermataBelow',  'arpeggiato',
        'cClefAlto', 'cClefAltoChange', 'cClefTenor', 'cClefTenorChange', 'unpitchedPercussionClef1']

T = RARE
print(T)

aa = {}
for k, v in enumerate(T):
    aa[k + 1] = v
print(aa)