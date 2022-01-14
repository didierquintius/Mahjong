
# import packages
import os
import cv2
import matplotlib.pyplot as plt
from detect_characters import detect_characters
from identify_character import identify_characters
from calculate_points import PointCalculator

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)  


def test_images():
    # get image
    image_path = "Images\\Hands\\images\\AZUM8062.JPG"
    plt.imshow(cv2.imread(image_path))
    plt.show()
    
    # detect characters in image
    character_images = detect_characters(image_path)
    
    # identify characters
    identify_model = identify_characters(50)
    characters = identify_model.identify(character_images)

    # calculate the points
    points, configuration = PointCalculator(characters).calculate_points()
    
    print(points, configuration)


if __name__ == '__main__':
    test_images()
