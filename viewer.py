import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os

OUT = 'labels.txt'


class Viewer:
    def __init__(self, model):
        self.model = model

        self.files = os.listdir('pictures_resized')
        self.it = iter(self.files)
        self.current_photo = next(self.it, '')
        if self.current_photo == '':
            print('You\'ve provided no pictures!')
        else:
            self.image = mpimg.imread('pictures_resized' + '\\' + self.current_photo)
            fig, ax = plt.subplots()
            self.shown = ax.imshow(self.image)
            fig.canvas.mpl_connect('key_press_event', self.onnextphoto)
            plt.show()

    def draw_lines(self, im):
        im_cut = im[0:1186, 300:350]
        img = (np.expand_dims(im_cut, 0))
        pred = self.model.predict(img)
        print(pred)
        copied = np.copy(im)
        for k in pred[0]:
            m = k / 100
            if m > 1186:
                break
            for i in range(0, 840):
                for j in range(0, 3):
                    copied[round(m)][i][j] = 0
        return copied

    def onnextphoto(self, event):
        if event.key == 'enter':
            self.current_photo = next(self.it)
            if self.current_photo != '':
                next_im = mpimg.imread('pictures_resized' + '\\' + self.current_photo)
                next_im = self.draw_lines(next_im)
                self.shown.set_data(next_im)
                plt.draw()
            else:
                print("All images have been processed")
                plt.close()
        elif event.key == 'escape':
            plt.close()
