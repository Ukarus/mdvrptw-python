# -*- coding: utf-8 -*-

import os
from basic.common import getrootpath
from core.utils import text2json

def main():

    instance= 'pr02.txt'
    rootpath = getrootpath()
    filePath = os.path.join(rootpath,'data','c-mdvrptw','txt')

    #Función para formatear datos en formato json
    text2json(instance,filePath)


if __name__ == '__main__':
    main()