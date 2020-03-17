#! /usr/bin/env python
# -*- coding: utf-8 -*-

import cv2 as cv


def area_sort(contours):
    new_cnts = []
    area_list = []
    for cnt in contours:
        area = cv.contourArea(cnt)
        # if area > 10:
        new_cnts.append(cnt)
        area_list.append(area)
    # space = np.ones([r, c], np.uint8) * 255
    # print(space)
    #
    # cv2.imshow('space', space)

    n = len(new_cnts)
    for j in range(0, n - 1):
        for i in range(0, n - 1 - j):
            if area_list[i] < area_list[i + 1]:
                new_cnts[i], new_cnts[i + 1] = new_cnts[i + 1], new_cnts[i]
                area_list[i], area_list[i + 1] = area_list[i + 1], area_list[i]

    return new_cnts


def sort(source: list, ruler: list):
    '''
    ruler 与 source 长度相同且一一对应的list
    根据ruler的值对source 排序
    返回 排序后的source
    :param source: 待排序list
    :param ruler: 排序参考
    :return: sorted
    '''

    if len(source) != len(ruler):
        return []

    n = len(source)
    for j in range(0, n - 1):
        for i in range(0, n - 1 - j):
            if ruler[i] < ruler[i + 1]:
                source[i], source[i + 1] = source[i + 1], source[i]
                ruler[i], ruler[i + 1] = ruler[i + 1], ruler[i]

    return source


