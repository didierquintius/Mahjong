# -*- coding: utf-8 -*-

from model import develop_model
import os

path = os.path.abspath(__file__)
path = os.path.dirname(path)
os.chdir(path)


def run_models():
    
    model_names = ['categories', 'dragon', 'wind', 'flower', 'number', 'circle', 'bamboo']

    for model_name in model_names:
        develop_model(model_name, samples_per_label=50, epochs=1)
    

if __name__ == '__main__':
    run_models()
