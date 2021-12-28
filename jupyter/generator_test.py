import random
import data
import os
import parameters as p
import importlib
import viewer as v
import numpy as np

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
print(act[1][0])
v.show_prediction(act[1][0], act[0][0])
