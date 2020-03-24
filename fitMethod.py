#! /usr/bin/env python
# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np
from util import area_sort

font = cv.FONT_HERSHEY_SIMPLEX  # 设置字体样式

def fitCircle(src):
    img = src.copy()
    mask = np.zeros(img.shape, np.uint8)
    cnt = getCnts(img)
    (x, y), radius = cv.minEnclosingCircle(cnt)
    center = (int(x), int(y))
    radius = int(radius)
    # area = cv.contourArea(cnt)
    # equi_diameter = np.sqrt(4 * area / np.pi)
    img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
    cv.circle(img, center, radius, (0, 255, 0), 2)
    cv.circle(mask, center, radius, 1, -1)
    # text1 = 'Center: (' + str(int(x)) + ', ' + str(int(y)) + ') '
    # text2 = 'Diameter: ' + str(2 * radius)
    # cv.putText(imgs, text1, (10, 30), font, 0.5, (0, 255, 0), 1, cv.LINE_AA, 0)
    # cv.putText(imgs, text2, (10, 60), font, 0.5, (0, 255, 0), 1, cv.LINE_AA, 0)

    return img, mask


def fitEllipse(src):
    img = src.copy()
    mask = np.zeros(img.shape, np.uint8)
    cnt = getCnts(img)
    ellipse = cv.fitEllipse(cnt)
    # (x, y), (a, b), angle = cv.fitEllipse(cnt)
    img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
    cv.ellipse(img, ellipse, (0, 255, 0), 2)
    cv.ellipse(mask, ellipse, 1, -1)
    # text1 = 'x: ' + str(int(x)) + ' y: ' + str(int(y))
    # text2 = 'a:  ' + str(int(a)) + ' b:  ' + str(int(b))
    # text3 = 'angle: ' + str(round(angle, 2))
    # cv.putText(imgs, text1, (10, 30), font, 0.5, (0, 255, 0), 1, cv.LINE_AA, 0)
    # cv.putText(imgs, text2, (10, 60), font, 0.5, (0, 255, 0), 1, cv.LINE_AA, 0)
    # cv.putText(imgs, text3, (10, 90), font, 0.5, (0, 255, 0), 1, cv.LINE_AA, 0)
    # print(mask.max(), mask.min())
    return img, mask


def outer(src):
    img = src.copy()
    mask = np.zeros(img.shape, np.uint8)
    cnt = getCnts(img)
    img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
    cv.drawContours(img, [cnt], 0, (0, 255, 0), 5)
    cv.drawContours(mask, [cnt], 0, 1, -1)
    return img, mask


def getCnts(img):
    image, contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    return area_sort(contours)[1]
