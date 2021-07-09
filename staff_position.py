import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

OUT = 'labels.txt'


class StaffPositionMarker:
    def __init__(self):
        self.current_locations = []
        self.files = os.listdir('pictures_resized')
        self.it = iter(self.files)
        self.current_photo = next(self.it, '')
        if self.current_photo == '':
            print('You\'ve provided no pictures!')
        else:
            self.image = mpimg.imread('pictures_resized' + '\\' + self.current_photo)
            fig, ax = plt.subplots()
            self.shown = ax.imshow(self.image)
            fig.canvas.mpl_connect('button_press_event', self.onclick)
            fig.canvas.mpl_connect('key_press_event', self.onnextphoto)
            plt.show()

    def save_coordinates(self):
        f = open(OUT, 'a')
        f.write(self.current_photo)
        f.write(f';{len(self.current_locations)}')
        for location in self.current_locations:
            f.write(f';{location}')
        f.write('\n')
        f.close()

    def onclick(self, event):
        if event.button == 3 and event.ydata is not None:
            print(event.ydata)
            self.current_locations.append(round(event.ydata))


    def onnextphoto(self, event):
        if event.key == 'enter':
            self.save_coordinates()
            self.current_photo = next(self.it)
            if self.current_photo != '':
                self.current_locations = []
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


StaffPositionMarker()