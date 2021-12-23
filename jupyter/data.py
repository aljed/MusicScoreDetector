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

    # a może nie trzymać się tego tak restrykcyjnie?
    def is_within(self, bb):
        return bb.xmin <= self.xmin and bb.xmax >= self.xmax and bb.ymin <= self.ymin and bb.ymax >= self.ymax

    def get_normalized(self, x, y):
        return BoundingBox(self.xmin / x, self.xmax / x, self.ymin / y, self.ymax / y)

    def serialize(self) -> list[float]:
        return [self.xmin, self.xmax, self.ymin, self.ymax]


@dataclass
class Element:
    typ: str
    bounding_box: BoundingBox

    def serialize(self, classes, empty=False):
        confidence_score = 0
        prob_list = np.zeros([len(classes)])
        if not empty:
            confidence_score = 1
            prob_list[classes[self.typ]] = 1.0
        return np.concatenate([[confidence_score], self.bounding_box.serialize(), prob_list])


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

    def retrieve(self, classes: list):

        files = os.listdir(p.XML_PATH)
        pages = {}
        num_of_files = len(files)
        counter = 1

        for f in files:

            if counter % 100 == 0:
                print(
                    f'{round(counter * 100 / num_of_files)}% of the files processed, we are at {counter} in {num_of_files}.')
            counter += 1
            page = Page(f)
            tree = ET.parse(p.XML_PATH + "\\" + f)
            root = tree.getroot()

            for obj in root.iter('object'):
                raw_bb = obj.find('bndbox')
                typ = obj.find('name').text
                if classes.__contains__(typ):
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
        slice = image[random_y:random_y + p.Y, random_x:random_x + p.X, 0:3]
        parts.append(PartData(slice, random_y, random_x, shape[0], shape[1]))

    return parts


def retrieve_class_names():
    counter = 0
    names = {}

    if not p.USED_PARAMETERS:
        files = os.listdir(p.CLASSES_PATH)
        for f in files:
            names[f.replace('.csv', '')] = counter
            counter += 1
    else:
        for index in p.USED_PARAMETERS:
            names[index] = counter
            counter += 1

    return names


@dataclass
class Data:
    img: list
    elements: list

    def to_ts(self, output_dim, classes):
        return (np.reshape(np.array(self.img) / 255, (p.Y, p.X, 3)),
                np.reshape(serialize_element_list(self.elements, classes), (output_dim)))


class Generator:

    def __init__(self, pages, output_dim, classes) -> None:
        self.pages = pages
        self.output_dim = output_dim
        self.classes = classes

    def generator(self, files):
        for file in files:
            if not isinstance(file, str):
                file = file.decode("utf-8")
            splitted = split_image(file)
            page = self.pages[file.replace(".png", ".xml")]
            xs_ys = [Data(s.slice, page.retrieve_from_box(
                        BoundingBox(s.x / s.max_x, (s.x + p.X) / s.max_x, s.y / s.max_y, (s.y + p.Y) / s.max_y))) \
                        .to_ts(self.output_dim, self.classes) for s in splitted]
            yield (np.array([i for i, j in xs_ys]),
                   np.array([j for i, j in xs_ys]))


def serialize_element_list(elements, classes):
    output_array = np.empty([p.ELEMENTS_MAX_NUMBER, len(classes) + 5])
    empty_number = p.ELEMENTS_MAX_NUMBER - len(elements)
    for i in range(p.ELEMENTS_MAX_NUMBER - len(elements)):
        random_class_index = random.randrange(len(classes))
        elements.append(
            Element(list(classes.keys())[random_class_index],
                    BoundingBox(random.random(), random.random(), random.random(), random.random()))
        )
    for i in range(len(elements)):
        empty = False
        if empty_number > 0:
            empty = True
        output_array[i, :] = elements[i].serialize(classes, empty)
    reshaped = np.reshape(np.array(output_array), (p.ELEMENTS_MAX_NUMBER * (len(classes) + 5)))
    return reshaped
