import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

import parameters as p
import math


def show_prediction(y1, x1):

    def extract_bb(y):
        return np.reshape(y[0], (p.GX * p.GY, -1))[..., 0:5]

    def show_bb(y, x):
        fig, ax = plt.subplots()
        ax.imshow(x[0])

        rectangles = []
        for i in range(p.GX * p.GY):
            current_box_row_index = math.floor(i / p.GY)
            current_box_column_index = i % p.GY
            width = y[i][1] * p.X
            height = y[i][2] * p.Y
            x_anchor = (current_box_column_index + y[i][3]) / p.GY * p.X - width / 2
            y_anchor = (current_box_row_index + y[i][4]) / p.GX * p.Y - height / 2
            if y[i][0] > 0:
                rectangles.append([x_anchor, y_anchor, width, height])

        for r in rectangles:
            p1 = patches.Rectangle((r[0], r[1]), r[2], r[3], linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(p1)

        plt.draw() 
        plt.show()

    show_bb(extract_bb(y1), x1)
