import math
import os
import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt
import random
import time


ANGLE = math.radians(0)
COS = math.cos(ANGLE)
SIN = math.sin(ANGLE)
PICTURES = '../pictures/'

test = []


def transform(x, y, value):
    v = round(x * COS + y * SIN)
    if v == 500 or v == 501 and value == 255:
        return 0
    else:
        return 255


def t2(x, y, value):
    if value > 128:
        return 255
    else:
        return 0


# def getPixelMap():
#     files = os.listdir(PICTURES)
#     random.shuffle(files)
#     for file in files:
#         image = mpimg.imread(PICTURES + '\\' + file)
#         x = np.shape(image)[0]
#         y = np.shape(image)[1]
#         avg = np.mean(image, axis=2)
#         transformed = np.empty([x, y, 3])
#         start = time.time()
#         for i in range(x):
#             for j in range(y):
#                 t = t2(i, j, avg[i][j])
#                 transformed[i][j][0] = t
#                 transformed[i][j][1] = t
#                 transformed[i][j][2] = t
#         end = time.time()
#         print(end - start)
#
#         return transformed


def getPixelMap():
    files = os.listdir(PICTURES)
    # random.shuffle(files)
    for file in files:
        image = mpimg.imread(PICTURES + '\\' + file)
        x = np.shape(image)[0]
        y = np.shape(image)[1]
        avg = np.mean(image, axis=2)
        res = []
        for i in range(x):
            c = np.count_nonzero(avg[i, :] < 200)
            if(c/y > 0.01):
                res.append(1)
            else:
                res.append(0)
        im = np.zeros([x,y,3 ])
        for i in range(len(res)):
            if res[i] == 1:
                im[:, res[i], :] = 255
        return im


image = getPixelMap()
fig, ax = plt.subplots()
shown = ax.imshow(image)
print(image)
plt.show()
