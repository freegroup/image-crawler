# Imports
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.image as mpimg

# Display the Digit from the image
# If the Label and PredLabel is given display it too
def display_digit(image, label=None, pred_label=None):
    if image.shape == (784,):
        image = image.reshape((28, 28))
    label = np.argmax(label, axis=0)
    if pred_label is None and label is not None:
        plt.title('Label: %d' % (label))
    elif label is not None:
        plt.title('Label: %d, Pred: %d' % (label, pred_label))

    plt.imshow(image, cmap=plt.get_cmap('gray_r'))
    plt.show()

# Display the convergence of the error while training
def display_convergence(error):
    plt.plot(error)
    plt.title('Error of the NN')
    plt.xlabel('Epoch')
    plt.ylabel('Error')
    plt.show()

# Plot confusion matrix
def plot_confusion_matrix(cm, classes, normalize=False,
                          title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')