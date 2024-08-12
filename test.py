y = 0
dy = 0.42
for i in range(0, 60, 2):
    y += dy * 0.02
    dy -= 0.0318
    dy *= 0.9920
    print("{}: {}, {}".format(i, y, dy))