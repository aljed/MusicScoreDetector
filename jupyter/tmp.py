import automl.efficientdet.model_inspect as inspection
from jupyter import Converter
from jupyter.parameters import Params
import data as d
import os

# classes = (d.retrieve_class_names())
# aa = {}
# for k in classes.keys():
#     v = classes[k]
#     aa[int(v) + 1] = k
# print(aa)


# predictor = inspection.get_prediction_function('./models/efficientdet-d1-finetune', './logs', 'efficientdet-d1', './configs/default.yaml')
#
#
# params = Params(X=128,
#                 Y=128,
#                 RECORDS_TO_SAVE=8192,
#                 BATCH_SIZE=32,
#                 CLASSES=['noteheadBlack'],
#                 PNG_PATH = r'/content/drive/MyDrive/Nuty/deep_scores_dense/deep_scores_dense/images_png/',
#                 XML_PATH = r'/content/drive/MyDrive/Nuty/deep_scores_dense/deep_scores_dense/xml_annotations/',
#                 CONVERTED_PATH = r'/content/drive/MyDrive/Nuty/deep_scores_dense/deep_scores_dense/converted/',
#                 CLASSES_PATH = r'/content/drive/MyDrive/Nuty/deep_scores_dense/deep_scores_dense/meta_info/')
#
# converter = Converter.Converter('', 80, 80, predictor, params, 0.9, 0.3)
# print(converter.convert('../deep_scores_dense/images_png/test.png'))
#
#
#
# from keras import backend as K
# K.clear_session()


params = Params(X=256,
                Y=256,
                RECORDS_TO_SAVE=8192,
                BATCH_SIZE=32,
                CLASSES = ['accidentalFlat','accidentalFlatSmall','accidentalNatural','accidentalNaturalSmall','accidentalSharp',
                    'accidentalSharpSmall','augmentationDot','flag128thUp','flag16thDown','flag16thUp','flag32ndDown','flag32ndUp',
                    'flag64thDown','flag64thUp','flag8thDown','flag8thDownSmall','flag8thUp','flag8thUpSmall','keyFlat','keyNatural','keySharp',
                    'noteheadBlackSmall','noteheadDoubleWhole','noteheadDoubleWholeSmall','noteheadHalf','noteheadHalfSmall',
                    'noteheadWhole','noteheadWholeSmall','rest128th','rest16th','rest32nd','rest64th','rest8th','restDoubleWhole','restHBar',
                    'restHalf','restLonga','restMaxima','restQuarter','restWhole','tuplet3','tuplet6'],
                PNG_PATH=r'C:\Users\user\PycharmProjects\nuty5\deep_scores_dense\images_png',
                XML_PATH = r'C:\Users\user\PycharmProjects\nuty5\deep_scores_dense\xml_annotations',
                CONVERTED_PATH = r'C:\Users\user\PycharmProjects\nuty5\deep_scores_dense\converted',
                CLASSES_PATH = r'C:\Users\user\PycharmProjects\nuty5\deep_scores_dense\meta_info')

files = os.listdir(params.PNG_PATH)
classes = d.retrieve_class_names()
generator = d.TFRecordGenerator(d.retrieve(classes, params.XML_PATH), classes, params)
generator.generate_records(files, 'data')