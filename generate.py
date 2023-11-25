import pytesseract
from PIL import Image
from PIL import ImageFilter
from gradio_client import Client
import re
from gtts import gTTS
import os
import numpy as np
import cv2
import langdetect
import string
import fitz
from pdf2image import convert_from_path
import random

# pdf to png
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\print\AppData\Local\Tesseract-OCR\tesseract.exe'
images = convert_from_path("in.pdf", poppler_path=r"C:\Users\print\Documents\poppler-23.11.0\Library\bin")
# for i in range(len(images)):
# # for i in range(1):
#     text = " ".join([text, pytesseract.image_to_string(images[i], lang="vie", config="")])

text = ""
for i in range(len(images)):
    image = np.array(images[i])[:, :, ::-1].copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 20)) # NOOOOOOOOOOOOOOO make smaller i think
    dilation = cv2.dilate(thresh, kernel)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    ctrs = list(zip(range(len(contours)), [cv2.boundingRect(c) for c in contours]))
    nearest = 70
    ctrs.sort(key=lambda r: [int(nearest * round(float(r[1][1]) / nearest)), r[1][0]])

    im_new = gray.copy()
    j = 0
    for c in ctrs:
        rect = c[1]
        x,y,w,h = rect
        cropped = im_new[y:y + h, x:x + w]
        config = ""
        language = "vie"
        if w < 50 and w > 15:
            config = "--psm 10"
            language = "eng"
        t = pytesseract.image_to_string(cropped, lang=language, config=config) # find a way to capture underscores
        text = "\n".join([text, t])
        j += 1

#text preprocessing
# text = text.split("Drills")[1] # what if there are multiple drills
text = text.replace('“', '"').replace('”', '"')
text = text.replace('§', '8')
text = re.sub(r"\n+", "\n", text)
text = text.replace("ELEMENTARY\nVIETNAMESE\n", "") #fix this

with open("out.txt", 'w+', encoding='utf-8') as f:
    f.write(text)

chapters = text.split("Drills")
chapters.pop()
with open("out3.txt", "a+", encoding='utf-8') as f:
    for i in range(len(chapters)):
        os.mkdir()
        chapter = re.split(r'\d+.\n', chapters[i])
        chapters[i] = chapter
        for j in range(len(chapter)):
            section = re.split(r'\d+[.,] ', chapter[j])
            chapters[i][j] = section
            for k in range(len(section)):
                question = re.sub(r'"[^"]*"', "", section[k].replace("\n", " "))
                chapters[i][j][k] = question
                f.write(question)
                f.write("\n")
                results = []
                lastlang = ""
                firstlang = ""
                for i in range(len(question.split())):
                    # identify language
                    word = question.split()[i]
                    if re.search("[^\x00-\x7F]", word) or word.lower().translate(str.maketrans('', '', string.punctuation)) in ["kia", "xe", "con", "mua", "y", "mai", "lan", "cam", "nay", "xem", "xa", "sinh", "hai", "bia", "ngon", "to", "sang", "ba", "quen", "qua", "bao", "trang", "ai", "ty", "ta"] + list(range(10)):
                        lang = "vi"
                    else:
                        try:
                            langs = langdetect.detect_langs(word)
                            langfound = False
                            for item in langs:
                                if (item.lang == "vi" or item.lang == "en") and not langfound:
                                    lang = item.lang
                                    langfound = True
                            if not langfound:
                                lang = "en"
                        except:
                            lang = "en"
                    if i == 1:
                        firstlang = lang
                    # compile into strings
                    try:
                        if lang == lastlang:
                            results[-1] = " ".join([results[-1], word])
                        else:
                            results.append(word)
                            # f.write(lastlang + " " + results[-2] + "\n")
                            lastlang = lang
                    except:
                        print("bruh")
                        
                # create audio file            
                with open ("out/{}/{}/{}.mp3".format(i, j, k), 'wb') as ff:
                    secondlang = "vi" if firstlang == "en" else "en"
                    for n in range(len(results)):
                        print("{}-{}-{}".format(i, j, k))
                        try:
                            tts = gTTS(text=results[n], lang=firstlang if n%2 == 0 else secondlang)
                            tts.write_to_fp(ff)
                        except:
                            print(results)
                            print(results[n])
            f.write("\n\n")
        f.write("\n\n\n\n")
            
lst1 = re.split(r"\d+.\n", text)
lst2 = sum([re.split(r"\d+[.,] ", q) for q in lst1], [])
lst = list(map(lambda l: re.sub(r'"[^"]*"', "", l.replace("\n", " ")), lst2))[1:-1]
lst0 = lst


    
with open("out2.txt", "w+", encoding="utf-8") as f:
    for l in lst:
        f.write(l)
        f.write("\n")
    
# for j in range(len(lst0)):
    