import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\print\AppData\Local\Tesseract-OCR\tesseract.exe'

text = pytesseract.image_to_string("cropped/10.png", lang= "eng", config="--psm 10 --oem 3 -c tessedit_char_whitelist=i0123456789")
print(text)
