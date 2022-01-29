from dataclasses import dataclass
import numpy as np
import imageio as im
import score_structure.parameters as p
import tensorflow as tf
from PIL import Image
import json


@dataclass
class BoundingBox:
    xmin: float
    xmax: float
    ymin: float
    ymax: float

    def get_area(self):
        return (self.xmax - self.xmin) * (self.ymax - self.ymin)

    def common_area(self, pos):  # returns None if rectangles don't intersect
        dx = min(self.xmax, pos.xmax) - max(self.xmin, pos.xmin)
        dy = min(self.ymax, pos.ymax) - max(self.ymin, pos.ymin)
        if (dx >= 0) and (dy >= 0):
            return dx * dy
        else:
            return 0

    def is_within(self, bb):
        return bb.xmin <= self.xmin and bb.xmax >= self.xmax and bb.ymin <= self.ymin and bb.ymax >= self.ymax

    def is_point_within(self, x, y):
        return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax

    def get_normalized(self, x, y):
        return BoundingBox(self.xmin / x, self.xmax / x, self.ymin / y, self.ymax / y)

    def get_relative_bb2(self, new_bb): # mam koordynaty w całym obrazku ale chcę w podanym wycinku
        return BoundingBox((self.xmin - new_bb.xmin) / (new_bb.xmax - new_bb.xmin),
                           (self.xmax - new_bb.xmin) / (new_bb.xmax - new_bb.xmin),
                           (self.ymin - new_bb.ymin) / (new_bb.ymax - new_bb.ymin),
                           (self.ymax - new_bb.ymin) / (new_bb.ymax - new_bb.ymin))

    def get_relative_bb(self, new_bb):
        return BoundingBox(new_bb.xmin + (new_bb.xmax - new_bb.xmin) * self.xmin,
                           new_bb.xmin + (new_bb.xmax - new_bb.xmin) * self.xmax,
                           new_bb.ymin + (new_bb.ymax - new_bb.ymin) * self.ymin,
                           new_bb.ymin + (new_bb.ymax - new_bb.ymin) * self.ymax)


@dataclass
class Element:
    typ: str
    bounding_box: BoundingBox


@dataclass
class Data:
    img: list
    elements: list
    bb: BoundingBox
    page_Y: int
    page_X: int


class TFRecordGenerator:

    def __init__(self, pages, classes, params: p.Params) -> None:
        self.pages = pages
        self.classes = {c: i for i, c in enumerate(classes)}
        self.params = params

    def generate_example(self, number, filename, number_in_file, data):

        resultant_filename = filename + str(number_in_file)

        relative_bbs = [e.bounding_box.get_relative_bb2(data.bb) for e in data.elements]

        xmins = [e.xmin for e in relative_bbs]
        xmaxs = [e.xmax for e in relative_bbs]
        ymins = [e.ymin for e in relative_bbs]
        ymaxs = [e.ymax for e in relative_bbs]
        types = [e.typ.encode("utf-8") for e in data.elements]
        labels = [self.classes[e.typ] + 1 for e in data.elements]

        import io

        def image_to_byte_array(image:Image):
            imgByteArr = io.BytesIO()
            image.save(imgByteArr, format="png")
            imgByteArr = imgByteArr.getvalue()
            return imgByteArr

        example = tf.train.Example(features=tf.train.Features(feature={
            "image/height": tf.train.Feature(int64_list=tf.train.Int64List(value=[self.params.Y])),
            "image/width": tf.train.Feature(int64_list=tf.train.Int64List(value=[self.params.X])),
            "image/filename": tf.train.Feature(bytes_list=tf.train.BytesList(
                value=[resultant_filename.encode("utf-8")])),
            "image/source_id": tf.train.Feature(bytes_list=tf.train.BytesList(value=[str(number).encode("utf-8")])),
            "image/key/sha256": tf.train.Feature(bytes_list=tf.train.BytesList(value=[resultant_filename.encode("utf-8")])),
            "image/encoded": tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_to_byte_array(Image.fromarray(data.img))])),
            "image/format": tf.train.Feature(bytes_list=tf.train.BytesList(value=["png".encode("utf8")])),
            "image/object/bbox/xmin": tf.train.Feature(float_list=tf.train.FloatList(value=xmins)),
            "image/object/bbox/xmax": tf.train.Feature(float_list=tf.train.FloatList(value=xmaxs)),
            "image/object/bbox/ymin": tf.train.Feature(float_list=tf.train.FloatList(value=ymins)),
            "image/object/bbox/ymax": tf.train.Feature(float_list=tf.train.FloatList(value=ymaxs)),
            "image/object/class/text": tf.train.Feature(bytes_list=tf.train.BytesList(value=types)),
            "image/object/class/label": tf.train.Feature(int64_list=tf.train.Int64List(value=labels)),
            "image/object/difficult": tf.train.Feature(int64_list=tf.train.Int64List(value=np.zeros(np.shape(labels), dtype=np.int).tolist())),
            "image/object/truncated": tf.train.Feature(int64_list=tf.train.Int64List(value=np.zeros(np.shape(labels), dtype=np.int).tolist())),
            "image/object/view": tf.train.Feature(bytes_list=tf.train.BytesList(
                 value=np.full(np.shape(labels), "Unspecified".encode("utf-8")).tolist())),
        }))

        return example

    def generate_records(self, files, output_path):

        def save_record(serialized_examples, index: int):
            tf_writer = tf.io.TFRecordWriter((output_path + '/' + 'record' + str(index)).encode("utf-8"))
            for serialized_examples in serialized_examples:
                tf_writer.write(serialized_examples)
            tf_writer.close()

        examples = []
        example_number = 0
        record_number = 0

        files = self.pages.keys()

        for file in files:

            file_used = False

            while True:

                if len(examples) < self.params.RECORDS_TO_SAVE and file_used is False:
                    file_used = True
                    if not isinstance(file, str):
                        file = file.decode("utf-8")
                    records_new = split_image(file, self.pages[file], self.params.PNG_PATH)
                    example_in_file_number = 0
                    for d in records_new:
                        examples.append(self.generate_example(
                            example_number, file, example_in_file_number, d))
                        example_number += 1
                        example_in_file_number += 1

                if len(examples) >= self.params.RECORDS_TO_SAVE:
                    elements_to_yield = examples[0:self.params.RECORDS_TO_SAVE]
                    elements_to_yield = [e.SerializeToString() for e in elements_to_yield]


                    if len(examples) > self.params.RECORDS_TO_SAVE:
                        examples = examples[self.params.RECORDS_TO_SAVE:]
                    else:
                        examples = []

                    save_record(elements_to_yield, record_number)
                    record_number += 1
                else:
                    break


class Page:

    def __init__(self, name):
        self.name = name
        self.elements = []

    def add(self, element):
        self.elements.append(element)

    def retrieve_from_box(self, bb):
        filtered = []
        for e in self.elements:
            if e.bounding_box.is_within(bb):
                filtered.append(e)
        return filtered


def retrieve(json_path, classes=None):
    file = open(json_path, "r")
    json_string = json.load(file)
    categories = json_string['categories']
    categories = {idx: value['name'] for idx, value in categories.items() if value['annotation_set'] == 'deepscores'}
    images = json_string['images']
    annotations = json_string['annotations'].values()
    pages = {}
    num_of_files = len(images)
    counter = 0
    for image in images:
        counter += 1
        if counter % 100 == 0:
            print(
                f'{round(counter * 100 / num_of_files)}% of the files processed, '
                f'we are at {counter} in {num_of_files}.')
        id = image['id']
        width = image['width']
        height = image['height']
        page = Page(id)
        picture_annotations = [a for a in annotations if a['img_id'] == str(id)]
        elements = []
        for value in picture_annotations:
            category_name = categories[value['cat_id'][0]]
            a_bbox = value['a_bbox']
            if classes and category_name in classes or not classes:
                elements.append(Element(category_name,
                                        BoundingBox(a_bbox[0] / width, a_bbox[2] / width, a_bbox[1] / height, a_bbox[3] / height)))
        for e in elements:
            page.add(e)
        pages[image['filename']] = page
    return pages


#print(retrieve('E:\Downloads\ds2_dense\deepscores_train.json')[0])


@dataclass
class PartData:
    slice: list
    bb: BoundingBox


def split_image(filename, page: Page, png_path) -> list:  # of Data
    image = np.array(im.imread(png_path + '/' + filename))
    shape = np.shape(image)
    max_y = shape[0] - p.Y
    max_x = shape[1] - p.X
    parts = []

    ymin = 0
    yend = False
    while not yend:
        if ymin == max_y:
            yend = True
        xmin = 0
        xend = False
        while not xend:
            if xmin == max_x:
                xend = True
            img_slice = image[ymin:ymin + p.Y, xmin:xmin + p.X, 0:3]
            parts.append(PartData(img_slice,
                                  BoundingBox(xmin / shape[1], (xmin + p.X) / shape[1], ymin / shape[0],
                                              (ymin + p.Y) / shape[0])))
            xmin += p.Y
            if xmin > max_x:
                xmin = max_x
        ymin += p.Y
        if ymin > max_y:
            ymin = max_y

    data_from_page = [Data(s.slice, page.retrieve_from_box(s.bb), s.bb, shape[0], shape[1]) for s in parts]

    return data_from_page


def retrieve_class_names(classes):
    counter = 0
    names = {}

    for index in classes:
        names[index] = counter
        counter += 1

    return names
