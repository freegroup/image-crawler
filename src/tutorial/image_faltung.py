# Imports
import tensorflow as tf
import numpy as np
import os
from keras.datasets import mnist
import matplotlib.pyplot as plt

from keras.layers import *
from keras.activations import *
from keras.models import *
from keras.optimizers import *
from keras.initializers import *
from keras.utils.np_utils import to_categorical

np.random.seed(42)

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

image = x_train[0]
image = image.reshape((28, 28))

kernel = np.random.uniform(low=0.0, high=1.0, size=(2,2))

# Stride (1,1)
# Conv Funktion definieren und anschließend plotten
def conv2D(image, kernel):
    rows, cols = image.shape
    image = np.pad(image, [(1, 1), (1, 1)], mode='constant', constant_values=0)
    c = np.zeros_like(image, dtype=np.int32)
    for i in range(rows):
        for n in range(cols):
            c[i+1][n+1] = np.sum(kernel * image[i:i+2, n:n+2])

    return c[1:-1, 1:-1]

conv_image = conv2D(image, kernel)

# Input und Outputbild des Pooling Layers mit imshow() ausgeben
plt.imshow(image, cmap="gray")
plt.show()

plt.imshow(conv_image, cmap="gray")
plt.show()