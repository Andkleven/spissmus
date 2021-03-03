
        
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 16:23:46 2018

@author: amkle
"""

import cv2
from math import acos, sqrt, pi, exp
import numpy as np


#mmPerPixsel = 6/280
colors = {'red':(255,0,0), 'blue':(0,0,255), 'gul':(255,255,0), 'grenn':(0,255,0)}  


def draw_linje(img, linje, key):                                                        # tegne linje på bilder mellom to punkter, når du har funnet linjene
    shape= np.shape(img)
    img = draw_line(img,key, 0, linje[1], shape[1], (linje[0]*shape[1]+ linje[1]))
    
def draw_line(img,key, x1,y1,x2,y2):
	cv2.line(img, (int(x1),int(y1)), (int(x2),int(y2)), (colors[key]), 2)              # tegner linjen mellom to punkter 
      
def measure(x1,y1,x2,y2):                                                           # måler avstanden mellom to punkter. Med for holdet mmPerPixsel = 6/280
    mmPerPixsel = 6/280
    lengde = np.sqrt(((x1-x2)**2)+((y1-y2)**2))*mmPerPixsel
    return(lengde)

def text(img,x1,y1,x2,y2,lengde):                                                   # Skiver lengenen på en linje på bilde
    cv2.putText(img, "{:.1f}mm".format(lengde),
		(int(x1+abs((x2-x1)/2)), int(y1+abs((y2-y1)/2))), cv2.FONT_HERSHEY_SIMPLEX,
		0.70, (255,0,0),2)
    
def text_vinkel(img,x,y,vinkel):                                                    # Skirver vinkelen mellom to linjen på bilde
    cv2.putText(img, "{:.1f}".format(vinkel),
		(int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX,
		0.70, (255,255,255),2)
    

def linje(x1,x2,y1,y2,x3=None,y3=None):                                             # Finner linjen mellom to eller tre punkter 
    if x3==None:
        x = np.array([x1,x2])
        y = np.array([y1,y2])   
    else:
        x = np.array([x1,x2,x3])
        y = np.array([y1,y2,y3])  
    linje = np.polyfit(x,y,1)                   # bruker numpys ployfit som bruker regresjon til å finne snitt linjen(https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.polyfit.html)
    return(linje)
    
def vektor(x1,x2,y1,y2,x3=None,y3=None):                                            # Finner to eller en vektor fra samme punkt
    vektor1 = [(x1-x2),(y1-y2)]
    if x3==None:
        vektor2=0
    else:
        vektor2 = [(x3-x2),(y3-y2)]
    return(vektor1, vektor2)
    
    
    
def vektor_linje(linje1,linje2):                                                    # Finner en-hetes vektorerne to to linje og krysspunktet 
    x = (linje1[1]-linje2[1])/(linje2[0]-linje1[0])
    y = linje1[0]*x + linje1[1]
    x1 = 150
    y1 = linje1[0]*x1 + linje1[1]
    y2 = linje2[0]*x1 + linje2[1]
    vektor1 = [int(x1-x),int(y1-y)]
    vektor2 = [int(x1-x),int(y2-y)]
    return(vektor1,vektor2,x,y)
    
def vinkel1(vektor1,vektor2):                                                       # Finner vinkelen mellom to vektorer
    vinkel = acos(((vektor1[0]*vektor2[0])+(vektor1[1]*vektor2[1]))/
                  (sqrt((vektor1[0]**2)+(vektor1[1]**2))*sqrt((vektor2[0]**2)+(vektor2[1]**2))))*(180/pi)

    return(vinkel)
    
def finn_mus(measur,v):                                                             # Finner ut hvilken ART det er med FORMELEN
    prosent = (exp(-2290+(165*measur[1])+(-4.40*measur[2])+(258*measur[0])))/(1+(exp(-2290+(165*measur[1])+(-4.40*measur[2])+(258*measur[0]))))
    if prosent <  .4:
        art = 'Araneus'
    elif 1 >= prosent > .95:
        art = 'Isodon'
    else:
        art = 'ubestemt'
    
    return(art, prosent)
    
    
def run(v):                                                                     # Hovedfunsjonen som kjører de andre programmene. Tar en en liste med bilde og punkter på bilde.
    measur = []
    img = v[1]

    draw_line(img,'grenn', v[0][4][1],v[0][4][0],v[0][9][1],v[0][9][0])
    mea = measure(0,v[0][4][0],0,v[0][9][0])                                # Måler Height
    measur.append(mea)                                                          # Legger den til i liste over mål        
    text(img,v[0][4][1],v[0][4][0],v[0][9][1],v[0][9][0],mea)     
    if v[2]:                                                                    # Måler Length
        draw_line(img,'red',v[0][3][1],v[0][3][0],v[0][8][1],v[0][8][0])
        mea = measure(v[0][3][1],v[0][3][0],v[0][8][1],v[0][8][0])
        measur.append(mea)                                                      # Legger den til i liste over mål        
        text(img,v[0][3][1],v[0][3][0],v[0][8][1],v[0][8][0],mea) 
    else:
        measur.append(0)
    
    if v[3]==True:
        linje1 = linje(v[0][0][1],v[0][1][1],v[0][0][0],v[0][1][0],v[0][7][1],v[0][7][0])
    else:
        linje1 = linje(v[0][0][1],v[0][1][1],v[0][0][0],v[0][1][0])
    linje2 = linje(v[0][2][1],v[0][3][1],v[0][2][0],v[0][3][0])
    vektor1,vektor2,x,y  = vektor_linje(linje1,linje2)
    vinkel = vinkel1(vektor1,vektor2)                                           # Måler AngleM
    if x<5:    
        text_vinkel(img,5,y-10,vinkel)
    else:
        text_vinkel(img,x+20,y-5,vinkel)
    draw_linje(img,linje1,'gul')
    draw_linje(img,linje2,'gul')
    measur.append(vinkel)                                                       # Legger den til i liste over mål   
    
    """
    vektor1, vektor2 = vektor(v[0][3][1],v[0][5][1],v[0][3][0],v[0][5][0],v[0][2][1],v[0][2][0])
    vinkel = vinkel1(vektor1,vektor2)
    draw_line(img,'blue', v[0][3][1],v[0][3][0],v[0][5][1],v[0][5][0])
    draw_line(img,'blue', v[0][2][1],v[0][2][0],v[0][5][1],v[0][5][0])
    text_vinkel(img,v[0][5][1]-30,v[0][5][0]-20,vinkel) 
    measur.append(vinkel)
"""
    
    art, prosent = finn_mus(measur,v)
    
    #plot(img)
    return(art,img,measur, prosent)                                                      # returnert bilde, art, liste over mål

    
    
    



    
    


