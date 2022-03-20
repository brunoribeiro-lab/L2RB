try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import numpy as np
im = cv2.imread("../now.png")
top = 152
right = 1100
width = 30
height = 20
crop_img = im[top : (top + height) , right: (right + width)]
sought =[185, 185, 186]

#imm=np.array(Image.open("p.png").convert('RGB'))
imm = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
 
# Find all pixels where the 3 NoTE ** BGR not RGB  values match "sought", and count
result = np.count_nonzero(np.all(imm==sought,axis=2))
print(result)
if result > 15000  : 
    print("Play On")
else:
    print("Play Off")
    
cv2.imwrite("test.png", crop_img)