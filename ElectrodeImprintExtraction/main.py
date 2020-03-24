#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2 as cv
import numpy as np
from electrodeProcess import getElectrodeImprint



if __name__ == '__main__':
    imgs = os.listdir('./imgs')
    for img in imgs:
        if 'bmp' in img:
            getElectrodeImprint('./imgs/' + img)
