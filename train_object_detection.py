# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 12:58:05 2021

@author: didie
"""

from detecto.core import Model, Dataset

import os

# %%
# set current working directory to file folder
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# load in dataset
dataset = Dataset('Images\\Hands\\labels\\', 'Images\\Hands\\images\\')

# load in previous model
model = Model(['character'])
model.load('models\\mahjong_character.pth', ['character'])

# train and save model
model.fit(dataset)
model.save('models\\mahjong_character.pth')
