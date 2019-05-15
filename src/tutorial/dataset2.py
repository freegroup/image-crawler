from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import numpy as np
import os

from plotting import *

# Save Path
dir_path = "/Users/d023280/Documents/workspace/image-crawler"

# Load Dataset
mnist = input_data.read_data_sets(dir_path+"/mnist_data/", one_hot=True)
train_size = mnist.train.num_examples 
test_size = mnist.test.num_examples 

print(train_size)
print(test_size)

x_train = mnist.train.images
y_train = mnist.train.labels

print(x_train.shape)
print(y_train.shape)

display_digit(x_train[2], label=y_train[2])

