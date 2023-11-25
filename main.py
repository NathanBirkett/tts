from playsound import playsound

track = 0
while True:
    inpt = input("> ")
    if inpt == "q":
        break
    elif inpt == "n":
        track += 1
    elif inpt == "":
        pass
    elif inpt.isnumeric():
        track = int(inpt)
    print(track)
    playsound("outTest1/{}.mp3".format(track))