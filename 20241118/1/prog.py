from collections import UserString

class DivStr(UserString):
    def __init__(self, s=""):
        super().__init__(s)

    def __mod__(self, n):
        l = len(self.data)
        delen = l // n
        ost = self.data[delen * n:]
        return self.__class__(ost)

    def __floordiv__(self, n):
        l = len(self.data)
        delen = l // n

        s = [self[i*delen:(i+1)*delen] for i in range(n)]
        return iter(s)

from sys import stdin
exec(stdin.read())