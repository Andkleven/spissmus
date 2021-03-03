# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 12:23:34 2018

@author: Eikarus
"""

"""prøve at svart er lik under 100 01


"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 14:39:33 2019

@author: amkle
"""

    
    
from imutils import perspective
from imutils import contours
import numpy as np
import cv2
import matplotlib.pyplot as plt
from dark import dark
from measure import linje as li
from measure import vektor
import matplotlib as ply

def plot(img):
    plt.imshow(img)              
    plt.show()


def fand_objekt(image):


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)                              # Laster inn bilde svart hvite
    gray = cv2.GaussianBlur(gray, (7, 7), 0)                                    # Gjør bilde bluri så det fortere å analysere     
    edged = cv2.Canny(gray, 0, 70)
    edged = cv2.dilate(edged, None, iterations=10)
    edged = cv2.erode(edged, None, iterations=10)                               # Finner kontraster i bilde

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,                    # Finner kontuere til objekter i bilde
                            cv2.CHAIN_APPROX_SIMPLE)

    try:
        cnts = cnts[0] 
        
        (cnts, _) = contours.sort_contours(cnts)
        
        Area_max = cnts[0]
        for c in cnts:                                                          # Finner det største objektet i bilde
            if cv2.contourArea(c) >= cv2.contourArea(Area_max):
                Area_max = c   
        box = cv2.minAreaRect(Area_max)                                         # Finner fire punkter som definnerer objektet
        box = cv2.boxPoints(box) 
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)                                     # setter dem i orden fra øverst til venstre, øverst til høyre, nederst til høyre og nederst til venstre
        area = cv2.contourArea(Area_max)                                        # Finner arealet til objektet
    except:
        box = 0                                                                 # Om det ikke er noe objekt i bilde settes arialet til 0 og ounktene til 0
        area = 0

    return(box, area)


def xy_koor(box):
    list_x = []
    for i in range(4):
        list_x.append(box[i][0])
    max_x = int(np.max(list_x))
    min_x = int(np.min(list_x))

    list_y = []
    for i in range(4):
        list_y.append(box[i][1])
    max_y = int(np.max(list_y)+30)
    min_y = int(np.min(list_y)-30)
    if min_y < 0:
        min_y = 0    
    if min_x < 0:
        min_x = 0    
    return((max_x), (min_x), (max_y), (min_y))                                  # Finner max og min verdien til x og y i boksen som bestemmer arialet 

def first(orig1,orig2):                                                         # Finner det høyeste objektet i to bilder
    box1, Area1 = fand_objekt(orig1)
    box2, Area2 = fand_objekt(orig2)
    
    max_x1, min_x1, max_y1, min_y1 = xy_koor(box1)
    max_x2, min_x2, max_y2, min_y2 = xy_koor(box2)
  
    if((max_y1-min_y1) > (max_y2-min_y2)):                                      # Om bilde 1 er setter den first lik 1 
        first = True
    else:
        first = False                                                           # Om bilde 2 er setter den first lik 0 
    return(first)
        

def kjeve(image):
    box, Area_max = fand_objekt(image)
    shape = np.shape(image)
    max_x, min_x, max_y, min_y = xy_koor(box)
    max1_x = int((max_x - min_x)/2)
    orig = image[min_y:max_y, 0:shape[1]]                                       # lager et bilder rundt kjeven 

    orig1 = orig.copy()[0:, 0:(min_x+max1_x)]                                   # Deler bilde to vertikalt orig1 er første bilde
    orig2 = orig.copy()[0:, (min_x+max1_x):]                                    # orig2 er andre del av bilde

    return(orig, orig1, orig2, first)

def mirror(image, first):                                                       # fliper bilde om first er 0
    if (first == False):
        image = cv2.flip(image, 1)
    return(image)


def draw_circle(R, S, image):                                                   # tegenr en rødt skrikel R=radius S er senter punkt i bilde
    cv2.circle(image,(S,R), 3, (0,0,255), -1)
    return(image)

                                             
def ps(ima, col):
    shape = np.shape(ima)
    list1 = []
    list2 = []
    for j in range(col, 0, -1):
        for i in range(0, shape[0]-50, 1):
            a = ima[i, j]
            if (70 <= a[0] and  100 <= a[1] and 110 <= a[2]):
                checkpoint = 0
                for b in range(i, i+10, 1):
                    for c in range(j, j+7, 1):
                        a = ima[b, c]
                        if (70 <= a[0] and  100 <= a[1] and 110 <= a[2]):
                            checkpoint += 1
                            if (checkpoint == 20):
                                list1.append(i)
                                list2.append(j)
                                
    i = np.min(list1[:])
    a = list1.index(i)
    j = list2[a]                           
    return(ima, i, j)

            

def black2(ima, col_start, col_end, start_row):
    black_list = []
    for i in range(start_row, start_row + 40, 1):
        for j in range(col_start + 25, col_end, 1):
            a = ima[i, j]
            if (a[0] <= 40  and  a[1] <= 50  and a[2] <=  50):
                black_list.append([i,j])
    return(black_list) 

 
def black4(ima, row, col):
    black_list = []
    ima = ima[row-60:row-15,col-110:col-10]
    shape=np.shape(ima)
    checkpoint = 0
    for i in range(2, shape[0]-2, 1):
        for j in range(2, shape[1]-2, 1):
            a = ima[i, j]
            if (75 >= a[0] and  85 >= a[1] and 105 >= a[2]):              
                for b in range(i-2, i+2, 1):
                    for c in range(j-2, j+2, 1):
                        a = ima[b, c]
                        if (75 >= a[0] and  85 >= a[1] and 105 >= a[2]):
                            checkpoint += 1
                            if (checkpoint == 1):
                                black_list.append([i+row-60,j+col-110])   
    return(black_list)


def last(ima, row_start, col_start, col_end):
    black_list = []
    shape = np.shape(ima)
    for i in range(row_start, shape[0]-2, 1):
        for j in range(col_start, col_end, 1):
            a = ima[i,j]
            if (60 <= a[0] and  60 <= a[1]  and 60 <= a[2]):
                checkpoint = 0
                for b in range(i-5, i, 1):
                    for c in range(j-20, j+10, 1):
                        a = ima[b,c]
                        if (80 <= a[0] and  80 <= a[1]  and 80 <= a[2]):
                            checkpoint += 1
                            if (checkpoint == 110):
                                black_list.append([i,j]) 
    return(black_list)
    
    
def firkant(image,orig): 
    edged = cv2.Canny(image, 70, 150)
    edged = cv2.dilate(edged, None, iterations=20)
    edged = cv2.erode(edged, None, iterations=20)
    
        
    cnts = cv2.findContours(edged.copy(), cv2.RETR_CCOMP,
    	cv2.CHAIN_APPROX_TC89_L1)
    cnts = cnts[0] 
    
    (cnts, _) = contours.sort_contours(cnts)
        
    Area_max = cnts[0]
    for c in cnts:
        if cv2.contourArea(c) >= cv2.contourArea(Area_max):
            Area_max = c
    orig = orig.copy()
    box = cv2.minAreaRect(Area_max)
    box = cv2.boxPoints(box)
    box = perspective.order_points(box)
    box = np.array(box, dtype="int")
    #cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
    #plot(orig)
        	# in top-left, top-right, bottom-right, and bottom-left
    return(box, edged) 


    
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
                                

def test(img, row, col_start, col_slutt):
    black_list = []
    for j in range(col_start,col_slutt,-1):
        for i in range(row,row-20, -1):
            a = img[i,j]
            if (a[0] <= 60  and  a[1] <= 60  and a[2] <= 60):
                black_list.append([i,j])
            else:
                break
    return(black_list)    
    
    
def topp(linje, x, y, edged):
    #plot(edged)
    skritt = int(abs(1/linje))
    if linje>0: steg=1
    else:  steg=-1
    k=0
    for i in range(x,400):
        k+=1
        if k%skritt==0: y+=steg
        for j in range(y-1,y+20):
            if edged[j,i]==255: 
                return(y,i)  

def front(linje, x, y, edged):
    #plot(edged)
    skritt = int(abs(1/linje))
    if linje>0: steg=-1
    else:  steg=1
    k=0
    for i in range(x,0,-1):
        k+=1
        if k%skritt==0: y+=steg
        for j in range(y,y-2,-1):
            if edged[j,i]==255: 
                return(y,i)  
                
                
def bunn(linje, x, y, edged):
    if linje>0: steg=1
    else:  steg=-1
    k=0
    for i in range(y,0,-1):
        k+=1
        if int(linje)==0: pass
        elif k%int(linje)==0: x+=steg
        if edged[i,x]==255: return(i,x) 
        
def ned_black(ima, row, col):
    shape = np.shape(ima)
    list1 = []
    for i in range(row+80, shape[0]-10, 1):
        for j in range(col-20, col+10, 1):
            a = ima[i,j]
            if (70 <= a[0] and  100 <= a[1] and 110 <= a[2]):
                list1.append([i,j])                                                            
    black_list2 = []
    for i in range(np.shape(list1)[0]):
        black_list2.append(list1[i][0])  
    row, col = list1[black_list2.index(np.max(black_list2))]
    return(row,col)

def ned_white(ima, row, col):
    shape = np.shape(ima)
    for j in range(row, shape[0], 1):
        a = ima[j, col+5]
        if (a[0] >= 40  and  a[1] >= 60  and a[2] >= 70):
            row = j-1
            return(row)
            
            
def opp(ima, row, col):
    for j in range(row, 0, -1):
        a = ima[j, col]
        if (a[0] <= 40  and  a[1] <= 40  and a[2] <= 50):
            row = j+1
            return(row)
            
def ned(ima, row, col):
    shape = np.shape(ima)
    for j in range(row, shape[0], 1):
        a = ima[j, col]
        if (a[0] <= 80  and  a[1] <= 80  and a[2] <= 80):
            row = j-1
            return(row)

def hoyre(ima, row, col):
    shape = np.shape(ima)
    for j in range(col, shape[1]-1, 1):
        a = ima[row, j]
        if (a[0] <= 80  and  a[1] <= 80  and a[2] <= 80):
            col = j-1
            return(col)

def venstre(ima, row, col):
    for j in range(col, 0, -1):
        a = ima[row, j]
        if (a[0] <= 80  and  a[1] <= 80  and a[2] <= 80):
            col = j+1
            return(col)            
            
def hoyre_hvite(ima, row, col):
    shape = np.shape(ima)
    for j in range(col, shape[1]-1, 1):
        a = ima[row, j]
        if (a[0] >= 80  and  a[1] >= 80  and a[2] >= 80):
            col = j-1
            return(col)            


def bilde_back(img):
    
    orig, orig1, orig2, first = kjeve(img)      # Kjører funsjon kjeve
    first = first(orig1,orig2)                  # Kjører funsjon first   
    orig = mirror(orig, first)                  # Kjører funsjon mirror
    rent_bilde = orig.copy()
    orig, img1, img_front, first= kjeve(orig)   # Kjører funsjon kjeve
    img = dark(img1)                            # Kjører funsjon dark 
    gray = dark(orig)                           # Kjører funsjon dark 
    koor = []
    x1,y1=store_tann(gray)                      # Finner yterkanten til kjeven(ved hjelp av fargekontraster) 
    cv2.line(gray, (x1-30,y1), (x1-30,y1-210), (255,255,255), 20)       # Tegner en hvit linje opp fra punktet funnet i linje over 
    box, edged = firkant(gray,orig)                                     # Finner boksen fom definerer firkanten rundt kjeven. edged er bilde der kontraster er fram hevet
    
    #punkt 0 og 1
    koor.append([box[2][1],box[2][0]])                          # Legger punkt 0 og en til 1 listen koor
    koor.append([box[3][1],box[3][0]])

    
    #punkt 2
    linje1 = li(box[1][0],box[0][0],box[1][1],box[0][1])        # Finner linjen mellom topp punktene som definnerer 
    row_4, col = topp(linje1[0], box[0][0], box[0][1], edged)   # Finner topp punktet av kjeven ved å søke langs linjen. Bruker kontraster til å finne kjeven med edged
    row = ned_white(img1, row_4, col)                           # Søker mot venstre til det blir svart. Der settes punkt 2
    koor.append([row, col])                                     # Legger punkt 2 til list koor

    
    #punkt 3
    col = koor[2][1]                                            
    img, row, col = ps(img, col-35)                 # Finner topp punktet på kjeven bak punkt 2 med farge forskjell
    row = opp(img, row, col)+5
    col = venstre(img, row, col)+5
    row = opp(img, row, col)
    col = venstre(img, row, col)
    koor.append([row,col])                          # Legger til punktet i listen koor

    
    #finner punkt 4
    row,col=koor[3]
    col1 = hoyre_hvite(img, row-40, col+20)                     # Finner mitden av toppen til kjeven
    col2 = hoyre(img, row-40, col1+30)
    row = opp(rent_bilde, row_4,int(((col2-col1)/2)+col1))      # Finner toppen punktet til kjever
    koor.append([row,int(((col2-col1)/2)+col1)])                # Legger til punktet i listen koor

    
    #finner punkt 5               
    start_row, col_start = koor[3]                              # Finner bunnpunktet mellom punkt 3 og 2
    _, col_end = koor[2]
    black_list = black2(img1, col_start, col_end, start_row)
    black_list2 = []
    for i in range(np.shape(black_list)[0]):
        black_list2.append(black_list[i][0])
    row, col = black_list[black_list2.index(np.max(black_list2))]
    koor.append([row, col])
    #plot(img1)
    

    #finner punkt 6
    row,col = koor[4]  
    vektor1,_ = vektor(box[2][0],box[3][0],box[2][1],box[3][1])                           # Finner linjen1 mellom punkt 1 og 0 sp finner den linjen som er vinkel rett på linjen1 
    vektor2,_ = vektor(box[3][0],col,box[3][1],row)                                      # og går gjennom punkt 4. Søker fra kryss punktet mellom linjen og oppover til den kommer til kjeven.
    t = (-(vektor2[0]*vektor1[0])-(vektor2[1]*vektor1[1]))/((vektor1[1]**2)+(vektor1[0]**2))
    x = int(vektor2[0]+vektor1[0]*t)+col
    y = int(vektor2[1]+vektor1[1]*t)+row
    linje = li(x,col,y,row)
    row,col = bunn(linje[0], x, y, edged)
    koor.append([row,col])
    #plot(img1)     
    
    
    # finner punkt 7
    try:      
        row, col = ned_black(img, koor[5][0], int(koor[3][1]+((koor[5][1]-koor[3][1])/2)))  # Ser om det er kjeve bak punkt 3 og om det er noen punkt 7 eller om den er bruket av
        koor.append([row,col])
        punkt_c = True
      
    except:
        punkt_c = False
        koor.append([0,0]) 

    
    #punkt 8
    
    try:
        row, col = front(linje1[0], box[2][0], box[2][1], edged)               #
        black_list = black4(img_front, row, col-np.shape(img1)[1])
        black_list2 = []
        for i in range(np.shape(black_list)[0]):
            black_list2.append(black_list[i][1]) 
        row, col = black_list[black_list2.index(np.min(black_list2))]
        col = int(col + ((col - hoyre(img, row, col))/2))
        koor.append([row, col+np.shape(img1)[1]])
        nervehule = True
    
    except:
        nervehule = False 
        koor.append([0,0])

 
    #punkt 9

    black_list = test(img1, koor[6][0], koor[6][1], koor[2][1]-10)
    if len(black_list)>0:
        black_list2 = []
        for i in range(np.shape(black_list)[0]):
            black_list2.append(black_list[i][0])  
        row, col = black_list[black_list2.index(np.min(black_list2))]
        koor.append([row, col])
    else:
        koor.append([koor[6][0], koor[6][1]])
    
    if punkt_c==False:
        cv2.line(gray, (koor[2][1],koor[2][0]), (koor[2][1],koor[2][0]-20), (255,255,255), 20)
        cv2.line(gray, (x1-30,y1), (x1-30,y1-220), (255,255,255), 20)
        cv2.line(gray, (koor[9][1],koor[9][0]+20), (koor[9][1],koor[9][0]),  (255,255,255), 20)
        #plot(gray)
        box, edged = firkant(gray,orig)
        koor[0] = [box[2][1],box[2][0]]
        koor[1] = [box[3][1],box[3][0]]

    koor.pop(6)
    koor.insert(6,[0,0])
    return(img, koor, orig, img_front, punkt_c, first, nervehule, rent_bilde)


               
def draw_multi(koor, orig):
    for i in range(len(koor)):
        row, col = koor[i]
        draw_circle(row, col, orig) 
    return(orig)
    
def image(img):
    img_back, koor, orig, img_front, punkt_c, first, nervehule, rent_bilde = bilde_back(img)
    orig = draw_multi(koor, rent_bilde.copy())
    #plot(orig)
    return(koor, orig, nervehule, punkt_c, rent_bilde)
