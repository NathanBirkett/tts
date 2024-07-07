import pytesseract
import cv2
import numpy as np
import statistics as st

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\print\AppData\Local\Tesseract-OCR\tesseract.exe'

image = cv2.cvtColor(cv2.imread("in.png"), cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 20))
dilation = cv2.dilate(thresh, kernel)
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# maxHeight = cv2.boundingRect(max(contours, key=lambda c: cv2.boundingRect(c)[3]))[3]
heights = list(map(lambda c: cv2.boundingRect(c)[3], contours))
print(heights)
maxHeight = st.median(heights)
print(maxHeight)
maxHeight = 50

for y in range(image.shape[0]):
    for x in range(image.shape[1] - 1, -1, -1):
        try:
            image[y, x] = image[y, x-int(((y+16)%33.4)*0.25)]
        except:
            print("error")
            image[y, x] = (255, 255, 255)
a = 1
kernel = np.ones((a,a),np.float32)/a**2
image = cv2.filter2D(image,-1,kernel)
# two = cv2.GaussianBlur(image, (0, 0), 3)
cv2.imwrite("out.png", image)
# image = np.array(image)[:, :, ::-1].copy()
text = pytesseract.image_to_string(image, lang="vie")
print(text)