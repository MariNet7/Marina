from math import *

def Calc(s, t, u):
    def ff(vblr):
        form = f"def func(x): return {vblr}"
        exec(form, globals())
        return func
    x_func = ff(s)
    y_func = ff(t)

    def calc(z):
        x = x_func(z)
        y = y_func(z)
        return eval(u)

    return calc

print(Calc(*eval(input()))(eval(input())))