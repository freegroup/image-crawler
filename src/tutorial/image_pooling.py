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

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

image = x_train[0]
image = image.reshape((28, 28))

# Max-Pooling Funktion definieren und auf ein Bild aus dem
# MNIST Dataset anwenden.
# 2x2, max
def max_pooling(image):
    rows, cols = image.shape
    c = np.zeros(shape=(rows//2, cols//2), dtype=np.int32)
    for i in range(0,rows,2):
        for n in range(0,cols,2):
            c[i//2][n//2] = np.max(image[i:i+1, n:n+1])

    return c

pooling_image = max_pooling(image)

print(image.shape)
print(pooling_image.shape)

# Input und Outputbild des Pooling Layers mit imshow() ausgeben
plt.imshow(image, cmap="gray")
plt.show()

plt.imshow(pooling_image, cmap="gray")
plt.show()