"""This is module."""
import sys
from math import *

def thefun(a, b, c):
    """Some function."""
    return int(a) / int(b) + sin(int(c))

l = sys.argv[1]
a = b = l
print(thefun(a, b, l))
