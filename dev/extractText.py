try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
ima = cv2.imread("../now.png")
im = cv2.cvtColor(ima, cv2.COLOR_BGR2RGB)
# crop
top = 165
right = 40
height = 420
width = 257
crop_img = im[top : (top + height) , right: (right + width)]

text = pytesseract.image_to_string(im, lang='eng')
print(text)
cv2.imwrite("test2.png", crop_img)