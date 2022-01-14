# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 20:57:25 2021

@author: didie
"""

# import packages
import os, pickle, cv2
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv3D, MaxPooling3D, Dropout

from livelossplot import PlotLossesKeras
from tensorflow.keras.models import load_model
from resize_images import resize_images
from keras.preprocessing.image import ImageDataGenerator

abspath = os.path.abspath(__file__)
path = os.path.dirname(abspath)
os.chdir(path)

datagen = ImageDataGenerator(rotation_range=45, width_shift_range=0.1,
                             height_shift_range=0.1, shear_range=0.1,
                             zoom_range=0.1, horizontal_flip=True,
                             vertical_flip = True)

def CNN_Model(img_size, nodes1, nodes2,nodes3, kernel1, kernel2, kernel3, pool1, pool2, pool3, dropout_rate, dense_nodes, output = 42):
    model = Sequential([
      Conv3D(nodes1, kernel1, input_shape=(img_size, img_size, 3, 1), activation='relu'),
      MaxPooling3D(pool_size=pool1),
      
      Conv3D(nodes2, kernel2, input_shape=(img_size - kernel1[0] - pool1[0] + 2, 
                                           img_size - kernel1[1] - pool1[1] + 2, 1, nodes1), activation = 'relu'),
      MaxPooling3D(pool_size=pool2),
      Dropout(dropout_rate),
      
      Conv3D(nodes3, kernel3, input_shape=(img_size - kernel2[0] - pool2[0] + 2, 
                                           img_size - kernel2[1] - pool2[1] + 2, 1, nodes2), activation = 'relu'),
      MaxPooling3D(pool_size=pool3),
      Dropout(dropout_rate),
      
      Flatten(),
      Dense(dense_nodes, activation = 'relu'),
      Dense(output, activation='softmax'),
    ])
    return model  

def get_relevant_images(model_name, img_size):
    image_folder = os.path.join('Images', 'Character', 'ImageSize' + str(img_size))
    
    if not os.path.exists(image_folder):
        resize_images(img_size, 'Character')
                   
    data_original = []
    labels_original = []
    
    for file in os.listdir(image_folder):
        if ("jpg" in file.lower()):
    
            full_name = file.split('.jpg')[0]
            _ , category, number = full_name.split('_')
            
            if model_name == 'categories':
                label = category 
            else: 
                if category != model_name: continue
                label = number
            
            image = cv2.imread(os.path.join(image_folder, file), cv2.IMREAD_COLOR)
            image = np.array(image) / 255
            
            data_original.append(image)
            labels_original.append(label)
          
    labels_original = pd.get_dummies(labels_original)
    
    unique_labels = labels_original.columns
    
    labels_original = labels_original.to_numpy()
    data_original = np.array(data_original)
    
    plt.show()
    
    return data_original, labels_original, unique_labels

def construct_dataset(data, labels, img_size, unique_labels, samples_per_label,
                      test_size, train_size):
    
    training_data = np.empty((0, img_size, img_size, 3))
    
    training_labels = np.empty((0, len(unique_labels)))
    count = 0

    for batch in datagen.flow(data, labels):
        data, label = batch
        training_data = np.append(training_data, data, axis = 0)
        training_labels = np.append(training_labels, label, axis = 0)
        
        count += 1
        print(count)
        if count % 50 == 0: print(count)
        if count == samples_per_label: break
    
    training_data = training_data.reshape(-1, img_size, img_size, 3, 1)
    
    
    x_train, x_test, y_train, y_test = train_test_split(training_data, training_labels,
                                                    test_size = test_size,
                                                    train_size = train_size)
    
    return x_train, x_test, y_train, y_test

def get_model(model_path, img_size, unique_labels):
        
    try:
        model = load_model(model_path)
    except:
        model = CNN_Model(img_size, 32, 64, 128, (3,3,3), (3,3,1), (3,3,1), (2,2,1),(2,2,1),
                      (2,2,1), 0.1, 24, output = len(unique_labels))
      
        model.compile( optimizer = 'adam',  loss='categorical_crossentropy',  
                      metrics=['accuracy'])
    
    return model
def develop_model(model_name, img_size = 50, test_size = 0.1,
                  epochs = 5, train_size = None, samples_per_label = 1000):
   
    data, labels, unique_labels = get_relevant_images(model_name, img_size)
           
    x_train, x_test, y_train, y_test = construct_dataset(data, labels, img_size, unique_labels, samples_per_label, test_size, train_size)
      
    # Compile the model.
    model_path = 'models\\' + model_name + '_' + str(img_size) + '_model'

    model = get_model(model_path, img_size, unique_labels)
    plt.imshow(x_train[0,:,:,:,0])
    plt.show()
    # Train the model
    callback = EarlyStopping(monitor='val_loss', patience=3, min_delta=1e-4,
                                 restore_best_weights = True)
    model.fit(x_train, y_train, validation_data=(x_test, y_test), 
              epochs = epochs, callbacks=[callback, PlotLossesKeras()],
              validation_steps=5)
    
    # Save model and y labels
    model.save(model_path)
    pickle.dump(unique_labels, open(model_path +'\\unique_labels.pkl', 'wb'))
    
    

