import numpy as np
import matplotlib.pylab as pyl
import cv2
from numba import jit

@jit
def ekstrakcja(img):
    size = np.size(img)
    skel = np.zeros(img.shape,np.uint8) 
    
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    
    ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    img = cv2.dilate(img,np.array([[1,1,1],[1,1,1],[1,1,1]]),iterations = 1)
    
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, element)
    

    done = False
    
    while( not done):
        eroded = cv2.erode(img,element)
        temp = cv2.dilate(eroded,element)
        temp = cv2.subtract(img,temp)
        skel = cv2.bitwise_or(skel,temp)
        img = eroded.copy()
    
        zeros = size - cv2.countNonZero(img)
        if zeros==size:
            done = True
    
    img = cv2.dilate(img,np.array([[1,1],[1,1]]),iterations = 1)
    ret,out = cv2.threshold(skel,127,255,cv2.THRESH_BINARY_INV)
    return skel

'''
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                                [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                                [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
                                [0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
                                [0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0],
                                [0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0],
                                
'''