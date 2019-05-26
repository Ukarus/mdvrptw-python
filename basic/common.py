# -*- coding: utf-8 -*-

import os

ROOT_PATH = [
    os.path.dirname(os.path.realpath('foodif.py'))
    #os.path.realpath("app\\Http\\Controllers\\foodif_vrp")
]

'''
os.path.dirname(os.path.realpath(__file__))
'C:\wamp64\www\Foodif2\Plataforma-FoodIf\\app\Http\Controllers\\foodif_vrp'
os.path.join(os.environ["USERPROFILE"], "Documents\FoodIf\\foodif_vrp"),
    Ubuntu
    ROOT_PATH = [
        os.path.join(os.environ['HOME'], 'Documentos/FoodIfV2/foodif_vrp'),
    ]
'''


def getrootpath(paths=ROOT_PATH):
    if isinstance(paths, list):
        for path in ROOT_PATH:
            if os.path.exists(path):
                return path
    elif isinstance(paths, str):
        return paths
    else:
        pass


def makeDirsForFile(filename):
    try:
        os.makedirs(os.path.split(filename)[0])
    except:
        pass


def existFile(filename, overwrite=False, displayInfo=True):
    if os.path.exists(filename):
        if overwrite:
            os.remove(filename)
            if displayInfo:
                print ('File: %s exists. Remove: overwrite old file.' % filename)
            return False
        else:
            if displayInfo:
                print ('File: %s exists. Skip: no new file is created.' % filename)
            return True
    else:
        if displayInfo:
            print ('File: %s does not exist. Create new file. ' % filename)
        return False
