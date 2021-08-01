PNG_PATH = 'C:\\Users\\user\\Downloads\\deep_scores_dense\\deep_scores_dense\\images_png'
XML_PATH = 'C:\\Users\\user\\Downloads\\deep_scores_dense\\deep_scores_dense\\xml_annotations'
CONVERTED_PATH = 'C:\\Users\\user\\Downloads\\deep_scores_dense\\deep_scores_dense\\converted'
CLASSES_PATH = 'C:\\Users\\user\\Downloads\\deep_scores_dense\\deep_scores_dense\\meta_info'
X = 100
Y = 100
PARTS_NUMBER = 100
ELEMENTS_MAX_NUMBER = 10


# %%
import os
import imageio as im
import random
import numpy as np
from dataclasses import dataclass
import xml.etree.ElementTree as ET

random.seed()

@dataclass
class PartData:
    slice: list
    y: int
    x: int
    max_y: int
    max_x: int

def split_image(filename):
    
    image = np.array(im.imread(PNG_PATH + '\\' + filename))
    shape = np.shape(image)
    max_y = shape[0] - Y
    max_x = shape[1] - X
    parts = []
    
    for i in range(PARTS_NUMBER):
        random_y = random.randrange(max_y)
        random_x = random.randrange(max_x)
        slice = image[random_y:random_y + Y, random_x:random_x + X, 0]
        parts.append(PartData(slice, random_y, random_x, shape[0], shape[1]))
        
    return parts


# %%
@dataclass
class BoundingBox:
    xmin: float
    xmax: float
    ymin: float
    ymax: float
        
    def is_within(self, bb):
        return bb.xmin <= self.xmin and bb.xmax >= self.xmax and bb.ymin <= self.ymin and bb.ymax >= self.ymax

    def get_normalized(self, x, y):
        return BoundingBox(self.xmin/x, self.xmax/x, self.ymin/y, self.ymax/y)

    def serialize(self) -> list[float]:
        return [self.xmin, self.xmax, self.ymin, self.ymax]

def retrieve_class_names():
    files = os.listdir(CLASSES_PATH)
    counter = 0
    names = {}
    for f in files:
        names[f.replace('.csv', '')] = counter
        counter += 1
    return names

classes = retrieve_class_names()

@dataclass
class Element:
    typ: str
    bounding_box: BoundingBox   

    def serialize(self):
        prob_list = np.zeros([len(classes)])
        prob_list[classes[self.typ]] = 1.0
        return np.concatenate([prob_list, self.bounding_box.serialize(), [1.0]])

class Page:

    def __init__(self, name):
        self.name = name
        self.elements = []
        
    def add(self, element):
        self.elements.append(element)
        
    def retrieve_from_box(self, bb):
        filtered = []
        for e in self.elements:
            if e.bounding_box.is_within(bb):
                filtered.append(e)
        return filtered

    
class Retriever:
    
    def retrieve():

        files = os.listdir(XML_PATH)
        pages = {}
        num_of_files = len(files)
        counter = 1

        for f in files:

            if counter % 100 == 0:
                print(f'{round(counter*100/num_of_files)}% of the files processed, we are at {counter} in {num_of_files}.')
            counter += 1
            page = Page(f)
            tree = ET.parse(XML_PATH + "\\" + f)
            root = tree.getroot()

            for obj in root.iter('object'):

                raw_bb = obj.find('bndbox')
                page.add(Element(
                    obj.find('name').text,
                    BoundingBox(
                        float(raw_bb.find('xmin').text),
                        float(raw_bb.find('xmax').text),
                        float(raw_bb.find('ymin').text),
                        float(raw_bb.find('ymax').text)
                )))

            pages[f] = page

        return pages         


# %%
pages = Retriever.retrieve() 


# %%
import tensorflow as tf

output_dim = ELEMENTS_MAX_NUMBER * (5 + len(classes))

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(Y,X,1)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(16, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(1024, activation='relu'),
    tf.keras.layers.Dense(output_dim, activation='sigmoid')
])


# %%
# Get generator of data

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

@dataclass
class Data:
    img: list
    elements: list

    def to_ts(self):
        return (np.reshape(self.img, (1, Y, X, 1)), np.reshape(serialize_element_list(self.elements), (1, output_dim)))
  
def generator(files):
    for file in files:
        file = file.decode("utf-8")
        splitted = split_image(file)
        page = pages[file.replace(".png", ".xml")]
        for s in splitted:
            data = Data(s.slice, page.retrieve_from_box(BoundingBox(s.x / s.max_x, (s.x + X) / s.max_x, s.y / s.max_y, (s.y + Y) / s.max_y)))
            yield data.to_ts()


# %%
files = os.listdir(PNG_PATH)
ds = tf.data.Dataset.from_generator(generator, args=[files], output_types=(tf.int32, tf.float32), output_shapes=([1, Y, X, 1], [1, output_dim]))


# %%
def serialize_element_list(elements):
    output_array = np.empty([ELEMENTS_MAX_NUMBER, len(classes) + 5])

    for i in range(ELEMENTS_MAX_NUMBER - len(elements)):
        random_class_index = random.randrange(len(classes))
        elements.append(
            Element(list(classes.keys())[random_class_index], BoundingBox(random.random(), random.random(), random.random(), random.random()))
        )

    for i in range(len(elements)):
        output_array[i,:] = elements[i].serialize()

    return np.reshape(np.array(output_array), (ELEMENTS_MAX_NUMBER * (len(classes) + 5)))

model.compile(optimizer='adam',
              loss=tf.keras.losses.CategoricalCrossentropy(), 
              metrics=['accuracy'])
a = model.fit(ds, epochs=2)


