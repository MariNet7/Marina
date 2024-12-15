def fib(m, n):
    c1, c2 = 0, 1
    for i in range(0, m+n):
        c1, c2 = c2, c1+c2
        if i >= m:
            yield c1
from sys import stdin
exec(stdin.read())
