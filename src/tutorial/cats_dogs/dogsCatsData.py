from keras.preprocessing.image import ImageDataGenerator
from keras.utils.np_utils import to_categorical
import numpy as np
import os
import glob
import cv2
from skimage import transform
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

dir_path = os.path.dirname(os.path.realpath(__file__))

file_dir = os.path.join(dir_path, "images")
img_size = 64
img_depth = 3
classes = 2

# Load Cats (0) and Dogs (1) from images to NumpyArray
def extract_cats_vs_dogs(file_dir):
    cats_dir = os.path.join(file_dir,"cats", "*.jpg")
    dogs_dir = os.path.join(file_dir,"dogs", "*.jpg")

    img_cats = glob.glob(cats_dir)
    img_dogs = glob.glob(dogs_dir)

    num_dogs = len(img_dogs)
    num_cats = len(img_cats)

    x = np.empty(
        shape=(num_cats+num_dogs, img_size, img_size, img_depth),
        dtype=np.float32
    )
    y = np.empty(
        shape=(num_cats+num_dogs),
        dtype=np.int8
    )
    cnt = 0
    for dog in img_dogs:
        try:
            img = cv2.imread(dog)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = transform.resize(img,(img_size, img_size, img_depth))
            x[cnt] = img
            y[cnt] = 1
            cnt += 1
        except:
            pass

    for cat in img_cats:
        try:
            img = cv2.imread(cat)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = transform.resize(img,(img_size, img_size, img_depth))
            x[cnt] = img
            y[cnt] = 0
            cnt += 1
        except:
            pass
    np.save(file_dir+"/x.npy",x)
    np.save(file_dir+"/y.npy",y)

def load_cats_vs_dogs(file_dir):
    x = np.load(file_dir+"/x.npy")
    y = np.load(file_dir+"/y.npy")

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    return (x_train, y_train), (x_test, y_test)

class DOGSCATS:
    def __init__(self, file_dir):
        self.width = 64
        self.height = 64
        self.depth = 3
        self.num_classes = 2
        (self.x_train, self.y_train), (self.x_test, self.y_test) = load_cats_vs_dogs(file_dir)
        self.train_size, self.test_size = self.x_train.shape[0], self.x_test.shape[0]
        # Reshape x data
        self.x_train = self.x_train.reshape(self.train_size, self.width, self.height, self.depth)
        self.x_test = self.x_test.reshape(self.test_size, self.width, self.height, self.depth)
        # Create one hot arrays
        self.y_train = to_categorical(self.y_train, num_classes=self.num_classes)
        self.y_test = to_categorical(self.y_test, num_classes=self.num_classes)
        # Change dtype from int to float
        self.x_train = self.x_train.astype("float32")
        self.x_test = self.x_test.astype("float32")
        # z-score Standardisierung
        mean = np.mean(self.x_train)
        stddev = np.std(self.x_train)
        self.x_train -= mean
        self.x_train /= stddev
        self.x_test -= mean
        self.x_test /= stddev

    def data_augmentation(self, augment_size=5000):
        image_generator = ImageDataGenerator(
            rotation_range=15.0,
            zoom_range=0.10,
            width_shift_range=0.10,
            height_shift_range=0.10)
        # fit data for augmenting
        image_generator.fit(self.x_train, augment=True)
        # get transformed images
        randidx = np.random.randint(self.train_size, size=augment_size)
        x_augmented = self.x_train[randidx].copy()
        x_copy = x_augmented.copy()
        y_augmented = self.y_train[randidx].copy()
        x_augmented = image_generator.flow(x_augmented, np.zeros(augment_size),
                                           batch_size=augment_size, shuffle=False).next()[0]
        # append augmented data to trainset
        self.x_train = np.concatenate((self.x_train, x_augmented))
        self.y_train = np.concatenate((self.y_train, y_augmented))
        self.train_size = self.x_train.shape[0]

if __name__ == "__main__":
    #extract_cats_vs_dogs(file_dir)

    (x_train, y_train), (x_test, y_test) = load_cats_vs_dogs(file_dir)
    print(type(y_train))
    for i in range(10):
        img = x_train[i]
        label = y_train[i]
        plt.imshow(img)
        plt.title("Class: "+ str(label))
        plt.show()
