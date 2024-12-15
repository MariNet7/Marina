chi = int(input())
cl = ""
if chi % 2 == 0 and chi % 25 == 0:
    cl += "A + "
else:
    cl += "A - "
if chi % 2 != 0 and chi % 25 == 0:
    cl += "B + "
else:
    cl += "B - "
if chi % 8 == 0:
    cl += "C +"
else:
    cl += "C -"
print(cl)