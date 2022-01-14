# -*- coding: utf-8 -*-

from detecto.core import Model
from detecto import utils
import matplotlib.pyplot as plt



def detect_characters(image_path, detection=0.9):
    """
    This function makes use of an objection detection model to identify in which
    part of an image a character is located.
    """

    image = utils.read_image(image_path)
    detect_model = Model().load('models\\mahjong_character.pth', ['character'])
    labels, boxes, scores = detect_model.predict(image)
    character_images = []

    # for each valid character
    for index, box in enumerate(boxes):
        if scores[index] > detection:
            box = [int(item) for item in box]
            y1, x1, y2, x2 = box
            
            character_image = image[x1:x2, y1:y2, :]
            character_images.append(character_image)
            plt.imshow(character_image)
            plt.show()
    
    return character_images
    
    