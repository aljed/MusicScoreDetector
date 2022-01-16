import math
import numpy as np
import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
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
    for i in range(len(staffs)-1):
        borders.append(staffs[i].get_border_between_staffs(staffs[i+1]))
    return borders


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


def check_staff(generator):
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
                staffs_list.append(lines_group.copy())
                lines_group.clear()

        lines_group.append(next(it))
        staffs_list.append(lines_group.copy())

        return staffs_list

    def fill_gaps(g):
        new_positions = []
        for i in range(len(g) - 1):
            if g[i + 1] - 2 == g[i]:
                new_positions.append(g[i])
                new_positions.append(g[i] + 1)
            else:
                new_positions.append(g[i])
                if i == len(g) - 2:
                    new_positions.append(g[i + 1])
        return new_positions

    filled = fill_gaps(generator)
    merged = merge_thick_lines(filled)
    staffs = [Staff(lines_group, []) for lines_group in group(merged)]

    return staffs


class StaffPositionFinder:

    def __init__(self):
        self.colour_threshold = 100
        self.start_threshold = 0.7

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
    threshold = 0.99
    colour_threshold = 100
    for staff in staffs:
        x = np.shape(img)[1]
        avg = np.mean(img, axis=2)
        y_range = staff.line_positions[4] - staff.line_positions[0]

        lst = []
        for i in range(x):
            c = np.count_nonzero(avg[round(staff.line_positions[0]):round(staff.line_positions[4]), i] < colour_threshold)
            if c / y_range > threshold:
                lst.append(i)

        staff.measure_positions = merge_thick_lines(lst)


# def getPixelMap():
#     files = os.listdir(PICTURES)
#     # random.shuffle(files)
#     file = "test.png"
#     print(file)
#     image = mpimg.imread(PICTURES + '\\' + file) * 255
#     x = np.shape(image)[0]
#     y = np.shape(image)[1]
#
#     staffs = get_staff_positions(image)
#     line_positions = [staff.line_positions for staff in staffs]
#     line_positions = np.array(line_positions, dtype=np.uintc)
#     line_positions = np.reshape(line_positions, [-1])
#
#     im = np.zeros([x, y, 3], dtype=np.uintc)
#     im.fill(int(255))
#     for i in range(len(line_positions)):
#         im[line_positions[i], :, :] = 0
#     return im
#
#
# i = getPixelMap()
# fig, ax = plt.subplots()
# shown = ax.imshow(i)
# plt.show()
