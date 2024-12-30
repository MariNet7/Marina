class Vowel:
    slots = 'a', 'e', 'i', 'o', 'u', 'y'

    def __init__(self, a=None, e=None, i=None, o=None, u=None, y=None):
        self.a = a
        self.e = e
        self.i = i
        self.o = o
        self.u = u
        self.y = y


    def poln(self):
        return all(getattr(self, slot) is not None for slot in self.slots)

    def __str__(self):
        values = [f"{slot}: {getattr(self, slot)}" for slot in sorted(self.slots) if getattr(self, slot) is not None]
        return ', '.join(values)

    @property
    def answer(self):
        return 42

    @property
    def full(self):
        return self.poln()

    @full.setter
    def full(self, value):
        pass

import sys
exec(sys.stdin.read())