import math
from dataclasses import dataclass

import numpy as np
import imageio as im
from typing import List

from data import BoundingBox
from StaffPositionRetriever import get_border_pixels, get_staff_positions
import deserializer as d
from parameters import Params
import xml.etree.cElementTree as ET


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
        elements = ElementsMap(self.model_params.CLASSES, height, width)

        ymax = self.model_params.Y
        ymin = 0

        for y_stride in range(num_of_y_strides):

            if ymax >= height + 128:
                break

            if ymax > height:
                ymin = height - self.model_params.Y
                ymax = height

            xmin = 0
            xmax = self.model_params.X

            for x_stride in range(num_of_x_strides):

                if xmax >= width + 128:
                    break

                if xmax > width:
                    xmin = width - self.model_params.X
                    xmax = width

                img_slice = image[ymin:ymax, xmin:xmax]
                prediction = self.predict(raw_images=[img_slice[:,:,0:3]])[0][0]
                bb_index = 0

                while prediction[bb_index][5] > self.acceptance_threshold:

                    bb_xmin = round(prediction[bb_index][2])
                    bb_ymin = round(prediction[bb_index][1])
                    bb_xmax = round(prediction[bb_index][4])
                    bb_ymax = round(prediction[bb_index][3])

                    bb = BoundingBox(bb_xmin + xmin, bb_xmax + xmin, bb_ymin + ymin, bb_ymax + ymin)
                    name = self.model_params.CLASSES[0]
                    elements.add(name, bb)

                    bb_index += 1

                xmin += self.x_stride
                xmax += self.x_stride

            ymin += self.y_stride
            ymax += self.y_stride

        elements.postprocess(self.coef)
        #
        # import pickle
        # with open("demofile.txt", "wb") as f:
        #         #     pickle.dump((elements, image), f)
        # with open("demofile.txt", "rb") as f:
        #     (elements, image) = pickle.load(f)

        return self.convert_to_xml(elements, image)

    def wrap_measures(self, measure_xmls):
        pass  # todo

    def convert_to_xml(self, elements_map, image):
        staffs = get_staff_positions(image)
        groups: List[d.Group] = elements_map.group_by(staffs)
        measure_xmls = []
        for g in groups:
            measure_xmls += g.deserialize()
        i = 0
        for m in measure_xmls:
            m.set("number", str(i))
            i += 1
        return [ET.dump(m) for m in measure_xmls]
        return self.wrap_measures(measure_xmls)


class ElementsMap:

    @dataclass
    class Element:
        position: BoundingBox
        used: bool

        def is_similar(self, second, coef):
            return self.position.common_area(second.position) / ((self.position.get_area() + second.position.get_area()) / 2) > coef

    def __init__(self, classes, height, width):
        self.elements = {c: [] for c in classes}
        self.height = height
        self.width = width

    def add(self, name, bb):
        self.elements[name].append(self.Element(bb, False))

    def postprocess(self, coef):
        for name in self.elements:
            self.elements[name] = self.group_similar(self.elements[name], coef)

    def group_similar(self, elements, coef):
        new_elements = []
        for i in range(len(elements)):
            if not elements[i].used:
                neighbours = [elements[i]]
                for j in range(len(elements)):
                    if not elements[j].used and j != i:
                        if elements[j].is_similar(elements[i], coef):
                            neighbours.append(elements[j])
                            elements[j].used = True
                new_elements.append(self.aggregate(neighbours))
        return new_elements

    def aggregate(self, neighbours):
        avg_xmax = np.sum([n.position.xmax for n in neighbours]) / len(neighbours)
        avg_xmin = np.sum([n.position.xmin for n in neighbours]) / len(neighbours)
        avg_ymax = np.sum([n.position.ymax for n in neighbours]) / len(neighbours)
        avg_ymin = np.sum([n.position.ymin for n in neighbours]) / len(neighbours)
        return self.Element(BoundingBox(avg_xmax, avg_xmin, avg_ymax, avg_ymin), False)

    def group_by(self, staffs):
        borders = get_border_pixels(staffs)
        borders.insert(0, 0)
        borders.append(math.inf)
        groups = []
        for i in range(len(borders) - 1):
            ymin = borders[i]
            if i + 1 == len(borders):
                ymax = self.height
            else:
                ymax = borders[i+1]
            groups.append(d.Group(staffs[i], self.get_elements_in_range(ymin, ymax, staffs[i])))
        return groups

    def get_elements_in_range(self, ymin, ymax, staff):
        measures = []
        for i in range(len(staff.measure_positions)):
            xmin = staff.measure_positions[i]
            if i == len(staff.measure_positions) - 1:
                xmax = self.width
            else:
                xmax = staff.measure_positions[i + 1]
            measure_map = ElementsMap(self.elements.keys(), self.height, self.width)
            for c in self.elements:
                for e in self.elements[c]:
                    y_midpoint = (e.position.ymax + e.position.ymin)/2
                    x_midpoint = (e.position.xmax + e.position.xmin)/2
                    if ymin <= y_midpoint < ymax and xmin <= x_midpoint < xmax:
                        measure_map.add(c, e.position)
            measures.append(d.Measure(xmin, xmax, measure_map))
        return measures
