from dataclasses import dataclass
import numpy as np
import imageio as im
import os
import random
import parameters as p
import xml.etree.ElementTree as ET


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


@dataclass
class Element:
    typ: str
    bounding_box: BoundingBox   

    def serialize(self, classes):
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

        files = os.listdir(p.XML_PATH)
        pages = {}
        num_of_files = len(files)
        counter = 1

        for f in files:

            # if counter % 100 == 0:
            #     print(f'{round(counter*100/num_of_files)}% of the files processed, we are at {counter} in {num_of_files}.')
            counter += 1
            page = Page(f)
            tree = ET.parse(p.XML_PATH + "\\" + f)
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


@dataclass
class PartData:
    slice: list
    y: int
    x: int
    max_y: int
    max_x: int


def split_image(filename):
    
    image = np.array(im.imread(p.PNG_PATH + '\\' + filename))
    shape = np.shape(image)
    max_y = shape[0] - p.Y
    max_x = shape[1] - p.X
    parts = []
    
    for i in range(p.PARTS_NUMBER):
        random_y = random.randrange(max_y)
        random_x = random.randrange(max_x)
        slice = image[random_y:random_y + p.Y, random_x:random_x + p.X, 0]
        parts.append(PartData(slice, random_y, random_x, shape[0], shape[1]))
        
    return parts


def retrieve_class_names():
    files = os.listdir(p.CLASSES_PATH)
    counter = 0
    names = {}
    for f in files:
        names[f.replace('.csv', '')] = counter
        counter += 1
    return names


@dataclass
class Data:
    img: list
    elements: list

    def to_ts(self, output_dim, classes):
        return (np.reshape(self.img/255, (1, p.Y, p.X, 1)), np.reshape(serialize_element_list(self.elements, classes), (1, output_dim)))
  
class Generator:

    def __init__(self, pages, output_dim, classes) -> None:
        self.pages = pages
        self.output_dim = output_dim
        self.classes = classes

    def generator(self, files):
        for file in files:
            file = file.decode("utf-8")
            splitted = split_image(file)
            page = self.pages[file.replace(".png", ".xml")]
            for s in splitted:
                data = Data(s.slice, page.retrieve_from_box(BoundingBox(s.x / s.max_x, (s.x + p.X) / s.max_x, s.y / s.max_y, (s.y + p.Y) / s.max_y)))
                yield data.to_ts(self.output_dim, self.classes)


def serialize_element_list(elements, classes):
    output_array = np.empty([p.ELEMENTS_MAX_NUMBER, len(classes) + 5])
    for i in range(p.ELEMENTS_MAX_NUMBER - len(elements)):
        random_class_index = random.randrange(len(classes))
        elements.append(
            Element(list(classes.keys())[random_class_index], BoundingBox(random.random(), random.random(), random.random(), random.random()))
        )
    for i in range(len(elements)):
        output_array[i,:] = elements[i].serialize(classes)
    reshaped = np.reshape(np.array(output_array), (p.ELEMENTS_MAX_NUMBER * (len(classes) + 5)))
    return reshaped