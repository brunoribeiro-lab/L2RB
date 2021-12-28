try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import numpy as np

im = cv2.imread("../now.png")
top = 67 
right = 506
height = 20
width = 250
crop_img = im[top : (top + height) , right: (right + width)]
sought = [184, 15, 15]

#imm=np.array(Image.open("p.png").convert('RGB'))
imm = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
 
# Find all pixels where the 3 NoTE ** BGR not RGB  values match "sought", and count
result = np.count_nonzero(np.all(imm==sought,axis=2))
print(result)
if result > 90 and result < 200 : 
    print("Play On")
else:
    print("Play Off")
    

cv2.imwrite("test.png", crop_img)