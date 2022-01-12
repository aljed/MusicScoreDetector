import random
import data
import os
import parameters as p
import importlib
import pickle
import numpy as np

importlib.reload(p)
importlib.reload(data)


def dump_data():
    random.seed()
    classes = data.retrieve_class_names()
    output_dim = p.GX * p.GY * (5 + len(classes))
    pages = data.Retriever().retrieve(classes)

    files = os.listdir(p.PNG_PATH)
    generator = data.Generator(pages, output_dim, classes).generator(files)
    i = 1

    e = [generator.__next__()]

    while True:
        if len(e) == 64:
            with open('data\\' + str(i / 64) + '.pkl', 'wb') as outp:
                print(i)
                random.shuffle(e)
                pickle.dump(e, outp, pickle.HIGHEST_PROTOCOL)
            e = []
        a = next(generator, None)
        if a is None:
            break
        e.append(a)
        i += 1

    with open('data\\' + str(i / 64) + '.pkl', 'wb') as outp2:
        random.shuffle(e)
        pickle.dump(e, outp2, pickle.HIGHEST_PROTOCOL)


def generate_data(data_dir_path, batch_size, output_size):
    files = os.listdir(data_dir_path)
    pad = []
    for file in files:
        with open(data_dir_path + '/' + file, 'rb') as data_file:
            part_data = pickle.load(data_file)
        part_data = pad + part_data
        pad_size = len(part_data) % batch_size
        batches_number = int(len(part_data) / batch_size)
        pad = part_data[len(part_data) - pad_size:]
        part_data = part_data[:len(part_data) - pad_size]
        for j in range(batches_number):
            batch = part_data[j * batch_size:(j + 1) * batch_size]
            yield (np.reshape(np.array([i for i, j in batch]), (batch_size, p.X, p.Y, 3)),
                   np.reshape(np.array([j for i, j in batch]), (batch_size, output_size)))

classes = data.retrieve_class_names()
output_dim = p.GX * p.GY * (5 + len(classes))

a = generate_data('data', 8, output_dim ).__next__()
b = generate_data('data', 8, output_dim).__next__()

comparison = a[0][0] == b[0][0]
equal_arrays = comparison.all()

print(equal_arrays)