import cv2
import threading
import time
import numpy as np

rightnow = cv2.imread("n.png")
w, h = rightnow.shape[:2]
# start_x:end_x, start_y:end_y
top=514
right=430
height= 40
width=100
crop_img = rightnow[top : (top + height) , right: (right + width)]
BLUE_MIN = np.array([40,90,130], np.uint8)
BLUE_MAX = np.array([255,255,255], np.uint8)
dst = cv2.inRange(crop_img, BLUE_MIN, BLUE_MAX)
no_blue = cv2.countNonZero(dst)
print('The number of white pixels is: ' + str(no_blue))
if no_blue >= 300 and no_blue <= 500:
    print("Terminou")
else:
    print("N terminou")
    
cv2.imwrite("finish.png", crop_img)
