import cv2
import six.moves.urllib as urllib
import tarfile
import os


CWD_PATH = os.path.dirname(os.path.realpath(__file__))

# Path to frozen detection graph. This is the actual model that is used for the object detection.
# download from https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md
MODEL_NAME = 'ssd_mobilenet_v2_coco_2018_03_29'
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017' #fast
#MODEL_NAME = 'faster_rcnn_resnet101_kitti_2018_01_28'
#MODEL_NAME = 'faster_rcnn_resnet101_coco_11_06_2017' #medium speed
#MODEL_NAME = 'faster_rcnn_nas_coco_2018_01_28'
#MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'

MODEL_FILE = MODEL_NAME + '.tar.gz'
PATH_TO_MODELS =os.path.join(CWD_PATH, "model")
PATH_TO_CKPT = os.path.join(PATH_TO_MODELS, MODEL_NAME, 'frozen_inference_graph.pb')
PATH_TO_PBTXT = os.path.join(PATH_TO_MODELS, MODEL_NAME, 'graph.pbtxt')
PATH_TO_TGZ = os.path.join(PATH_TO_MODELS, MODEL_FILE)
NUM_CLASSES = 90


DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'
fileAlreadyExists = os.path.isfile(PATH_TO_CKPT)
if not fileAlreadyExists:
    if not os.path.exists(PATH_TO_MODELS):
        os.makedirs(PATH_TO_MODELS)
    download_url =DOWNLOAD_BASE + MODEL_FILE
    print('Downloading frozen inference graph: '+download_url)
    opener = urllib.request.URLopener()
    opener.retrieve(download_url, PATH_TO_TGZ)
    tar_file = tarfile.open(PATH_TO_TGZ)
    tar_file.extractall(path= PATH_TO_MODELS)



# Pretrained classes in the model
classNames = {0: 'background',
              1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
              7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
              13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
              18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
              24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
              32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
              37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
              41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
              46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
              51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
              56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
              61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
              67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
              75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
              80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
              86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}


def id_class_name(class_id, classes):
    for key, value in classes.items():
        if class_id == key:
            return value


# Loading model
model = cv2.dnn.readNetFromTensorflow(PATH_TO_CKPT, PATH_TO_PBTXT)
image = cv2.imread("image.jpeg")

image_height, image_width, _ = image.shape

model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))
output = model.forward()
# print(output[0,0,:,:].shape)


for detection in output[0, 0, :, :]:
    confidence = detection[2]
    if confidence > .5:
        class_id = detection[1]
        class_name=id_class_name(class_id,classNames)
        print(str(str(class_id) + " " + str(detection[2]) + " " + class_name))
        box_x = detection[3] * image_width
        box_y = detection[4] * image_height
        box_width = detection[5] * image_width
        box_height = detection[6] * image_height
        cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), (23, 230, 210), thickness=1)
        cv2.putText(image,class_name ,(int(box_x), int(box_y+.05*image_height)),cv2.FONT_HERSHEY_SIMPLEX,(.005*image_width),(0, 0, 255))





cv2.imshow('image', image)
# cv2.imwrite("image_box_text.jpg",image)

cv2.waitKey(0)
cv2.destroyAllWindows()