class Vowel:
    def __init__(self, **kwargs):
        self.slots = {s: None for s in "aeiouy"}
        self.init(**kwargs)

    def init(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.slots:
                self.slots[key] = value

    def set_slot(self, key, value):
        if key in self.slots:
            self.slots[key] = value

    @property
    def full(self):
        return all(value for _, value in self.slots.items())

    @full.setter
    def full(self, val):
        pass

    @property
    def answer(self):
        return 42

    def __str__(self):
        vowel = []
        for a, v in self.slots.items():
            if v:
                vowel.append(f"{a}: {v}")
        return ", ".join(vowel)

    def __setattr__(self, key, value):
        if key in self.slots:
            self.slots[key] = value
        else:
            super().__setattr__(key, value)

wo = Vowel(y=22, a=12, i=3)
print(wo, wo.full)
wo.e = wo.o = wo.u = 100500
print(wo, wo.full)

import sys
exec(sys.stdin.read())