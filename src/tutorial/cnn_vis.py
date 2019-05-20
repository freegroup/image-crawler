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
dir_path = "C:/Users/jan/Dropbox/_Programmieren/Udemy Tensorflow Kurs"
log_dir = "C:/Users/Jan/Documents/logs/mnist/"

(x_train, y_train), (x_test, y_test) = mnist.load_data() #28x28x1
width = 28
height = 28
depth = 1
num_classes = 10
train_size, test_size = x_train.shape[0], x_test.shape[0]
epochs = 10

x_train = x_train.reshape(train_size, width, height, depth)
x_test = x_test.reshape(test_size, width, height, depth)
y_train = to_categorical(y_train, num_classes=num_classes)
y_test = to_categorical(y_test, num_classes=num_classes)

# Define the DNN
model = Sequential()

model.add(Conv2D(filters=16, kernel_size=3, padding='same', input_shape=(width, height, depth)))
model.add(Activation("relu"))
model.add(Conv2D(filters=32, kernel_size=3, padding='same'))
model.add(Activation("relu"))
model.add(MaxPool2D())

model.add(Conv2D(filters=32, kernel_size=3, padding='same'))
model.add(Activation("relu"))
model.add(Conv2D(filters=64, kernel_size=3, padding='same'))
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

tb = TensorBoard(log_dir=log_dir,
                 histogram_freq=0)

model.fit(
    x=x_train,
    y=y_train,
    verbose=1,
    batch_size=64,
    epochs=epochs,
    validation_data=[x_test, y_test],
    callbacks=[tb])

# Test the DNN
score = model.evaluate(x_test, y_test)
print("Score: ", score)

# Plot weights
w = model.layers[0].get_weights()[0]
print(w.shape)

f, ax = plt.subplots(8, 2, figsize=(15,15))
ax = ax.reshape(16)

for depth in range(16):
    ax[depth].imshow(w[:,:,0,depth], cmap="gray")

ax = ax.reshape(8,2)
f.subplots_adjust(hspace=0.5)
plt.show()