#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
形状筛选，包括面积筛选，圆度，等
'''

import cv2 as cv
from util import area_sort, sort
import numpy as np


def area_filter(cnts, min, max, sorted=False):
    '''
    面积过滤
    :param cnts: 形状列表
    :param min: 最小面积
    :param max: 最大面积
    :param sorted: 排序， 默认FALSE
    :return: 筛选后的cnt_list
    '''

    new_cnt = []
    for c in cnts:
        area = cv.contourArea(c)
        if min <= area <= max:
            new_cnt.append(c)

    return new_cnt if not sorted else area_sort(new_cnt)


def circularity_filter(cnts, min, max, sorted=False):
    '''
    根据圆度筛选轮廓
    圆度计算公式：
        e =（4 * PI * area）/ (length * length)
    :param cnts: 轮廓list
    :param min:  最小圆度
    :param max:  最大圆度
    :param sorted: 是否排序，默认Fal
    :return: cnt_list
    '''

    eList = []
    newList = []
    for c in cnts:
        length = cv.arcLength(c, True)
        area = cv.contourArea(c)
        e = (4 * np.pi * area) / (length * length)

        if min <= e <= max:
            eList.append(e)
            newList.append(c)

    return newList if not sorted else sort(newList, eList)
