test = "20 20:00 / 15 22:00 / 16 23:00"
test = "20 20:00"

if "/" in test:
    msg = test.split(" / ")
    msg = (x.split() for x in msg)

else:
    msg = (test.split(), )
    print(msg)
