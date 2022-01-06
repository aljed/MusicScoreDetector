import math
from dataclasses import dataclass

import numpy as np
import imageio as im

from data import BoundingBox, create_bb
from StaffPositionRetriever import get_border_pixels, get_staff_positions
from deserializer import Group
from parameters import Params


class Converter:

    def __init__(self, overlapping, y_stride, x_stride, predict, model_params: Params, acceptance_threshold, coef):
        self.overlapping = overlapping
        self.y_stride = y_stride
        self.x_stride = x_stride
        self.predict = predict
        self.model_params = model_params
        self.acceptance_threshold = acceptance_threshold
        self.coef = coef

    def convert(self, png_path):
        image = np.array(im.imread(png_path))
        # np.pad()
        shape = np.shape(image)
        height = shape[0]
        width = shape[1]
        num_of_x_strides = math.ceil((width - self.model_params.X) / self.x_stride) + 1
        num_of_y_strides = math.ceil((height - self.model_params.Y) / self.y_stride) + 1
        elements = ElementsMap(self.model_params.CLASSES)

        xmin = 0
        ymin = 0
        xmax = self.model_params.X
        ymax = self.model_params.Y

        for y_stride in range(num_of_y_strides):
            for x_stride in range(num_of_x_strides):

                img_slice = image[xmin:xmax][ymin:ymax]
                prediction = self.predict(img_slice)

                for i in range(self.model_params.GX * self.model_params.GY):
                    current_box_row_index = math.floor(i / self.model_params.GY)
                    current_box_column_index = i % self.model_params.GY
                    width = prediction[i][1] * self.model_params.X
                    height = prediction[i][2] * self.model_params.Y
                    x_anchor = (current_box_column_index + prediction[i][
                        3]) / self.model_params.GX * self.model_params.X - width / 2
                    y_anchor = (current_box_row_index + prediction[i][
                        4]) / self.model_params.GY * self.model_params.Y - height / 2
                    if prediction[i][0] > self.acceptance_threshold:
                        name = self.model_params.CLASSES[np.argmax(np.array(prediction[i][5:]))]
                        elements.add(name, create_bb(x_anchor, y_anchor, width, height, xmin, ymin))

                xmin += self.x_stride
                xmax += self.x_stride

            ymin += self.y_stride
            ymax += self.y_stride

        elements.postprocess(self.coef)
        return self.convert_to_xml(elements, image)

    def wrap_measures(self, measure_xmls):
        pass  # todo

    def convert_to_xml(self, elements_map, image):
        staffs = get_staff_positions(image)
        groups: list[Group] = elements_map.group_by(staffs)
        measure_xmls = [g.deserialize() for g in groups]
        return self.wrap_measures(measure_xmls)


class ElementsMap:

    @dataclass
    class Element:
        position: BoundingBox
        used: bool

        def is_similar(self, second, coef):
            return self.position.common_area(second) / ((self.position.get_area() + second.get_area()) / 2) > coef

    def __init__(self, classes):
        self.elements = {c: [] for c in classes}

    def add(self, name, bb):
        self.elements[name].append(self.Element(bb, False))

    def postprocess(self, coef):
        for (name, elements) in self.elements:
            self.elements[name] = self.group_similar(elements, coef)

    def group_similar(self, elements, coef):
        new_elements = []
        for i in range(len(elements)):
            if not elements[i].used:
                neighbours = [elements[i]]
                for j in range(len(elements)):
                    if not elements[j].used:
                        if elements[j].is_similar(elements[i], coef):
                            neighbours.append(elements[j])
                            elements[j].used = True
                new_elements.append(self.aggregate(neighbours))
        return new_elements

    def aggregate(self, neighbours):
        avg_xmax = np.sum([n.xmax for n in neighbours]) / len(neighbours)
        avg_xmin = np.sum([n.xmin for n in neighbours]) / len(neighbours)
        avg_ymax = np.sum([n.ymax for n in neighbours]) / len(neighbours)
        avg_ymin = np.sum([n.ymin for n in neighbours]) / len(neighbours)
        return self.Element(BoundingBox(avg_xmax, avg_xmin, avg_ymax, avg_ymin), False)

    def group_by(self, staffs):
        borders = get_border_pixels(staffs)
        borders.insert(0, 0)
        groups = []
        for i in range(len(borders) - 1):
            ymin = borders[i]
            if i + 1 == len(borders):
                ymax = math.inf
            else:
                ymax = borders[i+1]
            groups.append(Group(staffs[i], self.get_elements_in_range(ymin, ymax, staffs[i])))
        return groups

    def get_elements_in_range(self, ymin, ymax, staff):
        measures = []
        for i in range(len(staff.measure_positions) - 2):
            xmin = staff.measure_positions[i]
            xmax = staff.measure_positions[i + 1]
            measure_map = ElementsMap(self.elements.keys())
            for c, elements in self.elements:
                for e in elements:
                    y_midpoint = (e.bb.ymax + e.bb.ymin)/2
                    x_midpoint = (e.bb.xmax + e.bb.xmin)/2
                    if ymin <= y_midpoint < ymax and xmin <= x_midpoint < xmax:
                        measure_map.add(c, e.bb)
            measures.append(measure_map)
        return measures
