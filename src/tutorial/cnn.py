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
dir_path = "/Users/d023280/Documents/workspace/image-crawler/mnist/data"
log_dir = "/Users/d023280/Documents/workspace/image-crawler/mnist/log"

(x_train, y_train), (x_test, y_test) = mnist.load_data() #28x28x1
width = 28
height = 28
depth = 1
num_classes = 10
train_size, test_size = x_train.shape[0], x_test.shape[0]
epochs = 20

x_train = x_train.reshape(train_size, width, height, depth)
y_train = to_categorical(y_train, num_classes=num_classes)

x_test = x_test.reshape(test_size, width, height, depth)
y_test = to_categorical(y_test, num_classes=num_classes)


# Define the DNN
model = Sequential()

model.add(Conv2D(filters=32, kernel_size=3, strides=1, padding='same', input_shape=(width, height, depth)))
model.add(Activation("relu"))
model.add(MaxPool2D())

model.add(Flatten())

model.add(Dense(64))
model.add(Activation("relu"))
model.add(Dense(num_classes))
model.add(Activation("softmax"))

model.summary()

# Train the DNN
lr = 5e-4
optimizer = RMSprop(lr=lr)

model.compile(
    loss="categorical_crossentropy",
    optimizer=optimizer,
    metrics=["accuracy"])

tb = TensorBoard(
    log_dir=log_dir,
    histogram_freq=0)

model.fit(
     x=x_train,
     y=y_train,
     verbose=1,
     batch_size=64,
     epochs=epochs,
     validation_data=[x_test, y_test],
     callbacks=[tb])

# # Test the DNN
score = model.evaluate(x_test, y_test)
print("Score: ", score)