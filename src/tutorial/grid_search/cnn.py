import tensorflow as tf
import numpy as np
import os
from keras.datasets import mnist
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from keras.wrappers.scikit_learn import KerasClassifier
 
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
dir_path = "C:/Users/jan/Dropbox/_Programmieren/Udemy Tensorflow Kurs"
log_dir = "C:/Users/Jan/Documents/logs/mnist/"

data = MNIST()
data.data_augmentation(augment_size=5000)
x_train, y_train = data.x_train, data.y_train
x_test, y_test = data.x_test, data.y_test
x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.2)

width = 28
height = 28
depth = 1
num_classes = 10

epochs = 10
batch_size = 128

# Define the DNN
def create_model(optimizer, lr):
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
    optimizer = optimizer(lr=lr)
    model.compile(
        loss="categorical_crossentropy",
        optimizer=optimizer,
        metrics=["accuracy"])
    return model

model = KerasClassifier(
    build_fn=create_model,
    epochs=epochs,
    batch_size=batch_size,
    verbose=1)

optimizer_candidates = [Adam, RMSprop]
lr_candidates = [1e-3, 5e-3, 1e-4]

param_grid = {
    "optimizer": optimizer_candidates,
    "lr": lr_candidates}

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