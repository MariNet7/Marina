from collections import defaultdict

class Omnibus:
    kol = defaultdict(set)
    def __setattr__(self, name, znach):
        self.kol[name].add(self)
    def __getattr__(self, name):
        return len(self.kol[name])
    def __delattr__(self, name):
        if self in self.kol[name]:
            self.kol[name].remove(self)

import sys
exec(sys.stdin.read())
