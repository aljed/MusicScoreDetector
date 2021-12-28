import matplotlib.pyplot as plt
import matplotlib.patches as patches
import parameters as p
import math

def show_prediction(y, x):

    def extract_bb(y):
        return y[:5]

    def show_bb(y, x):
        fig, ax = plt.subplots()
        ax.imshow(x)
        rectangles = get_rectangles(y)
        for r in rectangles:
            p = patches.Rectangle((r[1], r[3]), r[0] - r[1], r[2] - r[3], linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(p)

        plt.draw()
        plt.show()

    show_bb(extract_bb(y), x)

    def get_rectangles(y):
        for i in range(p.GX * p.GY):
            current_box_row_index = math.floor(i / p.GY)
            current_box_column_index = i % p.GY
            unit_cell_width = 1 / p.GX
            unit_cell_height = 1 / p.GY
            current_bb = [current_box_column_index * unit_cell_width,
                                     (current_box_column_index + 1) * unit_cell_width,
                                     current_box_row_index * unit_cell_height,
                                     (current_box_row_index + 1) * unit_cell_height]
