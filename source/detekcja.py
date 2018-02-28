import cv2
import numpy as np


def detection(image):
    
    img = cv2.flip(image, 1)
    
    l_thres = np.int32(np.size(img, axis=0) / 2.5)
    #print l_thres
    all_lines = cv2.HoughLines(img,rho=1,theta=np.pi/180,threshold=l_thres)
    
    if (not (np.size(all_lines) >= 3)):
        return 0
        #all_lines = np.zeros([1,1,2], np.float32)
    
    #distances = all_lines[:,0,0]    
    fi = all_lines[:,0,1]*180/np.pi

    
    angle = np.median(fi)
    if (angle == 0):
        return 0
    elif (angle <= 90):
        angle = 90 - angle
        return angle
    elif (angle > 90):
        angle = 270 - angle
        return angle
    else:
        return 0

    return 0

def limcheck(angle, limits = (0,180)):
    if ((angle < limits[0]) or (angle > limits[1])):
        return False
    else:
        return True
    
    return False