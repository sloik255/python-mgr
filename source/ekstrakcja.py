import numpy as np
import cv2
from numba import jit

@jit
def ekstrakcja(img):

    size = np.size(img)
    skel = np.zeros(img.shape,np.uint8) 
    
    #odwrocenie kolorow - wymagane przez cv2
    ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    
    #generacja elementow strukturalnych dla operacji morfologicznych
    element_square = np.array([[1,1,1],[1,1,1],[1,1,1]])
    element_cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    
    #dylatacja
    img = cv2.dilate(img,element_square,iterations = 1)        
    #zamkniecie obiektu
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, element_cross)
    
    #szkieletyzacja iteracyjna
    done = False
    while( not done):
        eroded = cv2.erode(img,element_cross)
        temp = cv2.dilate(eroded,element_cross)
        temp = cv2.subtract(img,temp)
        skel = cv2.bitwise_or(skel,temp)
        img = eroded.copy()
    
        zeros = size - cv2.countNonZero(img)
        if zeros==size:
            done = True
    
    #pogrybienie linii to dwoch pikseli
    img = cv2.dilate(img,np.array([[1,1],[1,1]]),iterations = 1)
    
    #ponowne odrocenie kolorow
    ret,out = cv2.threshold(skel,127,255,cv2.THRESH_BINARY_INV)
    
    return skel