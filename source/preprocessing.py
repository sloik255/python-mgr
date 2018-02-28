import cv2
import numpy as np
import bisect
from numba import jit

##############################################################################
''' funkcja zewnetrzna ''' 
##############################################################################
def preprocessing(image):
    img = image
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img3 = imadjust(img2)
    
    img4 = sauvola(img3, k=0.15, window=(10,3))
    
    
    
    return img4

##############################################################################
''' funkcje wewnatrz ''' 
##############################################################################
@jit
def imadjust(src, tol=1, vin=[0,255], vout=(0,255)):
    dst = src.copy()
    tol = max(0, min(100, tol))

    if tol > 0:
        # Compute in and out limits
        # Histogram
        hist = np.zeros(256, dtype=np.int)
        for r in range(src.shape[0]):
            for c in range(src.shape[1]):
                hist[src[r,c]] += 1
        # Cumulative histogram
        cum = hist.copy()
        for i in range(1, len(hist)):
            cum[i] = cum[i - 1] + hist[i]

        # Compute bounds
        total = src.shape[0] * src.shape[1]
        low_bound = total * tol / 100
        upp_bound = total * (100 - tol) / 100
        vin[0] = bisect.bisect_left(cum, low_bound)
        vin[1] = bisect.bisect_left(cum, upp_bound)

    # Stretching
    if ((vin[1] - vin[0])==0):
        scale = 255
    else:
        scale = (vout[1] - vout[0]) / (vin[1] - vin[0])
    for r in range(dst.shape[0]):
        for c in range(dst.shape[1]):
            vs = max(src[r,c] - vin[0], 0)
            vd = min(int(vs * scale + 0.5) + vout[0], vout[1])
            dst[r,c] = vd
    return dst

def imequalize(img):
    return cv2.equalizeHist(img)

def adjust_gamma(image, gamma=1.0): #function from internet
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
 
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)

def sauvola(image, window=(3,3), k=0.2): 
    # Convert to double
    image = np.float32(image)
    image = image/255
    
    # Mean value
    mean = cv2.blur(image, window)
    
    # Standard deviation
    meanSquare = cv2.blur(np.power(image, 2), window)
    deviation = np.power((meanSquare - np.power(mean, 2)), 0.5)
    # Sauvola
    R = np.amax(deviation);
    threshold = np.multiply(mean, (1 + k * (deviation / R-1)))
    output = np.uint8(image > threshold)*255
    return output
