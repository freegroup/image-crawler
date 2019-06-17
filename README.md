# Create Image Dataset for Machine Laerning

## Introduction
How to create a deep learning dataset using Bing Image Search

Deep learning algorithms, especially Convolutional Neural Networks, can be data hungry beasts.
And to make matters worse, manually annotating an image dataset can be a time consuming, tedious, 
and even expensive process.

So is there a way to leverage the power of **Bing Image Search** (different sources are possible) to 
quickly gather training images and thereby cut down on the time it takes to build your dataset.

## Overview
Alright, so a brief overview of the steps needed to do this:

 - Collect a few hundred images that contain your object - The bare minimum would be about 100, ideally more like 500+, but, the more images you have, the more tedious step 2 is...
 - Annotate/label the images, ideally with a program. I personally used LabelImg. This process is basically drawing boxes around your object(s) in an image. The label program automatically will create an XML file that describes the object(s) in the pictures.
 - Split this data into train/test samples
 - Generate TF Records from these splits
 - Setup a .config file for the model of choice (you could train your own from scratch, but we'll be using transfer learning)
 - Train
 - Export graph from new trained model
 - Detect custom objects in real time!
 - Profit!

## Quick Start Guide
Open terminal and activate your Python environment (it needs to be Python 3.6) and navigate to this directory.

Install the requirements:

```bash
pip install -r requirements.txt
```

Next you need to create a 'config.ini' file per module. 
I've made an example file  'config.ini_template', so you can just copy that. The actual settings file will be ignored by git.


## Simple Python UI



brew install protobuf
 pip install pyobjc
 
 