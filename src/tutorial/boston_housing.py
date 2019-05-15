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


from plotting import *

(x_train, y_train), (x_test, y_test) = mnist.load_data()

num_features = 784
num_classes = 10
train_size, test_size = x_train.shape[0], x_test.shape[0]

x_train = x_train.reshape(train_size, num_features)
x_test = x_test.reshape(test_size, num_features)
y_train = to_categorical(y_train, num_classes=num_classes)
y_test = to_categorical(y_test, num_classes=num_classes)


init_w = TruncatedNormal(mean=0.0, stddev =0.05)
init_b = Constant(value=0.05)


# define the DNN
model = Sequential()

model.add(Dense(500, kernel_initializer=init_w, bias_initializer= init_b, input_shape=(num_features,)))
model.add(Activation("relu"))

model.add(Dense(300, kernel_initializer=init_w, bias_initializer= init_b))
model.add(Activation("relu"))

model.add(Dense(100, kernel_initializer=init_w, bias_initializer= init_b))
model.add(Activation("relu"))

model.add(Dense(num_classes, kernel_initializer=init_w, bias_initializer= init_b,))
model.add(Activation("softmax"))

model.summary()


lr = 0.0005
optimizer = RMSprop(lr=lr) # Adam(lr=lr)

model.compile(
    loss ="categorical_crossentropy",
    optimizer=optimizer,
    metrics=["accuracy"]
)

model.fit(
    x=x_train,
    y=y_train,
    verbose=1,
    batch_size=128,
    epochs=15,
    validation_data=[x_test, y_test]
)

score = model.evaluate(x_test, y_test)
print(score)

