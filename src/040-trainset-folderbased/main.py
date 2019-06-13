import os
from pydoc import locate

from configuration import Configuration


# Load the app configuration
#
dir_path = os.path.dirname(os.path.realpath(__file__))
conf = Configuration(inifile=os.path.join(dir_path, "config.ini"))


# read images and provide them in a JSON struct
#
ImageReaderWorker = locate(conf.impl_reader())
reader_worker = ImageReaderWorker()

# export the cropped regions in the related folders
#
ImageWriterWorker = locate(conf.impl_exporter())
writer_worker = ImageWriterWorker()

if __name__ == '__main__':
    for i in range(reader_worker.len()):
        image_meta = reader_worker.read(i)
        writer_worker.write(image_meta)
        print("cropped image "+str(i+1) + "/" + str(reader_worker.len()))
    writer_worker.close()
