# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 16:24:53 2019

@author: amkle
"""
import numpy as np
import cv2 


def draw_img(orig, koor, nervehule,k):
    _, dick_koor, img, back = draw(orig, True,k)
    for i in dick_koor:
        if len(dick_koor[i])==1:
            koor.pop(8)
            koor.insert(8,dick_koor[i][0])
            nervehule = True 
        elif len(dick_koor[i])==2:
            chack1, chack2 = False, False
            for j in range(len(koor)):
                if koor[j][0]-4< dick_koor[i][0][0]<koor[j][0]+4 and koor[j][1]-4< dick_koor[i][0][1]<koor[j][1]+4:
                    chack1 = True  
                    a = j   
                if koor[j][1]-4< dick_koor[i][1][1]<koor[j][1]+4 and koor[j][0]-4< dick_koor[i][1][0]<koor[j][0]+4:
                    chack2 = True
                    a = j
            if chack1:
                koor.pop(a)
                koor.insert(a,dick_koor[i][1])
            if chack2:
                koor.pop(a)
                koor.insert(a,dick_koor[i][0])
    return(koor,nervehule,back)


def draw(img, check, k):
    img = img.copy()
    windowName = 'Bilde'+str(k)
    koor = []
    koor_dict = {}
    t=0
    back = 0

    #img = np.zeros((512,512,3),np.uint8)
    cv2.namedWindow(windowName)

    
    def draw_circle(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(img, (x, y), 3, (0,255,0), -1)
            koor.append([y,x])
            cv2.destroyAllWindows()

    if check:
        while(True):
            cv2.setMouseCallback(windowName, draw_circle)
            t += 1
            cv2.imshow(windowName, img)  
            koor_dict.update({t: koor})
            koor = []
            key = cv2.waitKey(0)
            if key == ord('N') or key == ord('n'):
                back = 0
                break
            if key == ord('O') or key == ord('o'):
                back = 2
                break
        koor_dict = {k : v for k,v in koor_dict.items() if 0<len(v)<3}

        #koor_dict.pop(k for k, v in koor_dict.items() if len(v)>2)
             
    else:
        while(True):
            cv2.setMouseCallback(windowName, draw_circle)
            cv2.imshow(windowName, img)  
            key = cv2.waitKey(0)
            if key == ord('N') or key == ord('n'):
                back = 0
                break
            if key == ord('O') or key == ord('o'):
                back = 2
                break
         
       
    cv2.destroyAllWindows()
    return(koor, koor_dict, img, back)
    #cv2.imwrite('img.jpg', img)


def finn_punkt(koor):
    lengd = len(koor)
    max_koor = []
    for i in range(len(koor)):
        max_koor.append(koor[i][0])
    minimum = max_koor.index(np.min(max_koor))
    row_4_2, col_4_2 = koor[minimum]
    koor.pop(minimum)
    
    max_koor = []
    for i in range(len(koor)):
        max_koor.append(koor[i][0])
    minimum = max_koor.index(np.min(max_koor))
    row_2_4, col_2_4 = koor[minimum]
    koor.pop(minimum)
    
    if col_4_2 < col_2_4:
        row2, col2 = row_4_2, col_4_2
        row4, col4 = row_2_4, col_2_4
    else:
        row4, col4 = row_4_2, col_4_2
        row2, col2 = row_2_4, col_2_4
    
    max_koor = []
    for i in range(len(koor)):
        max_koor.append(koor[i][0])
    minimum = max_koor.index(np.min(max_koor))
    row3, col3 = koor[minimum]
    koor.pop(minimum)
    
    if lengd == 8:
        max_koor = []
        for i in range(len(koor)):
            max_koor.append(koor[i][1])
        minimum = max_koor.index(np.min(max_koor))
        row7, col7 = koor[minimum]
        koor.pop(minimum)
    else:
        row7, col7 = 0,0
    
    max_koor = []
    for i in range(len(koor)):
        max_koor.append(koor[i][1])
    minimum = max_koor.index(np.min(max_koor))
    row1, col1 = koor[minimum]
    koor.pop(minimum)
    
    max_koor = []
    for i in range(len(koor)):
        max_koor.append(koor[i][1])
    minimum = max_koor.index(np.min(max_koor))
    row9, col9 = koor[minimum]
    koor.pop(minimum)
    
    max_koor = []
    for i in range(len(koor)):
        max_koor.append(koor[i][1])
    minimum = max_koor.index(np.min(max_koor))
    row8, col8 = koor[minimum]
    koor.pop(minimum)
    
    max_koor = []
    for i in range(len(koor)):
        max_koor.append(koor[i][1])
    minimum = max_koor.index(np.min(max_koor))
    row0, col0 = koor[minimum]
    koor.pop(minimum)
    
    if lengd == 8: punkt_c = True
    else: punkt_c = False

    koor_new = [[row0,col0],[row1,col1],[row2,col2],[row3,col3],[row4,col4],[0,0],[0,0],[row7,col7],[row8,col8],[row9,col9]]
    return(koor_new, punkt_c)
    
    
