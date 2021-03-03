# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 17:08:35 2018

@author: Eikarus
"""

import numpy as np
from objekt import fand_objekt


def split(img):
    big_img = img[950:12870, 380:9720]

    shape_img = np.shape(big_img)
    div_row = shape_img[0]
    mellomrom_row = div_row - (1260*6)
    box_row = mellomrom_row // 7
    div_col = shape_img[1]
    mellomrom_col = div_col - (650*6)
    box_col = mellomrom_col // 7

    number = 0
    img_dick = {}
    
    for i in range(1,8):
        for j in range(7,0,-1):
            col1 = (j-1)*box_col + 650*(j-1)
            row1 = (i-1)*box_row + 1260*(i-1)
            reshape_1 = big_img[row1:(row1 + box_row), col1:(col1 + box_col)]
            _, area = fand_objekt(reshape_1)

            number += 1
            
            if area > 4000:
                img_dick.update({number: reshape_1})

    return(img_dick)


