import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import os
import random


OUT = 'marks.txt'


def is_marked(file):
    with open(OUT, "r") as a_file:
        for line in a_file:
            stripped_line = line.strip()
            if stripped_line.startswith(file):
                return True
        return False


class Marker:
    def __init__(self):
        self.sx = 0
        self.sy = 0
        self.nx = 0
        self.ny = 0
        self.coords = []
        self.rectangles = []
        self.files = os.listdir('pictures_resized')
        random.shuffle(self.files)
        self.it = iter(self.files)
        while True:
            self.current_photo = next(self.it)
            if not (is_marked(self.current_photo)):
                break
        if self.current_photo == '':
            print('You\'ve provided no pictures!')
        else:
            self.image = mpimg.imread('pictures_resized' + '\\' + self.current_photo)
            self.fig, self.ax = plt.subplots()
            self.shown = self.ax.imshow(self.image)
            self.fig.canvas.mpl_connect('button_press_event', self.onclick)
            self.fig.canvas.mpl_connect('button_release_event', self.onrelease)
            self.fig.canvas.mpl_connect('key_press_event', self.onnextphoto)
            plt.show()

    def save_coordinates(self):
        with open(OUT, 'a') as f:
            f.write(f'{self.current_photo}')
            for r in self.coords:
                f.write(f';{r[0]};{r[1]};{r[2]};{r[3]}')
            f.write('\n')
            self.coords = []

    def onclick(self, event):
        if event.button == 3 and event.ydata is not None:
            self.ny = (round(event.ydata))
            self.nx = (round(event.xdata))

    def onrelease(self, event):
        if event.button == 3 and event.ydata is not None:
            self.sy = (round(event.ydata))
            self.sx = (round(event.xdata))
            rect = patches.Rectangle((self.nx, self.ny), self.sx - self.nx, self.sy - self.ny, linewidth=1,
                                     edgecolor='r', facecolor='none')
            self.coords.append((self.sx, self.sy, self.nx, self.ny))
            self.rectangles.append(rect)
            self.ax.add_patch(rect)
            self.fig.canvas.draw_idle()

    def onnextphoto(self, event):
        if event.key == 'enter':
            self.save_coordinates()
            while True:
                self.current_photo = next(self.it)
                if not(is_marked(self.current_photo)):
                    break
            if self.current_photo != '':
                for r in self.rectangles:
                    r.remove()
                self.rectangles = []
                next_im = mpimg.imread('pictures_resized' + '\\' + self.current_photo)
                self.shown.set_data(next_im)
                plt.draw()
            else:
                print("All images have been processed")
                plt.close()
            plt.autoscale()
        elif event.key == 'escape':
            plt.close()
        elif event.key == '2':
            v = plt.axis()
            plt.axis([v[0], v[1], v[2] + 30, v[3] + 30])
            plt.draw()
        elif event.key == '8':
            v = plt.axis()
            plt.axis([v[0], v[1], v[2] - 30, v[3] - 30])
            plt.draw()
        elif event.key == '6':
            v = plt.axis()
            plt.axis([v[0] + 30, v[1] + 30, v[2], v[3]])
            plt.draw()
        elif event.key == '4':
            v = plt.axis()
            plt.axis([v[0] - 30, v[1] - 30, v[2], v[3]])
            plt.draw()


Marker()
