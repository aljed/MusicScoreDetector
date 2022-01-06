import random

import tensorflow as tf
import matplotlib.image as mpimg
import numpy as np

from tensorflow.keras import layers, models

from viewer import Viewer

LABELS_DIM = 5


class StaffPositionModel:

    def __init__(self, path=''):
        model = self.create_model()
        if path == '':
            labels, images = self.get_data()

            c = list(zip(labels, images))
            random.shuffle(c)
            labels, images = zip(*c)

            labels = np.asarray(labels)
            images = np.asarray(images)

            history = model.fit(images[:800], labels[:800], epochs=20, validation_data=(images[800:], labels[800:]))
            # plt.plot(history.history['accuracy'], label='accuracy')
            # plt.plot(history.history['val_accuracy'], label='val_accuracy')
            # plt.xlabel('Epoch')
            # plt.ylabel('Accuracy')
            # plt.ylim([0.5, 1])
            # plt.legend(loc='lower right')
            # plt.show()

            img = (np.expand_dims(images[900], 0))
            print(model.predict(img))
            print(labels[900])

            model.save_weights("five")
        else:
            model.load_weights(path)

        self.model = model

    def get_data(self):
        labels = np.empty([1090, 5])
        data = []
        with open('labels.txt', 'r') as f:
            for i, line in enumerate(f):
                attributes = line.split(';')
                im_labels = list(map(lambda y: int(y), attributes[2:7]))
                for j in range(len(im_labels), LABELS_DIM):
                    im_labels.append(0)
                values_num = int(attributes[1])
                #concatenated = np.concatenate((im_labels, np.ones(values_num), np.zeros(LABELS_DIM - values_num)))
                concatenated = im_labels
                for k in range(0, 10):
                    labels[i * 10 + k] = concatenated
                image = mpimg.imread('pictures_resized' + '\\' + attributes[0])
                image = image / 255
                # image = image[0:1186, 500:550]
                for k in range(0, 10):
                    data.append(image[0:1186, 150 + k * 50:200 + k * 50])
                # data.append(image)

        return labels, np.array(data)

    def create_model(self):
        model = models.Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(1186, 50, 3)))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(LABELS_DIM))
        model.compile(optimizer='adam',
                      loss=self.loss_fun,
                      metrics=['accuracy'],
                      run_eagerly=True)
        return model

    def loss_fun(self, r, p):
        # r_values, r_map = tf.split(r, 2, 1)
        # p_values, p_map = tf.split(p, 2, 1)
        return tf.math.square(r - p) #+ tf.math.square(r_map - p_map)*20


staff_pos = StaffPositionModel()
viewer = Viewer(staff_pos.model)

