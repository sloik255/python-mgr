import cv2
import numpy as np

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
    
    
    img = cv2.flip(image, 1)
    
    l_thres = np.int32(np.size(img, axis=0) / 2.5)
    
    all_lines = cv2.HoughLines(img,rho=1,theta=np.pi/180,threshold=l_thres)
    
    if (not (np.size(all_lines) >= 3)):
        return _err.too_much_lines
    
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
        pass

    return _err.fatal_from_detection

def calculateValue(angle, angle_lim, value_range):
    
    if (angle < angle_lim[0]):
        return _err.angle_below_min
    if (angle > angle_lim[1]):
        return _err.angle_above_max
    
    value = (angle-angle_lim[0])/(angle_lim[1]-angle_lim[0]) *value_range
    
    if ((value < 0) or (value > value_range)):
        return _err.value_out_of_limits
    
    if (value < 0):
        return _err.value_below_min
    if (value > value_range):
        return _err.value_above_max
    
    return value
    
    
    
    
    