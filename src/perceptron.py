from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import numpy as np

def dataset():
    x = np.array([[0,0],[0,1],[1,0],[1,1]])
    y = np.array([0,1,1,1])
    return x,y

class Perceptron():
    def __init__(self, epochs, lr):
        self.epochs = epochs
        self. w = []
        self.lr = lr


    def train (self, x,y):
        N, dim = x.shape
        self.w = np.random.uniform(-1,1, (dim, 1))


        # training
        error = 0.0
        for epoch in range(self.epochs):
            choice = np.random.choice(N) # pick random sample for dataset
            x_i = x[choice]
            y_i = y[choice]
            y_hat = self.predict(x_i)
            if y_hat != y_i:
                error +=1
                self.update_weights(x_i, y_i, y_hat)
        print("error", error)


    def update_weghts(self, x, y, y_hat):
        for i in range(self.w.shape[0]):
            delta_w_i = self.lr * (y -y_hat)*x[i]
            self.w[i] = self.w[i] + delta_w_i


    def predict(self, x):
        input_signal = self.w.T@x
        output_signal = self.activation(input_signal)
        return output_signal

    def activation(self, signal):
        return [1 if s>0 else 0 for s in signal]


x,y = dataset()

per = Perceptron(2,0.1)
per.train(x,y)
