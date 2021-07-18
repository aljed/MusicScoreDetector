import math
import os
import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt
import random
from dataclasses import dataclass
from statistics import median

from pip._internal.utils.misc import pairwise

ANGLE = math.radians(0)
COS = math.cos(ANGLE)
SIN = math.sin(ANGLE)
PICTURES = '../pictures/'


class Line:
    is_black: bool
    weight: int


@dataclass(frozen=True)
class Staff:
    lines: []


class StaffPositionFinder:

    def __init__(self):
        self.colour_threshold = 200
        self.start_threshold = 0.3

    def get_staff(self, image):
        return self.check_staff(self.get_positions(image, self.start_threshold))

    def get_positions(self, image, threshold):
        x = np.shape(image)[0]
        avg = np.mean(image, axis=2)

        list = []
        for i in range(x):
            c = np.count_nonzero(avg[i, :] < self.colour_threshold)
            if c / x > threshold:
                list.append(i)

        return list

    def check_staff(self, generator):
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
            staffs = []
            group = []

            for int in intervals:
                group.append(next(it))
                if m * 1.1 < int:
                    staffs.append(Staff(group.copy()))
                    group.clear()

            print(staffs)
            return staffs

        filled = fill_gaps(generator)
        merged = merge_thick_lines(filled)

        group(merged)

        return merged


def getPixelMap():
    files = os.listdir(PICTURES)
    random.shuffle(files)
    file = '1.pdf_6.jpg'
    file = files[0]
    print(file)
    image = mpimg.imread(PICTURES + '\\' + file)
    x = np.shape(image)[0]
    y = np.shape(image)[1]

    a = StaffPositionFinder()
    res = [round(x) for x in a.get_staff(image)]

    im = np.zeros([x, y, 3], dtype=np.uintc)
    im.fill(int(255))
    for i in range(len(res)):
        im[res[i], :, :] = 0
    return im


i = getPixelMap()
fig, ax = plt.subplots()
shown = ax.imshow(i)
plt.show()
