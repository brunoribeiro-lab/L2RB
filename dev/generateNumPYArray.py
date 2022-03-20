try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import numpy as np
import numpy
from numpy import asarray
from numpy import savetxt

"""im = cv2.imread("../now.png")
top = 152
right = 1100
width = 30
height = 20
crop_img = im[top : (top + height) , right: (right + width)]
imm = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
cv2.imwrite("findCrop.png", imm)"""


"""im = Image.open('findCrop.png')
pixels = list(im.getdata())
width, height = im.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
print(pixels)"""
im = cv2.imread("../now.png")
top = 152
right = 1100
width = 30
height = 20
crop_img = im[top : (top + height) , right: (right + width)]
pixels = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
arr = numpy.array(pixels)
newarr = arr.reshape(arr.shape[0], (arr.shape[1]*arr.shape[2]))
print(newarr)

#np.savetxt("Training_10007474.txt", pixels, delimiter=" ")
np.savetxt('a.dll', newarr, fmt='%s', delimiter=" ")
cv2.imwrite("findCrop.png", pixels)

        
