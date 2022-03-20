import numpy as np
import cv2
import numbers
import warnings
from contextlib import suppress
from numpy.linalg import norm
im = cv2.imread("now.png")  
top = 152
right = 1100
width = 30
height = 20
crop_img = im[top : (top + height) , right: (right + width)]
pixels = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
arr = np.array(pixels)
# reshaping the array from 3D
# matrice to 2D matrice.
newarr = arr.reshape(arr.shape[0], (arr.shape[1]*arr.shape[2]))
# skipping first row
# converting file data to string
data = np.loadtxt("iboss.dll", skiprows=1, dtype='str')
totalFound = 0
"""energies = (np.hsplit(data, 3))[0]
A = np.array(data)
B = np.array(newarr)
cosine = np.sum(A*B, axis=1)/(norm(A, axis=1)*norm(B, axis=1))
print("Cosine Similarity:", cosine)"""

"""for each in energies:
    print(each)"""
"""
difference = cv2.absdiff(data, newarr)
result = cv2.countNonZero(difference)
print(result)
print(difference)"""
"""error = np.mean( newarr != data )
print(error)
np.savetxt('a.dll', error, fmt='%s', delimiter=" ")"""

def get_image_difference(image_1, image_2):
    first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
    second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

    img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
    img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
    img_template_diff = 1 - img_template_probability_match

    # taking only 10% of histogram diff, since it's less accurate than template method
    commutative_image_diff = (img_hist_diff / 10) + img_template_diff
    return commutative_image_diff

img2 = cv2.imread('findCrop.png', 0)
#--- find percentage difference based on number of pixels that are not zero ---
percentage = get_image_difference(crop_img, img2)
print(percentage)
if percentage > 1 : 
    print("not found")
else:
    print("Found")