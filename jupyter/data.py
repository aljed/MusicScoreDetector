from dataclasses import dataclass
import numpy as np
import imageio as im
import os
import random
import parameters as p
import xml.etree.ElementTree as ET
import math


@dataclass
class BoundingBox:
    xmin: float
    xmax: float
    ymin: float
    ymax: float

    def is_within(self, bb):
        return bb.xmin <= self.xmin and bb.xmax >= self.xmax and bb.ymin <= self.ymin and bb.ymax >= self.ymax

    def is_point_within(self, x, y):
        return self.xmin >= x >= self.xmax and self.ymin >= y >= self.ymax

    def get_normalized(self, x, y):
        return BoundingBox(self.xmin / x, self.xmax / x, self.ymin / y, self.ymax / y)

    def serialize(self, slice_bb) -> list[float]:
        return [(self.xmin - slice_bb.xmin) / (slice_bb.xmax - slice_bb.xmin),
                (self.xmax - slice_bb.xmin) / (slice_bb.xmax - slice_bb.xmin),
                (self.ymin - slice_bb.ymin) / (slice_bb.ymax - slice_bb.ymin),
                (self.ymax - slice_bb.ymin) / (slice_bb.ymax - slice_bb.ymin)]


@dataclass
class Element:
    typ: str
    bounding_box: BoundingBox

    def serialize(self, classes, slice_bb: BoundingBox, empty=False):
        confidence_score = 0
        prob_list = np.zeros([len(classes)])
        if not empty:
            confidence_score = 1
            prob_list[classes[self.typ]] = 1.0
        return np.concatenate([[confidence_score], self.bounding_box.serialize(slice_bb), prob_list])


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

            if counter % 500 == 0:
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
    bb: BoundingBox


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
        parts.append(PartData(slice, random_y, random_x, shape[0], shape[1],
                              BoundingBox(random_x / max_x, (random_x + p.X) / max_x, random_y / max_y,
                                          (random_y + p.Y) / max_y)))

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
    bb: BoundingBox

    def to_ts(self, output_dim, classes, bb: BoundingBox):
        return (np.reshape(np.array(self.img) / 255, (p.Y, p.X, 3)),
                np.reshape(serialize_element_list(self.elements, classes, bb), output_dim))


class Generator:

    def __init__(self, pages, output_dim, classes) -> None:
        self.pages = pages
        self.output_dim = output_dim
        self.classes = classes

    def generator(self, files):
        xs_ys = []
        for file in files:
            if not isinstance(file, str):
                file = file.decode("utf-8")
            splitted = split_image(file)
            page = self.pages[file.replace(".png", ".xml")]
            if len(xs_ys) < p.BATCH_SIZE:
                xs_ys_new = [Data(s.slice, page.retrieve_from_box(s.bb), s.bb) for s in splitted]
                xs_ys += [d.to_ts(self.output_dim, self.classes, d.bb) for d in xs_ys_new if len(d.elements) > 0]
            if len(xs_ys) >= p.BATCH_SIZE:
                elements_to_yield = xs_ys[0:p.BATCH_SIZE]
                if len(xs_ys) > p.BATCH_SIZE:
                    xs_ys = xs_ys[p.BATCH_SIZE:]
                yield (np.array([i for i, j in elements_to_yield]),
                       np.array([j for i, j in elements_to_yield]))


def serialize_element_list(elements, classes, bb: BoundingBox):
    output_array = np.empty([p.GX * p.GY, len(classes) + 5])

    for i in range(p.GX * p.GY):
        current_box_row_index = math.floor(i / p.GY)
        current_box_column_index = i % p.GY
        unit_cell_width = (bb.xmax - bb.xmin) / p.GX
        unit_cell_height = (bb.ymax - bb.ymin) / p.GY
        current_bb = BoundingBox(current_box_column_index * unit_cell_width,
                                 (current_box_column_index + 1) * unit_cell_width,
                                 current_box_row_index * unit_cell_height,
                                 (current_box_row_index + 1) * unit_cell_height )
        elements_in_current_cell = [e for e in elements if
                                    current_bb.is_point_within((e.bounding_box.xmax + e.bounding_box.xmin) / 2,
                                                               (e.bounding_box.ymax + e.bounding_box.ymin) / 2)]
        if len(elements_in_current_cell) == 0:
            random_class_index = random.randrange(len(classes))
            random_element = Element(list(classes.keys())[random_class_index],
                                     BoundingBox(random.random(), random.random(), random.random(), random.random()))
            output_array[i, :] = random_element.serialize(classes, current_bb, True)
        else:
            output_array[i, :] = elements_in_current_cell[0].serialize(classes, current_bb, False)
    reshaped = np.reshape(np.array(output_array), (p.GX * p.GY * (len(classes) + 5)))

    return reshaped
