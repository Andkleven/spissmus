# USAGE
# python object_size.py --image images/example_01.png --width 0.955
# python object_size.py --image images/example_02.png --width 0.955
# python object_size.py --image images/example_03.png --width 3.5

# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
import matplotlib.pyplot as plt
from objekt import kjeve, first, mirror, pictures, opp,venstre,hoyre,dark

def plot(image):
    plt.imshow(image)
    plt.show()
def store_tann(gray):
    shape= np.shape(gray)
    for j in range(shape[1]-1,0,-1):
        for i in range(shape[0]-1,0,-1):
            a = gray[i, j]
            if (70 <= a[0] and  100 <= a[1] and 110 <= a[2]):
                checkpoint = 0
                for b in range(i, i+10, 1):
                    for c in range(j, j+7, 1):
                        a = gray[b, c]
                        if (70 <= a[0] and  100 <= a[1] and 110 <= a[2]):
                            checkpoint += 1
                            if (checkpoint == 20):
                                return(j,i)
                                
                                
                                
def firkant(image,orig):
    
    
    edged = cv2.Canny(image, 70, 150)
    edged = cv2.dilate(edged, None, iterations=10)
    edged = cv2.erode(edged, None, iterations=10)
    plot(edged)
    
    
    cnts = cv2.findContours(edged.copy(), cv2.RETR_CCOMP,
    	cv2.CHAIN_APPROX_TC89_L1)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    
    
    (cnts, _) = contours.sort_contours(cnts)
        
    Area_max = cnts[0]
    for c in cnts:


        if cv2.contourArea(c) >= cv2.contourArea(Area_max):
            Area_max = c
    
    orig = orig.copy()
    box = cv2.minAreaRect(Area_max)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    print(box)
    box = np.array(box, dtype="int")
    print(box)
        	# in top-left, top-right, bottom-right, and bottom-left
    box = perspective.order_points(box)
    print(box)

    plot(box)                            
# construct the argument parse and parse the arguments
for t in range(45,81):
    image = cv2.imread('araneus/img'+str(t)+'.jpg')
    
    try:
        orig, orig1, orig2, first = kjeve(image)
        first = first(orig1,orig2)
        orig = mirror(orig, first)
        orig, img1, img_front, first= kjeve(orig)
        gray=dark(orig)
    except:
        continue
    
    
    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    """kernel = np.ones((12,12),np.uint8)
    gray = cv2.morphologyEx(orig, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((7,7),np.uint8)
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    """
    x,y=store_tann(gray)
    """
    img, row1, col = pictures(img1) 
    row = opp(img1, row1, col)
    image = gray.copy()
    """
    #plot(image)

    #firkant(gray,orig)
    cv2.line(gray, (x-30,y), (x-30,y-200), (255,255,255), 20)
    #cv2.line(img, (col,row), (col,row-30), (255,255,255), 20)
    #cv2.line(img, (col,row-40), (x-30,row-40), (255,255,255), 20)
    firkant(gray,orig)
    # find contours in the edge map
    
