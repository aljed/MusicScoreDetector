from dataclasses import dataclass
import numpy as np
import imageio as im
import os
import random
import parameters as p
import xml.etree.ElementTree as ET
import math
from tensorflow.keras.applications.vgg19 import preprocess_input

def create_bb(x, y, width, height, x_transposition, y_transposition):
    return BoundingBox(xmin = x - width/2 + x_transposition,
                        xmax = x + width/2 + x_transposition,
                        ymin = y - height/2 + y_transposition,
                        ymax = y + height/2 + y_transposition)


@dataclass
class BoundingBox:
    xmin: float
    xmax: float
    ymin: float
    ymax: float

    def get_area(self):
        return (self.xmax - self.xmin) / (self.ymax - self.ymin)

    def common_area(self, pos):  # returns None if rectangles don't intersect
        dx = min(self.xmax, pos.xmax) - max(self.xmin, pos.xmin)
        dy = min(self.ymax, pos.ymax) - max(self.ymin, pos.ymin)
        if (dx >= 0) and (dy >= 0):
            return dx * dy
        else:
            return 0

    def is_within(self, bb):
        return bb.xmin <= self.xmin and bb.xmax >= self.xmax and bb.ymin <= self.ymin and bb.ymax >= self.ymax

    def is_point_within(self, x, y):
        return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax

    def get_normalized(self, x, y):
        return BoundingBox(self.xmin / x, self.xmax / x, self.ymin / y, self.ymax / y)

    def get_relative_bb2(self, new_bb):
        return BoundingBox((self.xmin - new_bb.xmin) / (new_bb.xmax - new_bb.xmin),
                (self.xmax - new_bb.xmin) / (new_bb.xmax - new_bb.xmin),
                (self.ymin - new_bb.ymin) / (new_bb.ymax - new_bb.ymin),
                (self.ymax - new_bb.ymin) / (new_bb.ymax - new_bb.ymin))

    def get_relative_bb(self, new_bb):
        return BoundingBox(new_bb.xmin + (new_bb.xmax - new_bb.xmin) * self.xmin,
                           new_bb.xmin + (new_bb.xmax - new_bb.xmin) * self.xmax,
                           new_bb.ymin + (new_bb.ymax - new_bb.ymin) * self.ymin,
                           new_bb.ymin + (new_bb.ymax - new_bb.ymin) * self.ymax)

    def serialize(self, slice_bb) -> list:
        new_bb = self.get_relative_bb2(slice_bb)
        width = abs(new_bb.xmax - new_bb.xmin) / p.GX
        height = abs(new_bb.ymax - new_bb.ymin) / p.GY
        x = abs(self.xmax + self.xmin) / 2
        y = abs(self.ymax + self.ymin) / 2
        return [abs(width) % 1,
                abs(height) % 1,
                abs((x - slice_bb.xmin) / (slice_bb.xmax - slice_bb.xmin)) % 1,
                abs((y - slice_bb.ymin) / (slice_bb.ymax - slice_bb.ymin)) % 1]


@dataclass
class Element:
    typ: str
    bounding_box: BoundingBox

    def serialize(self, classes, cell_bb: BoundingBox, empty=False):
        confidence_score = 0
        prob_list = np.zeros([len(classes)])
        if not empty:
            confidence_score = 1
            prob_list[classes[self.typ]] = 1.0
        return np.concatenate([[confidence_score], self.bounding_box.serialize(cell_bb), prob_list])


@dataclass
class Data:
    img: list
    elements: list
    bb: BoundingBox

    def to_ts(self, output_dim, classes, bb: BoundingBox):
        # processed_image = preprocess_input(np.reshape(self.img, [p.Y, p.X, 3]))
        # return (processed_image,
        #         np.reshape(serialize_element_list(self.elements, classes, bb), output_dim))

        return (np.reshape(np.array(self.img) , (p.Y, p.X, 3)),
                np.reshape(serialize_element_list(self.elements, classes, bb), output_dim))


class Generator:

    def __init__(self, pages, output_dim, classes) -> None:
        self.pages = pages
        self.output_dim = output_dim
        self.classes = classes

    def generator(self, files):
        xs_ys = []
        for file in files:
            while True:
                if len(xs_ys) < p.BATCH_SIZE:
                    if not isinstance(file, str):
                        file = file.decode("utf-8")
                    splitted = split_image(file)
                    page = self.pages[file.replace(".png", ".xml")]
                    xs_ys_new = [Data(s.slice, page.retrieve_from_box(s.bb), s.bb) for s in splitted]
                    xs_ys += [d.to_ts(self.output_dim, self.classes, d.bb) for d in xs_ys_new if len(d.elements) > 0]
                if len(xs_ys) >= p.BATCH_SIZE:
                    elements_to_yield = xs_ys[0:p.BATCH_SIZE]
                    if len(xs_ys) > p.BATCH_SIZE:
                        xs_ys = xs_ys[p.BATCH_SIZE:]
                    yield (np.array([i for i, j in elements_to_yield]),
                           np.array([j for i, j in elements_to_yield]))
                else:
                    break


def serialize_element_list(elements, classes, bb: BoundingBox):
    output_array = np.empty([p.GX * p.GY, len(classes) + 5])

    for i in range(p.GX * p.GY):
        current_box_row_index = math.floor(i / p.GY)
        current_box_column_index = i % p.GY
        unit_cell_width = 1 / p.GX
        unit_cell_height = 1 / p.GY
        current_bb = BoundingBox(current_box_column_index * unit_cell_width,
                                 (current_box_column_index + 1) * unit_cell_width,
                                 current_box_row_index * unit_cell_height,
                                 (current_box_row_index + 1) * unit_cell_height)

        def is_within_current_cell(e):
            resultant_bb = e.bounding_box.get_relative_bb2(bb)
            x = (resultant_bb.xmax + resultant_bb.xmin) / 2
            y = (resultant_bb.ymax + resultant_bb.ymin) / 2
            return current_bb.is_point_within(x, y)

        elements_in_current_cell = [e for e in elements if is_within_current_cell(e)]
        if len(elements_in_current_cell) == 0:
            random_class_index = random.randrange(len(classes))
            random_element = Element(list(classes.keys())[random_class_index],
                                     BoundingBox(random.random(), random.random(), random.random(), random.random()))
            output_array[i, :] = random_element.serialize(classes, current_bb.get_relative_bb(bb), True)
        else:
            output_array[i, :] = elements_in_current_cell[0].serialize(classes, current_bb.get_relative_bb(bb), False)
    reshaped = np.reshape(np.array(output_array), (p.GX * p.GY * (len(classes) + 5)))

    return reshaped


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

    def retrieve(self, classes: list, xml_path=p.XML_PATH):

        files = os.listdir(xml_path)
        pages = {}
        num_of_files = len(files)
        counter = 1

        for f in files:

            if counter % 500 == 0:
                print(
                    f'{round(counter * 100 / num_of_files)}% of the files processed, we are at {counter} in {num_of_files}.')
            counter += 1
            page = Page(f)
            tree = ET.parse(xml_path + "/" + f)
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
    bb: BoundingBox


def split_image(filename):
    image = np.array(im.imread(p.PNG_PATH + '/' + filename))
    shape = np.shape(image)
    max_y = shape[0] - p.Y
    max_x = shape[1] - p.X
    parts = []

    for i in range(p.PARTS_NUMBER):
        random_y = random.randrange(max_y) #205
        random_x = random.randrange(max_x) #436
        slice = image[random_y:random_y + p.Y, random_x:random_x + p.X, 0:3]
        parts.append(PartData(slice, random_y, random_x, shape[0], shape[1],
                              BoundingBox(random_x / shape[1], (random_x + p.X) / shape[1], random_y / shape[0],
                                          (random_y + p.Y) / shape[0])))

    return parts


def retrieve_class_names():
    counter = 0
    names = {}

    if not p.CLASSES:
        files = os.listdir(p.CLASSES_PATH)
        for f in files:
            names[f.replace('.csv', '')] = counter
            counter += 1
    else:
        for index in p.CLASSES:
            names[index] = counter
            counter += 1

    return names
