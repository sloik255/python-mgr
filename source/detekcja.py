import cv2
import numpy as np
from skimage.transform import hough_line 

class err:
    def __init__(self):
        self.too_much_lines = -1
        self.fatal_from_detection = -2
        self.angle_below_min = -3
        self.angle_above_max = -4
        self.value_below_min = -5
        self.value_above_max = -6
        pass
    pass


_err = err()

def detection(image):
    
    #ujednolicenie ukladu wspolrzednych
    img = cv2.flip(image, 1)
    #obliczenie minimalnej dlugosci wykrywanej linii
    l_thres = np.int32(np.size(img, axis=0) / 2.5)
    #uzyskanie wyniku transformacji Hougha w postaci danych linii
    hough, theta, d = hough_line(image, np.linspace(-np.pi/2, np.pi/2, 360*2))    
    
    h = hough
    maxindex = h.argmax();
    #odrzucenie transformacji gdy wykryto za duzo linii
    #print h.max()
    if (h.max()<l_thres):
        return _err.value_below_min
    
    if (maxindex > np.size(h, 1)):
        row = maxindex/np.size(h,1)
        column = maxindex - row*np.size(h,1)
    #przeliczenie radianow na stopnie
    
    angle = column/4.0
    
    #print "kat:", angle
    return angle

def detection_cv2(image):
    
    #ujednolicenie ukladu wspolrzednych
    img = cv2.flip(image, 1)
    #obliczenie minimalnej dlugosci wykrywanej linii
    l_thres = np.int32(np.size(img, axis=0))# / 1.5)
    #uzyskanie wyniku transformacji Hougha w postaci danych linii
    all_lines = cv2.HoughLines(img,rho=1,theta=np.pi/180,threshold=l_thres)  
    
    #odrzucenie transformacji gdy wykryto za duzo linii
    if (not (np.size(all_lines) >= 3)):
        return _err.too_much_lines
    
    #przeliczenie radianow na stopnie
    fi = all_lines[:,0,1]*180/np.pi
    
    #print "kat 0:", fi

    #unormowanie wyniku do ukladu wspolrzednych i zwrocenie wyniku
    for i in range (0, np.size(fi)):
        if (fi[i] <= 90):
            fi[i] = 90 - fi[i]
        elif (fi[i] > 90):
          fi[i] = 270 - fi[i]
          
    #print "kat 1:", fi        
    angle = np.median(fi)
    
    #print "kat:", angle
    return np.float(angle)


def calculateValue(angle, angle_lim, value_range):
    
    if (angle < angle_lim[0]):
        return _err.angle_below_min
    if (angle > angle_lim[1]):
        return _err.angle_above_max
    
    value = (angle*1.0-angle_lim[0]*1.0)/(angle_lim[1]*1.0-angle_lim[0]*1.0) *value_range*1.0
    
    if ((value < 0) or (value > value_range)):
        return _err.value_out_of_limits
    
    if (value < 0):
        return _err.value_below_min
    if (value > value_range):
        return _err.value_above_max
    
    return value
    
    
    
    
    