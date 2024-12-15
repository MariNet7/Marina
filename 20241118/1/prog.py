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

        for i in range(0, l, delen):
            yield self.data[i:i + delen]

from sys import stdin
exec(stdin.read())