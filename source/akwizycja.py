import numpy as np
import matplotlib.pylab as pyl
import cv2


def getPoints(img):
    
    points = (0,0,0,0)
            
    try:
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except:
        print "cannot get frame, firstly run camera"
        return (False, points)

    
    a = left(image[:,0:np.size(image,axis=1)/3])
    b = right(image[:,np.size(image,axis=1)/3*2:np.size(image,axis=1)]) \
        + np.size(image,axis=1)/3*2 
    c = top(image[0:np.size(image,axis=0)/3,:])
    d = bottom(image[np.size(image,axis=0)/3*2:np.size(image,axis=0),:]) \
        + np.size(image,axis=0)/3*2
    
    points = (a+10, b-10, c+10, d-20)
    print points

    return (True, points)

def left(image):
    
    x_min = 0
    img = image
    while (1):
        ad00 = np.sum(img, axis=0)
        differ = np.zeros(np.size(ad00), dtype=np.double)
        for r in range(0, np.size(ad00)-2):
            differ[r] = np.abs(ad00[r+1]*1.0 - ad00[r]*1.0)
        
        a = np.max(differ)/10
        b = np.mean(np.append(differ, -np.max(differ)))
        if (a<b):
            return x_min
        else:
            x_min = x_min + np.argmax(differ)+1
            img = image[:,np.abs(x_min):np.size(image,axis=1)]
            
def right(image):
    
    img = image
    x_max = np.size(img,axis=1)
    
    while (1):
        ad01 = np.sum(img, axis=0)
        differ = np.zeros(np.size(ad01), dtype=np.double)
        for r in range(0, np.size(ad01)-2):
            differ[r] = np.abs(ad01[r+1]*1.0 - ad01[r]*1.0)

        a = np.max(differ)/10
        b = np.mean(np.append(differ, -np.max(differ)))
        if (a<b):
            return x_max
        else:
            x_max = np.argmax(differ)
            img = img[:,0:np.abs(x_max)]

def top(image):
    
    y_min = 0
    img = image
    while (1):
        ad10 = np.sum(img, axis=1)
        differ = np.zeros(np.size(ad10), dtype=np.double)
        for r in range(0, np.size(ad10)-2):
            differ[r] = np.abs(ad10[r+1]*1.0 - ad10[r]*1.0)
        
        a = np.max(differ)/10
        b = np.mean(np.append(differ, -np.max(differ)))
        if (a<b):
            return y_min
        else:
            y_min = y_min + np.argmax(differ)+1
            img = image[np.abs(y_min):np.size(image,axis=0)]

def bottom(image):
    
    img = image
    y_max = np.size(img,axis=0)
    while (1):
        ad11 = np.sum(img, axis=1)
        differ = np.zeros(np.size(ad11), dtype=np.double)
        for r in range(0, np.size(ad11)-2):
            differ[r] = np.abs(ad11[r+1]*1.0 - ad11[r]*1.0)

        a = np.max(differ)/10
        b = np.mean(np.append(differ, -np.max(differ)))
        if (a<b):
            return y_max
        else:
            y_max = np.argmax(differ)
            img = img[0:np.abs(y_max)]
    
'''def left(image):
    
    x_min = 0
    img = image
    while (1):
        ad00 = np.sum(img, axis=0)
        differ = np.zeros(np.size(ad00), dtype=np.double)
        for r in range(0, np.size(ad00)-2):
            differ[r] = np.abs(ad00[r+1]*1.0 - ad00[r]*1.0)
        print differ

        pyl.figure()
        pyl.plot(differ)
        pyl.show(block=True)
        
        a = np.max(differ)/10
        b = np.mean(np.append(differ, -np.max(differ)))
        print a, " < ", b
        if (a<b):
            return x_min
        else:
            x_min = x_min + np.argmax(differ)+1
            img = image[:,np.abs(x_min):np.size(image,axis=1)]
            
def right(image):
    
    img = image
    x_max = np.size(img,axis=1)
    
    while (1):
        ad01 = np.sum(img, axis=0)
        differ = np.zeros(np.size(ad01), dtype=np.double)
        for r in range(0, np.size(ad01)-2):
            differ[r] = np.abs(ad01[r+1]*1.0 - ad01[r]*1.0)
        print differ
        pyl.figure()
        pyl.plot(differ)
        pyl.show(block=True)
        
        a = np.max(differ)/10
        b = np.mean(np.append(differ, -np.max(differ)))
        if (a<b):
            return x_max
        else:
            x_max = np.argmax(differ)
            img = img[:,0:np.abs(x_max)]

def top(image):
    
    y_min = 0
    img = image
    while (1):
        ad10 = np.sum(img, axis=1)
        differ = np.zeros(np.size(ad10), dtype=np.double)
        for r in range(0, np.size(ad10)-2):
            differ[r] = np.abs(ad10[r+1]*1.0 - ad10[r]*1.0)
        print differ
        
        pyl.figure()
        pyl.plot(differ)
        pyl.show(block=True)
        
        a = np.max(differ)/10
        b = np.mean(np.append(differ, -np.max(differ)))
        if (a<b):
            return y_min
        else:
            y_min = y_min + np.argmax(differ)+1
            img = image[np.abs(y_min):np.size(image,axis=0)]

def bottom(image):
    
    img = image
    y_max = np.size(img,axis=0)
    while (1):
        ad11 = np.sum(img, axis=1)
        differ = np.zeros(np.size(ad11), dtype=np.double)
        for r in range(0, np.size(ad11)-2):
            differ[r] = np.abs(ad11[r+1]*1.0 - ad11[r]*1.0)
        print differ
        
        pyl.figure()
        pyl.plot(differ)
        pyl.show(block=True)
        
        a = np.max(differ)/10
        b = np.mean(np.append(differ, -np.max(differ)))
        if (a<b):
            return y_max
        else:
            y_max = np.argmax(differ)
            img = img[0:np.abs(y_max)]'''