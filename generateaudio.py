import os
from gtts import gTTS

for file in os.listdir("texts/out"):
    with open("texts/out/{}".format(file), "r", encoding='utf-8') as f:
        chapter = file.removesuffix(".txt")
        section = 0
        question = 0
        part = -1
        in_part = False
        for line in f:
            line = line[:-1]
            if line == "<chap>":
                # chapter += 1
                if not os.path.exists("out/c{:02}".format(chapter)):
                    os.mkdir("out/c{:02}".format(chapter))
            elif line == "</chap>":
                sec = 0
            elif line == "<sec>":
                section += 1
                if not os.path.exists("out/c{:02}/s{:02}".format(chapter, section)):
                    os.mkdir("out/c{:02}/s{:02}".format(chapter, section))
            elif line == "</sec>":
                question = 0
                part = 0
            elif line == "<part>":
                part += 1
                in_part = True
                if not os.path.exists("out/c{:02}/s{:02}/p{:02}".format(chapter, section, part)):
                    os.mkdir("out/c{:02}/s{:02}/p{:02}".format(chapter, section, part))
            elif line == "</part>":
                question = 0
                in_part = False
            else:
                question += 1
                filename = ""
                if not in_part:
                    filename = "out/c{:02}/s{:02}/q{:02}.mp3".format(chapter, section, question)
                else:
                    filename = "out/c{:02}/s{:02}/p{:02}/q{:02}.mp3".format(chapter, section, part, question)
                with open (filename, 'wb') as ff:
                    if not in_part:
                        print("{}-{}-{}".format(chapter, section, question))
                    else:
                        print("{}-{}-{}-{}".format(chapter, section, part, question))
                    print(line)
                    try:
                        tts = gTTS(text=line, lang="vi")
                        # print(tts.text)
                        tts.write_to_fp(ff)
                    except:
                        print(question)