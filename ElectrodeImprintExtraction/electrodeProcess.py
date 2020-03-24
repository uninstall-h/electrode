#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

MINAREA = 5000

def cv_show(img, cmap='gray'):
    # cv.win
    plt.imshow(img, cmap)
    plt.show()

def show(name, img):
    cv.imshow(name, img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def getElectrodeImprint(path):
    '''
    获取电极印记
    :param path: 图片路径
    :return: None
    '''
    img = cv.imread(path)
    filename = path.split('/')[-1]
    # 转为灰度值
    grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    grayImg = cv.GaussianBlur(grayImg, (3, 3), 0)
    # cv_show(grayImg)
    # 转为二值图，进行轮廓提取
    binImg = cv.threshold(grayImg, 127, 255, cv.THRESH_BINARY_INV)[1]
    # 开操作，突出连接印记边缘
    openKernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (10, 10))
    dilateKernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (25, 25))
    morphImg = cv.morphologyEx(binImg, cv.MORPH_OPEN, openKernel, iterations=2)
    morphImg = cv.morphologyEx(morphImg, cv.MORPH_DILATE, dilateKernel, iterations=2)
    # 获取轮廓
    cnts = cv.findContours(morphImg, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[1]
    # cntsImg = cv.drawContours(img.copy(), cnts, -1, (255, 0, 0), 5)
    # cv_show(cntsImg, cmap='hsv')
    # 获取轮廓外接矩形
    rect = []
    for c in cnts:
        if cv.contourArea(c) > MINAREA:
            x, y, w, h = cv.boundingRect(c)
            if 0.7 <= w / h <= 1.3:
                # cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 5)
                rect.append([y-25, y+h+25, x-25, x+w+25])

    # 位置排序, 先根据y坐标排序，再每6个对x坐标排序
    rectSorted = []
    rect = sorted(rect, key=lambda ry: ry[0])
    for i in range(0, 41, 6):
        rectSorted.extend(sorted(rect[i:i+6], key=lambda rx: rx[2]))

    # print(rectSorted)
    for i, r in enumerate(rect):
        # show('imprint%s'%i, img[r[0]:r[1], r[2]:r[3]])
        print('./imgs/imprints/%s/%s.jpg'%(filename, i))
        # cv.imwrite('./imgs/imprints/%s/%s.jpg'%(filename, i), img[r[0]:r[1], r[2]:r[3]])
        plt.imsave('./imgs/imprints/%s/%s.jpg'%(filename, i), img[r[0]:r[1], r[2]:r[3]])

    # cv_show(img, cmap='hsv')