import tensorflow as tf
import numpy as np
import os
from keras.datasets import mnist
from sklearn.model_selection import train_test_split

from keras.layers import *
from keras.activations import *
from keras.models import *
from keras.optimizers import *
from keras.initializers import *
from keras.utils.np_utils import to_categorical
from keras.callbacks import *

from plotting import *
from mnistData import *


# Save Path
dir_path = "/Users/d023280/Documents/workspace/image-crawler/mnist/data"
log_dir = "/Users/d023280/Documents/workspace/image-crawler/mnist/log"


data = MNIST()
data.data_augmentation(augment_size=5000)

x_train, y_train = data.x_train, data.y_train
x_test, y_test = data.x_test, data.y_test

# Aufsplittung in ein ValidationSet und TrainSet auf Basis des train sets
x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.2)


width = 28
height = 28
depth = 1
num_classes = 10
epochs = 10

# Define the DNN
input_img = Input(shape=(width, height, depth))

x = Conv2D(filters=16, kernel_size=3, padding='same')(input_img)
x = Activation("relu")(x)
x = Conv2D(filters=32, kernel_size=3, padding='same')(x)
x = Activation("relu")(x)
x = MaxPool2D()(x)

x = Conv2D(filters=32, kernel_size=3, padding='same')(x)
x = Activation("relu")(x)
x = Conv2D(filters=64, kernel_size=3, padding='same')(x)
x = Activation("relu")(x)
x = MaxPool2D()(x)

x = Flatten()(x)

x = Dense(64)(x)
x = Activation("relu")(x)
x = Dense(num_classes)(x)
output_pred = Activation("softmax")(x)

model = Model(inputs=[input_img], outputs=[output_pred])

model.summary()

# Train the DNN
lr = 5e-4
optimizer = RMSprop(lr=lr)

model.compile(
    loss="categorical_crossentropy",
    optimizer=optimizer,
    metrics=["accuracy"])

tb = TensorBoard(log_dir=log_dir,
                 histogram_freq=0)

model.fit(
    x=x_train,
    y=y_train,
    verbose=1,
    batch_size=64,
    epochs=epochs,
    validation_data=[x_valid, y_valid],
    callbacks=[tb])

# Test the DNN
score = model.evaluate(x_test, y_test)
print("Score: ", score)

