import tensorflow as tf
import numpy as np
import os
from keras.datasets import mnist

from keras.layers import *
from keras.activations import *
from keras.models import *
from keras.optimizers import *
from keras.initializers import *
from keras.utils.np_utils import to_categorical
from keras.callbacks import *

from plotting import *

# Save Path

(x_train, y_train), (x_test, y_test) = mnist.load_data() #28x28x1
width = 28
height = 28
depth = 1
num_classes = 10
train_size, test_size = x_train.shape[0], x_test.shape[0]
epochs = 15

x_train = x_train.reshape(train_size, width, height, depth)
x_test = x_test.reshape(test_size, width, height, depth)
y_train = to_categorical(y_train, num_classes=num_classes)
y_test = to_categorical(y_test, num_classes=num_classes)

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


model.fit(
    x=x_train,
    y=y_train,
    verbose=1,
    batch_size=64,
    epochs=epochs,
    validation_data=[x_test, y_test])

# Test the DNN
score = model.evaluate(x_test, y_test)
print("Score: ", score)