# Imports
import tensorflow as tf
import numpy as np
import os
from os import makedirs
from os.path import exists, join
from keras.datasets import mnist
import time
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV

from keras.wrappers.scikit_learn import KerasClassifier
from keras.layers import *
from keras.activations import *
from keras.models import *
from keras.optimizers import *
from keras.initializers import *
from keras.utils.np_utils import to_categorical
from keras.callbacks import *

from plotting import *
from cifar10Data import *

# Load MNIST dataset
data = CIFAR10()
x_train, y_train = data.x_train, data.y_train
x_test, y_test = data.x_test, data.y_test
x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.2)

lr = 1e-3
optimizer = Adam
batch_size = 128
epochs = 10
train_size, width, height, depth = x_train.shape
test_size, num_classes = y_test.shape


# Define the DNN
def create_model(optimizer, lr):

    input_img = Input(shape=(width, height, depth))

    x = Conv2D(filters=32, kernel_size=3, padding='same')(input_img)
    x = Activation("relu")(x)
    x = Conv2D(filters=64, kernel_size=3, padding='same')(x)
    x = Activation("relu")(x)
    x = MaxPool2D()(x)

    x = Conv2D(filters=64, kernel_size=3, padding='same')(x)
    x = Activation("relu")(x)

    x = Conv2D(filters=32, kernel_size=3, padding='same')(x)
    x = Activation("relu")(x)
    x = Conv2D(filters=64, kernel_size=3, padding='same')(x)
    x = Activation("relu")(x)

    x = Flatten()(x)

    x = Dense(128)(x)
    x = Activation("relu")(x)
    x = Dense(num_classes)(x)
    output_pred = Activation("softmax")(x)

    optimizer = optimizer(lr=lr)
    model = Model(inputs=input_img, outputs=output_pred)
    model.compile(
        loss="categorical_crossentropy", 
        optimizer=optimizer, 
        metrics=["accuracy"])
    model.summary()
    return model

model = create_model(optimizer, lr)

model.fit(
    x=x_train, 
    y=y_train, 
    verbose=1, 
    batch_size=batch_size, 
    epochs=epochs, 
    validation_data=(x_valid, y_valid))

# Test the DNN
score = model.evaluate(x_test, y_test, batch_size=batch_size)
print("Test performance: ", score)