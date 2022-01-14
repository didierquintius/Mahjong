# -*- coding: utf-8 -*-

from tensorflow.keras.models import load_model
import cv2
import pickle
import numpy as np
import matplotlib.pyplot as plt

categories = {'B': 'bamboo', 'C': 'circle', 'N': 'number', 'D': 'dragon', 'W': 'wind',
              'F': 'flower'}


def load_model_from_name(name, img_size):
    """
    All models are stored in one folder. Use the name of the model and the
    img_size to determine the path of the model. Then the model can be
    loaded.
    """

    path = 'models/' + name + '_' + str(img_size) + '_model'
    model = load_model(path)
    y_labels = pickle.load(open(path + '/unique_labels.pkl', 'rb'))
    return model, y_labels


def load_models(img_size):
    
    model_names = ['categories', 'dragon', 'wind', 'flower', 'number', 'circle', 'bamboo']
    
    # load each of the models and store them in a dictionary
    models = {}
    labels = {}
    for model_name in model_names:
        models[model_name], labels[model_name] = load_model_from_name(model_name, img_size)
        
    return models, labels
        

class IdentifyCharacters:
    """
    Takes a list of images and identifies which mahjong character is displayed
    in the image. The goal of the identification is to obtain a label for each
    image. A label consists of a category and a character number. The
    identification takes place in two steps. The first step is a model called
    'categories' that identifies the category of the image. The next step is to
    use a model that is specified on that category to obtain the character
    number of the image.

    images: list of numpy arrays of 3 dimensions these three dimension determine
            the pixels of the image.

    img_size: is an integer value that determines to which dimensions the x and
              y-dimensions of an image shall be resized. The z-axis in this case
              is constantly equal to 3 (RGB). This value also determines what
              model is used to identify the image. The models are trained on a
              certain image size and this input images should therefore always
              be equal to this size.
    """

    def __init__(self, img_size):
        self.img_size = img_size  
        self.models, self.labels = load_models(self.img_size)
    
    def reformat_images(self, images):
        # resize the images, change the RGB order and store them in a list
        reformatted_images = []
        for image in images:
            
            image = image[:, :, [2, 1, 0]]/255
            # resize image to the desired format
            image = cv2.resize(image, (self.img_size, self.img_size))
                      
            reformatted_images += [image]
        
        # convert list of images to numpy array that matches the necessary input of
        # convolutional network
        reformatted_images = np.array(reformatted_images).reshape(-1, self.img_size,
                                                                  self.img_size, 3, 1)
        
        return reformatted_images
    
    def identify_category(self, images):
        category = self.models['categories'](images).numpy().argmax(axis=1)
        return category
    
    def identify_number(self, image, category):
       
        # feed image to the model that corresponds to its category
        
        number_probs = self.models[category](image)
        
        # convert the results of the model to the character number
        number = number_probs.numpy().argmax(axis=1)[0] + 1
        
        return number

    def identify(self, images):
        
        images = self.reformat_images(images)
        
        # feed images to categories model and calculate which category most likely
        # corresponds to the image
        # note that the index (not the name) of the category is stored
        image_category_indexes = self.identify_category(images)
        
        # predict the label of each image
        image_labels = []
        for index, category_index in enumerate(image_category_indexes):
            
            image = images[index:(index+1), :]
            
            # convert category index to category name
            category = self.labels['categories'][category_index]
            
            number = self.identify_number(image, category)
            
            plt.imshow(image.reshape(self.img_size, self.img_size, 3))
            plt.text(0, 0, category + str(number))
            plt.show()
            
            image_labels += [category + str(number)]
        return image_labels
