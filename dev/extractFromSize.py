try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
im = cv2.imread("now.png")
top=361
right=2
height= 80
width=250
crop_img = im[top : (top + height) , right: (right + width)]
cv2.imwrite("test.png", crop_img)

text = pytesseract.image_to_string(crop_img, lang='eng')
print(text)


if text.find('already fulfilled cannot be') > 0:
    print("PASSO 2")
    
if text.find('Target Location:') > 0:
    print("PASSO 1")
    
    
if text.find('been disconnected as you') > 0:
    print("I disconnect")
    
elif text.find('Character Name') > 0:
    print("Passo 1")