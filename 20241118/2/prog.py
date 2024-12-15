class Invalid_Input(Exception):
    pass
class Not_a_triangle(Exception):
    pass

def triangleSquare(inStr):
    try:
        (x1, y1), (x2, y2), (x3, y3) = eval(inStr)
    except:
        raise Invalid_Input
    ploshad = abs((x1 - x3) * (y2 - y3) - (y1 - y3) * (x2 - x3))
    if ploshad <= 0:
        raise Not_a_triangle
    else:
        return ploshad*0.5

while True:
    try:
        stroka = triangleSquare(input())
    except Invalid_Input:
        print("Invalid input")
    except Not_a_triangle:
        print("Not a triangle")
    else:
        print(f"{stroka:.2f}")
        break
