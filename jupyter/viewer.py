import matplotlib.pyplot as plt
import matplotlib.patches as patches


def show_prediction(y, x):

    def extract_bb(y):
        return y[:5]

    def show_bb(bb, x):
        fig, ax = plt.subplots()
        ax.imshow(x)
        rect = patches.Rectangle((bb[1], bb[3]), bb[0] - bb[1], bb[2] - bb[3], linewidth=1,
                                 edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        plt.draw()

    show_bb(extract_bb(y), x)
