import math
import numpy as np
# import os
# import matplotlib.image as mpimg
# import matplotlib.pyplot as plt
# import random
from dataclasses import dataclass
from statistics import median

ANGLE = math.radians(0)
COS = math.cos(ANGLE)
SIN = math.sin(ANGLE)
PICTURES = r'../deep_scores_dense/images_png'


def get_staff_positions(image) -> list:
    staffs = StaffPositionFinder().get_staff(image)
    complete_measures_positions(staffs, image)
    return staffs


@dataclass
class Staff:
    line_positions: list
    measure_positions: list

    def get_border_between_staffs(self, second):
        return (self.line_positions[4] + second.line_positions[0]) / 2


def get_border_pixels(staffs):
    borders = []
    for i in range(len(staffs)-2):
        borders.append(staffs[i].get_border_between_staffs(staffs[i+1]))
    return borders


class Line:
    is_black: bool
    weight: int


def check_staff(generator):
    def merge_thick_lines(lines):

        if len(lines) == 0:
            return np.array([])
        counter = 1

        while len(lines) > counter and lines[counter] - 1 == lines[counter - 1]:
            counter += 1

        if counter % 2 != 0:
            pos = lines[int(counter / 2 - 1 / 2)]
        else:
            pos = (lines[int(counter / 2 - 1)] + lines[int(counter / 2)]) / 2

        return np.insert(merge_thick_lines(lines[counter:]), 0, pos)

    def fill_gaps(g):
        new_positions = []
        for i in range(len(g) - 1):
            if g[i + 1] - 2 == g[i]:
                new_positions.append(g[i])
                new_positions.append(g[i] + 1)
            else:
                new_positions.append(g[i])
        return new_positions

    def group(lines):

        pairs = []
        for i in range(len(lines) - 1):
            pairs.append((lines[i], lines[i + 1]))

        intervals = list(map(lambda a: a[1] - a[0], pairs))
        m = median(intervals)
        it = iter(lines)
        staffs_list = []
        lines_group = []

        for interval in intervals:
            lines_group.append(next(it))
            if m * 1.5 < interval:
                staffs_list.append(Staff(lines_group.copy(), []))
                lines_group.clear()

        staffs_list.append(Staff(lines_group.copy(), []))

        return staffs_list

    filled = fill_gaps(generator)
    merged = merge_thick_lines(filled)
    staffs = group(merged)

    return staffs


class StaffPositionFinder:

    def __init__(self):
        self.colour_threshold = 1
        self.start_threshold = 0.3

    def get_staff(self, image):
        return check_staff(self.get_positions(image, self.start_threshold))

    def get_positions(self, image, threshold):
        x = np.shape(image)[0]
        avg = np.mean(image, axis=2)

        lst = []
        for i in range(x):
            c = np.count_nonzero(avg[i, :] < self.colour_threshold)
            if c / x > threshold:
                lst.append(i)

        return lst


def complete_measures_positions(staffs, img):
    threshold = 0.9
    colour_threshold = 200
    for staff in staffs:
        x = np.shape(img)[1]
        avg = np.mean(img, axis=2)

        lst = []
        for i in range(x):
            c = np.count_nonzero(avg[staff.line_positions[0]:staff.line_positions[4], i] < colour_threshold)
            if c / x > threshold:
                lst.append(i)

        staff.measure_positions = lst


# def getPixelMap():
#     files = os.listdir(PICTURES)
#     # random.shuffle(files)
#     file = files[0]
#     print(file)
#     image = mpimg.imread(PICTURES + '\\' + file)
#     x = np.shape(image)[0]
#     y = np.shape(image)[1]
#
#     a = StaffPositionFinder()
#     res = [round(x) for x in a.get_staff(image)]
#
#     im = np.zeros([x, y, 3], dtype=np.uintc)
#     im.fill(int(255))
#     for i in range(len(res)):
#         im[res[i], :, :] = 0
#     return im
#
#
# i = getPixelMap()
# fig, ax = plt.subplots()
# shown = ax.imshow(i)
# plt.show()
