#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from fitMethod import fitEllipse, fitCircle, outer
from excelOp import writeAreaToExcel


def get_img_list(path):
    path = path.strip().rstrip('/')
    file_list = os.listdir(path.rstrip('/'))
    # print(file_list)
    file_list = [f"{path}/{x}" for x in file_list]
    return file_list


if __name__ == '__main__':
    img_path = get_img_list("./img/first/")
    # print(img_path)
    area_list = {}
    # idx_list = []
    for i in img_path[:]:
        img = cv.imread(i, 0)[:-20, :-20]
        img_bulr = cv.medianBlur(img, ksize=5)
        plt.subplot(231)
        plt.axis('off')
        plt.imshow(img, "gray")
        plt.subplot(232)
        plt.axis('off')
        plt.imshow(img_bulr, "gray")
        plt.subplot(233)
        plt.axis('off')
        _, img_th = cv.threshold(img, 255, 155, cv.THRESH_OTSU)
        plt.imshow(img_th, "gray")
        plt.subplot(234)
        plt.axis('off')
        _, img_th = cv.threshold(img, 255, 255, cv.THRESH_OTSU)
        k = cv.getStructuringElement(cv.MORPH_CROSS, (5, 5))
        img_morph = cv.morphologyEx(img_th, cv.MORPH_OPEN, k, iterations=2)
        plt.imshow(img_morph, "gray")
        plt.subplot(235)
        plt.axis('off')
        fit_cyl_res, mask_cyl = fitCircle(img_morph)
        plt.imshow(fit_cyl_res)
        plt.subplot(236)
        plt.axis('off')
        fit_elp_res, mask_elp = fitEllipse(img_morph)
        plt.imshow(fit_cyl_res)
        # 设定子图间距 ， left < right, top > bottom, 数字表示窗口大小的比例（如下则子图间距为窗口大小的1%）
        plt.subplots_adjust(left=0.04, top=0.96, right=0.96, bottom=0.04, wspace=0.05, hspace=0.01)
        # plt.show()
        plt.imshow(mask_cyl, 'gray')
        print(i)
        # plt.show()

        area_outer, mask_outer = outer(img_morph)
        print(mask_outer.max(), mask_outer.min())
        print(area_outer.max(), area_outer.min())
        print(fit_cyl_res.max(), mask_cyl.max())
        print(fit_cyl_res.min(), mask_cyl.min())
        # plt.imshow(mask_outer)
        # plt.show()
        # print(img_morph.shape, mask_cyl.shape)
        # print(np.sum(mask_cyl == 255))
        # print(np.sum(img_morph == 0))
        # print(np.sum((img_morph + mask_cyl) == 1))
        fit_area_cyl = np.sum(mask_cyl == 1)
        fit_area_elp = np.sum(mask_elp == 1)
        fit_area_outer = np.sum(mask_outer == 1)
        area_cyl = np.sum((img_morph + mask_cyl) == 1)
        area_elp = np.sum((img_morph + mask_elp) == 1)
        area_out = np.sum((img_morph + mask_outer) == 1)
        idx = int(i.split('/')[-1].lstrip('n').strip('.bmp'))
        # idx_list.append(idx)
        cyl_rate = area_cyl / float(fit_area_cyl)
        elp_rate = area_elp / float(fit_area_elp)
        out_rate = area_out / float(fit_area_outer)
        area_list[idx] = [fit_area_cyl, area_cyl, cyl_rate,
                          fit_area_elp,  area_elp, elp_rate,
                          fit_area_outer, area_out, out_rate
                          ]

    # idx_list.sort()
    # print(idx_list)
    print(area_list)
    writeAreaToExcel(area_list)


