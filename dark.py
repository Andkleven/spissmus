# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 16:42:57 2018

@author: amkle
"""
import cv2
import numpy as np


def dark(img):
    shape_img = np.shape(img)
    for i in range(0, shape_img[0], 1):    # Alle farger under 80,80,80(rgb) blir gjort om til svart
        for j in range(0, shape_img[1], 1):
            a = img[i,j]
            if (80 >= a[0] and  80 >= a[1] and 80 >= a[2]):
                img[i,j]=[0,0,0]
    kernel = np.ones((12,12),np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)      #Fjerner alle flekker som er mindre enn 12,12 utenfor objektet.
    kernel = np.ones((7,7),np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)      #Fjerner alle flekker som er mindre enn 7,7 innfor objektet (https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html)

    return(img)
