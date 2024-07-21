import os
import re
import string

from gtts import gTTS


with open("in.txt", "r", encoding='utf-8') as f:
    text = f.read()
    text = text.replace('“', '"').replace('”', '"')
    
with open("out.txt", "w+", encoding='utf-8') as f:
    f.write("")
    
def split(pattern, string):
    split1 = re.split(pattern, string)
    split2 = []
    s = 0
    while s < len(split1):
        if re.match(pattern, split1[s]):
            split2.append(split1[s] + split1[s+1])
            s += 1
        else:
            split2.append(split1[s])
        s += 1
    return split2
    
with open("out.txt", "a+", encoding='utf-8') as f:
    chapters = text.split("Drills")
    for i in range(len(chapters)):
            chapter = split(r'([A-Z]\. )', chapters[i])
            chapters[i] = chapter
            f.write("<chap>\n")
            for j in range(len(chapter)):
                section = split(r'(\d+[.,] )', chapter[j])
                chapters[i][j] = section
                f.write("<sec>\n")
                for k in range(len(section)):
                    question = re.sub(r'"[^"]*"', "", section[k].replace("\n", " "))
                    question = re.sub(r'_+', "[trống]", question)
                    chapters[i][j][k] = question
                    f.write(question + "\n")
                f.write("</sec>\n")
            f.write("</chap>\n")