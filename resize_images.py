# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 22:41:37 2021

@author: didie
"""

import os
import cv2

# set current working directory to the folder the file is in
abspath = os.path.abspath(__file__)
path = os.path.dirname(abspath)
os.chdir(path)


def resize_images(img_size, image_type):
    # set cwd to the imagetype being analyzed
    os.chdir(os.path.join('Images', image_type))

    # create folder name where the resized images shall be stored
    folder_name = 'ImageSize' + str(img_size)

    # end function if the images have already been resized
    if folder_name in os.listdir('.'):
        return

    # make the folder
    os.mkdir(folder_name)

    # resize each image in the OriginalSize folder
    for item in os.listdir('OriginalSize'):
        if '.jpg' in item:
            # load image from path
            img = cv2.imread(os.path.join('OriginalSize', item), cv2.IMREAD_COLOR)

            # resize image to the desired format
            img = cv2.resize(img, (img_size, img_size))

            # save the resized image
            cv2.imwrite(os.path.join(folder_name, item), img)

    # return to the previous working directory
    os.chdir('..\\..')


def rename_images(image_folder):
    """

    """

    # create a dictionary showing the proper names for each category
    category_translation = {'B': 'bamboo', 'C': 'circle', 'N': 'number',
                            'D': 'dragon', 'W': 'wind', 'F': 'flower'}

    # create a dictionary showing the highest number in each category
    number_limit = {'B': 9, 'C': 9, 'N': 9, 'D': 3, 'W': 4, 'F': 8}

    # change current working directory to this folder
    os.chdir(os.path.join('Images', image_folder))

    # collect the amount of image sets that need to be renamed
    new_image_sets = os.listdir('Original Sets')

    # collect the images that have already been renamed
    current_images = os.listdir('.')

    # collect the image_sets of the files that have been renamed
    current_image_sets = [image[:image.find('_')] for image in current_images if '.jpg' in image]

    # get a unique list of the renamed image_sets
    current_image_sets = list(set(current_image_sets))

    for image_set in new_image_sets:

        # skip if image_set has already been imported
        if image_set in current_image_sets:
            continue

        # collect the images in the image_set
        images = os.listdir(os.path.join('Original Sets', image_set))

        image_count = 0
        for image in images:

            # only rename image if the image is a jpg
            if '.jpg' in image.lower():

                # get category and number of the image
                category = image[0]
                number = image[1]

                # check if the number category is an integer
                if category in category_translation.keys():
                    try:
                        number_int = int(number)
                    except:
                        next

                # check if the number is withing the valid range
                if number_int > 0 and number_int <= number_limit[category]:
                    # create the new image name
                    new_image = image_set + '_' + category_translation[category] + number + '.jpg'

                    # rename the image and put in the correct folder
                    os.rename(os.path.join('Original Sets', image_set, image),
                              new_image)
                    image_count += 1
        os.chdir('../..')
        if image_count != 42:
            print('Number of images renamed: ' + str(image_count))
