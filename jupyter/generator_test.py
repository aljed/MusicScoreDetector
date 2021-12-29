import random
import data
import os
import parameters as p
import importlib
import viewer as v
import numpy as np
from keras import backend as K

random.seed(1)
importlib.reload(p)
importlib.reload(data)

random.seed()
classes = data.retrieve_class_names()
output_dim = p.GX * p.GY * (5 + len(classes))
pages = data.Retriever().retrieve(classes, r'../test_xml_resources')

files = os.listdir(r'../test_resources')
generator = data.Generator(pages, output_dim, classes).generator(files)
act = generator.__next__()

np.set_printoptions(suppress=True)

#v.show_prediction(act[1], act[0])

def get_loss(y_actual, y_pred):
    y_actual_reshaped = K.reshape(y_actual, [p.BATCH_SIZE * p.GX * p.GY, -1])
    y_pred_reshaped = K.reshape(y_pred, [p.BATCH_SIZE * p.GX * p.GY, -1])

    main_probs_act = y_actual_reshaped[..., 0:1]
    main_probs_pred = y_pred_reshaped[..., 0:1]
    bb_probs_act = y_actual_reshaped[..., 1:3]
    bb_probs_pred = y_pred_reshaped[..., 1:3]
    classes_probs_act = y_actual_reshaped[..., 5:]
    classes_probs_pred = y_pred_reshaped[..., 5:]

    #loss = K.sum(K.binary_crossentropy(main_probs_act, main_probs_pred, from_logits=True))
    loss = K.sum(K.abs(main_probs_act - main_probs_pred))
    loss += K.sum(K.sum(K.abs(bb_probs_act - bb_probs_pred), 1) * main_probs_act)
    # loss += K.sum(K.sum(K.abs(classes_probs_act - classes_probs_pred), 1) * main_probs_act)

    return loss


print(get_loss(act[1], act[1]))
