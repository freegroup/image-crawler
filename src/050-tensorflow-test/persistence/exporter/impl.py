import os, tensorflow as tf
from PIL import Image
import os
import shutil

from configuration import Configuration
conf = Configuration()


class ExportToFolderWorker():
    def __init__(self):
        self.__dir = conf.exporter("dir")

        # cleanup and recreate the export directory
        if os.path.exists(self.__dir):
            shutil.rmtree(self.__dir)
        os.makedirs(self.__dir)
        self.__writer = tf.python_io.TFRecordWriter(os.path.join(self.__dir, "dataset.tfrecords"))

    def write(self, image_meta):
        md5 = image_meta["md5"]
        labels = image_meta["labels"]

        if len(labels) is not 0:
            img = image_meta["image"]
            format = b'jpg'  #image_meta["format"]

            filename = str.encode(md5)  # Filename of the image. Empty if image is not from file

            height = img.height
            width = img.width

            image_data = img.tobytes()  # tf.gfile.FastGFile(imgfile,'rb').read()

            xmins = []  # List of normalized left x coordinates in bounding box (1 per box)
            xmaxs = []  # List of normalized right x coordinates in bounding box (1 per box)
            ymins = []  # List of normalized top y coordinates in bounding box (1 per box)
            ymaxs = []  # List of normalized bottom y coordinates in bounding box (1 per box)
            classes_text = []  # List of string class name of bounding box (1 per box)
            classes_int = []  # List of integer class id of bounding box (1 per box)


            for label in labels:
                text = label["text"]
                x1 = label["x"]
                y1 = label["y"]
                x2 = x1 + label["width"]
                y2 = y1 + label["height"]

                xmins.append(float(x1)/width)
                xmaxs.append(float(x2)/width)
                ymins.append(float(y1)/height)
                ymaxs.append(float(y2)/height)

                classes_text.append(str.encode(text))
                classes_int.append(1)

            print(filename, height, width, xmins, xmaxs, ymins, ymaxs, classes_text, classes_int)

            tf_example = tf.train.Example(features = tf.train.Features(feature={
                'image/height': int64_feature(height),
                'image/width': int64_feature(width),
                'image/filename': bytes_feature(filename),
                'image/source_id': bytes_feature(filename),
                'image/encoded': bytes_feature(image_data),
                'image/format': bytes_feature(format),
                'image/object/bbox/xmin': float_list_feature(xmins),
                'image/object/bbox/xmax': float_list_feature(xmaxs),
                'image/object/bbox/ymin': float_list_feature(ymins),
                'image/object/bbox/ymax': float_list_feature(ymaxs),
                'image/object/class/text': bytes_list_feature(classes_text),
                'image/object/class/label': int64_list_feature(classes_int),
            }))
            self.__writer.write(tf_example.SerializeToString())
            print("   added image")
        else:
            print("   skipped image because of missing labels")

    def close(self):
        self.__writer.close()


def int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def int64_list_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def bytes_list_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))


def float_list_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))

