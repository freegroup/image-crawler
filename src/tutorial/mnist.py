from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import numpy as np
import os

from keras.datasets import boston_housing
from keras.layers import *
from keras.activations import *
from keras.models import *
from keras.optimizers import *
from keras.initializers import *
from keras.utils.np_utils import to_categorical


from plotting import *

(x_train, y_train), (x_test, y_test) = boston_housing.load_data()

num_features = 13
train_size, test_size = x_train.shape[0], x_test.shape[0]

init_w = RandomUniform(minval=-1.0, maxval = 1.0)
init_b = Constant(value=0.0)


# define the DNN
model = Sequential()
model.add(Dense(16, kernel_initializer=init_w, bias_initializer= init_b, input_shape=(num_features,)))
model.add(Activation("relu"))
model.add(Dense(1, kernel_initializer=init_w, bias_initializer= init_b,))
model.summary()



def r_squared(y_true, y_pred):
    numerator = tf.reduce_mean(tf.square(tf.subtract(y_true, y_pred)))
    denominator = tf.reduce_mean(tf.square(tf.subtract(y_true, tf.reduce_mean(y_true))))
    r2 = tf.clip_by_value(tf.subtract(1.0, tf.div(numerator, denominator)), clip_value_min=0.0, clip_value_max=1.0)
    return r2


lr = 0.005
optimizer = Adam(lr=lr)

model.compile(
    loss ="mse",
    optimizer=optimizer,
    metrics=[r_squared]
)

model.fit(
    x=x_train,
    y=y_train,
    verbose=1,
    batch_size=128,
    epochs=2000,
    validation_data=[x_test, y_test]
)

score = model.evaluate(x_test, y_test)
print(score)

