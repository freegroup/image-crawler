# Imports
import tensorflow as tf
import numpy as np
import os
from os import makedirs
from os.path import exists, join
from keras.datasets import mnist
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from keras.wrappers.scikit_learn import KerasClassifier


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

log_dir = "C:/Users/Jan/Documents/logs/cifar10/"

# Load MNIST dataset
data = CIFAR10()
x_train, y_train = data.x_train, data.y_train
x_test, y_test = data.x_test, data.y_test
x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.2)

batch_size = 128
epochs = 10
train_size, width, height, depth = x_train.shape
test_size, num_classes = y_test.shape
width, height, depth = x_train.shape[1:]

tb = TensorBoard(
    log_dir=log_dir,
    histogram_freq=0)

# Define the DNN
def create_model(lr,optimizer,  conv_blocks, dense_layer, dense_units):
    input_img = Input(shape=(width, height, depth))

    x = Conv2D(filters=16, kernel_size=3, padding="same")(input_img)
    x = Activation("relu")(x)
    x = MaxPool2D()(x)

    for c in range(conv_blocks-1):
        x = Conv2D(filters=16, kernel_size=3, padding="same")(x)
        x = Activation("relu")(x)
        x = MaxPool2D()(x)

    x = Flatten()(x)

    for d in range(dense_layer):
        x = Dense(units=dense_units)(x)
        x = Activation("relu")(x)

    x = Dense(units=num_classes)(x)
    output_pred = Activation("softmax")(x)

    optimizer = optimizer(
        lr=lr)
    model = Model(
        inputs=input_img,
        outputs=output_pred)
    model.compile(
        loss="categorical_crossentropy",
        optimizer=optimizer,
        metrics=["accuracy"])
    model.summary()
    return model

model = KerasClassifier(
    build_fn=create_model,
    epochs=epochs,
    batch_size=batch_size,
    verbose=1)

optimizer_candidates = [Adam]
lr_candidates = [1e-3]
conv_blocks_candidates = [2, 3]
dense_layer_candidates = [1, 2]
dense_units_candidates = [256, 512]

param_grid = {
    "optimizer": optimizer_candidates,
    "lr": lr_candidates,
    "conv_blocks": conv_blocks_candidates,
    "dense_layer": dense_layer_candidates,
    "dense_units": dense_units_candidates}

grid = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    n_jobs=1,
    verbose=1,
    cv=3)

grid_result = grid.fit(x_train, y_train)

# Summary
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_["mean_test_score"]
stds = grid_result.cv_results_["std_test_score"]
params = grid_result.cv_results_["params"]

for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))

# model = create_model(optimizer, lr)

# model.fit(
#     x=x_train,
#     y=y_train,
#     verbose=1,
#     batch_size=batch_size,
#     epochs=epochs,
#     validation_data=(x_valid, y_valid),
#     callbacks=[tb])

# # Test the DNN
# score = model.evaluate(x_test, y_test, batch_size=batch_size)
# print("Test performance: ", score)