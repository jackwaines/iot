#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

import scipy as sp 
import sklearn
import random 
import time 

from sklearn import preprocessing, model_selection

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Dense 
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle


data = pd.read_csv('weatherHistory.csv')

data = shuffle(data)

i = 5
data_to_predict = data[:i].reset_index(drop = True)
predict_conditions = data_to_predict.prediction 
predict_conditions = np.array(predict_conditions)
prediction = np.array(data_to_predict.drop(['prediction'],axis= 1))

data = data[i:].reset_index(drop = True)

X = data.drop(['prediction'], axis = 1)
X = np.array(X)
Y = data['prediction'].astype(str)

encoder = LabelEncoder()
encoder.fit(Y)
Y = encoder.transform(Y)
Y = to_categorical(Y)

train_x, test_x, train_y, test_y = model_selection.train_test_split(X,Y,test_size = 0.1, random_state = 0)

input_dim = len(data.columns) - 1

model = Sequential()
model.add(Dense(8, input_dim = input_dim , activation = 'relu'))
model.add(Dense(10, activation = 'relu'))
model.add(Dense(10, activation = 'relu'))
model.add(Dense(10, activation = 'relu'))
model.add(Dense(3, activation = 'softmax'))

model.compile(loss = 'categorical_crossentropy' , optimizer = 'adam' , metrics = ['accuracy'] )

model.fit(train_x, train_y, epochs = 20, batch_size = 2)

scores = model.evaluate(test_x, test_y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

from tensorflow.keras.models import load_model

model.save("./my_model/",save_format="tf")

model2 = tf.keras.models.load_model('./my_model')

print("All Done!")