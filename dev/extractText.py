try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2

OCR = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = OCR
ima = cv2.imread("../now2.png")
im = cv2.cvtColor(ima, cv2.COLOR_BGR2RGB)
# crop
"""top = 165
right = 40
height = 420
width = 257
crop_img = im[top : (top + height) , right: (right + width)]
"""
text = pytesseract.image_to_string(im, lang='eng')
print(text)
#cv2.imwrite("test2.png", crop_img)